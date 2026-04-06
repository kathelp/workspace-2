#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

WORK_GMAIL = 'garrett@launchlabs.ai'
WORK_PROJECT_ID = '6g7Mg937PG4P9g6V'
FOLLOWUP_PROJECT_ID = '6g7Mg93mCQHHwXmx'
INBOX_PROJECT_ID = '6g7Mf5J6p939RxX4'

NOISE_HINTS = [
    'newsletter', 'weekly digest', 'weekly report', 'promo', 'promotion', 'receipt',
    'statement', 'summary', 'invited you to', 'ready:', 'intel report', 'digest'
]

HIGH_SIGNAL_HINTS = [
    'action required', 'action needed', 'follow up', 'follow-up', 'question', 'review',
    'security', 'renewal', 'invoice', 'payment', 'alert', 'error', 'issue', 'warning',
    'unread registered agent documents', 'contract', 'docusign', 'launch labs'
]


def load_todoist_token():
    env_file = Path('/Users/kat/.openclaw/workspace/.env.todoist')
    for line in env_file.read_text().splitlines():
        if line.startswith('TODOIST_API_TOKEN='):
            return line.split('=', 1)[1].strip()
    raise RuntimeError('TODOIST_API_TOKEN not found')


def run_gog_search(query, limit=25):
    env = os.environ.copy()
    env['GOG_ACCOUNT'] = WORK_GMAIL
    cmd = ['gog', 'gmail', 'search', query, '--max', str(limit), '--json']
    out = subprocess.check_output(cmd, env=env, text=True)
    return json.loads(out)


def classify(thread):
    subject = (thread.get('subject') or '').lower()
    sender = (thread.get('from') or '').lower()

    if any(h in subject for h in NOISE_HINTS):
        return None
    if 'noreply' in sender and not any(h in subject for h in HIGH_SIGNAL_HINTS):
        return None
    if any(h in subject for h in HIGH_SIGNAL_HINTS):
        return {
            'project_id': WORK_PROJECT_ID,
            'content': f"Email follow-up: {thread.get('subject')}",
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
    query = sys.argv[1] if len(sys.argv) > 1 else 'is:unread newer_than:2d'
    dry_run = '--create' not in sys.argv

    results = run_gog_search(query)
    threads = results.get('threads', [])
    actions = []
    for thread in threads:
        decision = classify(thread)
        if decision:
            actions.append((thread, decision))

    if dry_run:
        print(json.dumps({
            'mode': 'dry-run',
            'query': query,
            'matches': [
                {
                    'thread_id': t.get('id'),
                    'from': t.get('from'),
                    'subject': t.get('subject'),
                    'project_id': d['project_id'],
                    'task_content': d['content'],
                }
                for t, d in actions
            ]
        }, indent=2))
        return

    token = load_todoist_token()
    created = []
    for thread, decision in actions:
        desc = f"From: {thread.get('from')}\nDate: {thread.get('date')}\nGmail thread id: {thread.get('id')}"
        task = create_todoist_task(token, decision['content'], decision['project_id'], desc)
        created.append({
            'thread_id': thread.get('id'),
            'task_id': task.get('id'),
            'content': task.get('content'),
        })

    print(json.dumps({
        'mode': 'create',
        'query': query,
        'created': created,
    }, indent=2))


if __name__ == '__main__':
    main()
