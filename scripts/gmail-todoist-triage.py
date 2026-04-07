#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

WORKSPACE = Path('/Users/kat/.openclaw/workspace')
TODOIST_ENV = WORKSPACE / '.env.todoist'
STATE_DIR = WORKSPACE / '.openclaw' / 'state'
STATE_DIR.mkdir(parents=True, exist_ok=True)
STATE_FILE = STATE_DIR / 'gmail-todoist-triage.json'

WORK_GMAIL = 'garrett@launchlabs.ai'
WORK_PROJECT_ID = '6g7Mg937PG4P9g6V'
FOLLOWUP_PROJECT_ID = '6g7Mg93mCQHHwXmx'
INBOX_PROJECT_ID = '6g7Mf5J6p939RxX4'

NOISE_HINTS = [
    'newsletter', 'weekly digest', 'weekly report', 'promo', 'promotion', 'receipt',
    'statement', 'summary', 'invited you to', 'ready:', 'intel report', 'digest',
    'your api account', 'jobs alert', 'weekly', 'account statement'
]

HIGH_SIGNAL_HINTS = [
    'action required', 'action needed', 'follow up', 'follow-up', 'question', 'review',
    'security', 'renewal', 'invoice', 'payment', 'alert', 'error', 'issue', 'warning',
    'unread registered agent documents', 'contract', 'docusign', 'launch labs',
    'compliance filings due', 'webhook disconnected'
]


def load_state():
    if not STATE_FILE.exists():
        return {'created_by_thread': {}}
    try:
        return json.loads(STATE_FILE.read_text())
    except Exception:
        return {'created_by_thread': {}}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2) + '\n')


def load_todoist_token():
    for line in TODOIST_ENV.read_text().splitlines():
        if line.startswith('TODOIST_API_TOKEN='):
            return line.split('=', 1)[1].strip()
    raise RuntimeError('TODOIST_API_TOKEN not found')


def run_gog_search(query, limit=25):
    with tempfile.NamedTemporaryFile(mode='r+', suffix='.json', delete=True) as tmp:
        command = (
            f"env GOG_ACCOUNT='{WORK_GMAIL}' gog gmail search "
            f"{json.dumps(query)} --max {int(limit)} --json > {json.dumps(tmp.name)}"
        )
        subprocess.run(['bash', '-lc', command], check=True, timeout=60)
        tmp.seek(0)
        return json.load(tmp)


def classify(thread):
    subject = (thread.get('subject') or '').strip()
    subject_l = subject.lower()
    sender = (thread.get('from') or '').strip()
    sender_l = sender.lower()
    labels = [l.lower() for l in (thread.get('labels') or [])]

    if 'category_promotions' in labels:
        return None
    if any(h in subject_l for h in NOISE_HINTS):
        return None
    if 'noreply' in sender_l and not any(h in subject_l for h in HIGH_SIGNAL_HINTS):
        return None

    if any(h in subject_l for h in HIGH_SIGNAL_HINTS):
        return {
            'project_id': WORK_PROJECT_ID,
            'content': f'Email follow-up: {subject}',
            'reason': 'high-signal subject',
        }

    if any(name in sender_l for name in ['tristan', 'sam ', 'scott ', 'mike ', 'emily ', 'holly ', 'matthew', 'eric ']):
        return {
            'project_id': WORK_PROJECT_ID,
            'content': f'Review email from {sender.split("<",1)[0].strip()}: {subject}',
            'reason': 'known work contact',
        }

    return None


def create_todoist_task(token, content, project_id, description=''):
    payload = {
        'content': content,
        'project_id': project_id,
        'description': description,
    }
    req = urllib.request.Request(
        'https://api.todoist.com/api/v1/tasks',
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        },
        method='POST',
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def main():
    args = sys.argv[1:]
    create_mode = '--create' in args
    limit = 25
    query = 'is:unread newer_than:2d'

    filtered = []
    skip = False
    for i, arg in enumerate(args):
        if skip:
            skip = False
            continue
        if arg == '--create':
            continue
        if arg == '--max' and i + 1 < len(args):
            limit = int(args[i + 1])
            skip = True
            continue
        filtered.append(arg)
    if filtered:
        query = filtered[0]

    results = run_gog_search(query, limit=limit)
    threads = results.get('threads', [])
    state = load_state()
    created_by_thread = state.setdefault('created_by_thread', {})

    actions = []
    skipped_existing = []
    for thread in threads:
        thread_id = thread.get('id')
        if thread_id in created_by_thread:
            skipped_existing.append({
                'thread_id': thread_id,
                'task_id': created_by_thread[thread_id],
                'subject': thread.get('subject'),
            })
            continue
        decision = classify(thread)
        if decision:
            actions.append((thread, decision))

    if not create_mode:
        print(json.dumps({
            'mode': 'dry-run',
            'query': query,
            'account': WORK_GMAIL,
            'matches': [
                {
                    'thread_id': t.get('id'),
                    'from': t.get('from'),
                    'subject': t.get('subject'),
                    'project_id': d['project_id'],
                    'task_content': d['content'],
                    'reason': d['reason'],
                }
                for t, d in actions
            ],
            'skipped_existing': skipped_existing,
        }, indent=2))
        return

    token = load_todoist_token()
    created = []
    for thread, decision in actions:
        desc = (
            f"From: {thread.get('from')}\n"
            f"Date: {thread.get('date')}\n"
            f"Gmail thread id: {thread.get('id')}\n"
            f"Reason: {decision['reason']}"
        )
        task = create_todoist_task(token, decision['content'], decision['project_id'], desc)
        task_id = task.get('id')
        created_by_thread[thread.get('id')] = task_id
        created.append({
            'thread_id': thread.get('id'),
            'task_id': task_id,
            'content': task.get('content'),
            'reason': decision['reason'],
        })

    save_state(state)
    print(json.dumps({
        'mode': 'create',
        'query': query,
        'account': WORK_GMAIL,
        'created': created,
        'skipped_existing': skipped_existing,
    }, indent=2))


if __name__ == '__main__':
    try:
        main()
    except subprocess.TimeoutExpired:
        print(json.dumps({'error': 'gog command timed out'}), file=sys.stderr)
        sys.exit(2)
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='replace')
        print(json.dumps({'error': f'Todoist HTTP {e.code}', 'body': body[:1000]}), file=sys.stderr)
        sys.exit(3)
    except Exception as e:
        print(json.dumps({'error': str(e)}), file=sys.stderr)
        sys.exit(1)
