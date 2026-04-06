#!/bin/bash
set -euo pipefail

WORKSPACE="/Users/kat/.openclaw/workspace"
TODOIST_ENV="$WORKSPACE/.env.todoist"
ACCOUNT="garrett@launchlabs.ai"
QUERY="${1:-in:inbox -label:kat/reviewed -label:kat/todo-created newer_than:14d}"
MODE="${2:-dry-run}"
MAX="${3:-25}"

TMP_GMAIL="$(mktemp)"
trap 'rm -f "$TMP_GMAIL"' EXIT

env GOG_ACCOUNT="$ACCOUNT" gog gmail search "$QUERY" --max "$MAX" --json --no-input > "$TMP_GMAIL"

python3 - "$TMP_GMAIL" "$TODOIST_ENV" "$MODE" <<'PY'
import json, subprocess, sys, urllib.request
from pathlib import Path

gmail_path, todoist_env_path, mode = sys.argv[1:4]
ACCOUNT = 'garrett@launchlabs.ai'
WORK_PROJECT_ID = '6g7Mg937PG4P9g6V'
NOISE_HINTS = [
    'newsletter', 'weekly digest', 'weekly report', 'promo', 'promotion', 'receipt',
    'statement', 'summary', 'invited you to', 'ready:', 'intel report', 'digest',
    'your api account', 'jobs alert', 'weekly', 'account statement', 'top dealership marketing service',
    'rsvp', 'celebration'
]
HIGH_SIGNAL_HINTS = [
    'action required', 'action needed', 'follow up', 'follow-up', 'question', 'review',
    'security', 'renewal', 'invoice', 'payment', 'alert', 'error', 'issue', 'warning',
    'unread registered agent documents', 'contract', 'docusign',
    'compliance filings due', 'webhook disconnected', 'scorecard'
]
REVIEWED_LABEL = 'kat/reviewed'
TODO_LABEL = 'kat/todo-created'

results = json.loads(Path(gmail_path).read_text())

def gog(*args):
    cmd = ['env', f'GOG_ACCOUNT={ACCOUNT}', 'gog', *args, '--no-input']
    return subprocess.check_output(cmd, text=True)

def ensure_label(name):
    try:
        existing = gog('gmail', 'labels', 'list', '--json')
        data = json.loads(existing)
        labels = data.get('labels') if isinstance(data, dict) else data
        labels = labels or []
        if any((label.get('name') or '').lower() == name.lower() for label in labels):
            return
        gog('gmail', 'labels', 'create', name)
    except subprocess.CalledProcessError:
        pass

def add_label(thread_id, label):
    try:
        gog('gmail', 'labels', 'modify', thread_id, '--add', label)
    except subprocess.CalledProcessError:
        pass

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
    if 'comments-noreply@docs.google.com' in sender_l and 'scorecard' in subject_l:
        return {
            'project_id': WORK_PROJECT_ID,
            'content': f'Review scorecard comment: {subject}',
            'reason': 'scorecard comment',
        }
    if 'noreply' in sender_l and not any(h in subject_l for h in HIGH_SIGNAL_HINTS):
        return None
    if any(h in subject_l for h in HIGH_SIGNAL_HINTS):
        return {
            'project_id': WORK_PROJECT_ID,
            'content': f'Email follow-up: {subject}',
            'reason': 'high-signal subject',
        }
    return None

matches = []
review_only = []
for thread in results.get('threads', []):
    decision = classify(thread)
    if decision:
        matches.append((thread, decision))
    else:
        review_only.append(thread)

ensure_label(REVIEWED_LABEL)
ensure_label(TODO_LABEL)

if mode != 'create':
    print(json.dumps({
        'mode': 'dry-run',
        'matches': [
            {
                'thread_id': t.get('id'),
                'from': t.get('from'),
                'subject': t.get('subject'),
                'project_id': d['project_id'],
                'task_content': d['content'],
                'reason': d['reason'],
            }
            for t, d in matches
        ],
        'review_only': [
            {
                'thread_id': t.get('id'),
                'from': t.get('from'),
                'subject': t.get('subject'),
            }
            for t in review_only
        ],
    }, indent=2))
    raise SystemExit(0)

token = None
for line in Path(todoist_env_path).read_text().splitlines():
    if line.startswith('TODOIST_API_TOKEN='):
        token = line.split('=',1)[1].strip()
        break
if not token:
    raise SystemExit('TODOIST_API_TOKEN not found')

def create_task(content, project_id, description):
    payload = {'content': content, 'project_id': project_id, 'description': description}
    req = urllib.request.Request(
        'https://api.todoist.com/api/v1/tasks',
        data=json.dumps(payload).encode('utf-8'),
        headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'},
        method='POST'
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)

created = []
for thread, decision in matches:
    desc = (
        f"From: {thread.get('from')}\n"
        f"Date: {thread.get('date')}\n"
        f"Gmail thread id: {thread.get('id')}\n"
        f"Reason: {decision['reason']}"
    )
    task = create_task(decision['content'], decision['project_id'], desc)
    add_label(thread.get('id'), TODO_LABEL)
    add_label(thread.get('id'), REVIEWED_LABEL)
    created.append({
        'thread_id': thread.get('id'),
        'task_id': task.get('id'),
        'content': task.get('content'),
        'reason': decision['reason'],
    })

reviewed = []
for thread in review_only:
    add_label(thread.get('id'), REVIEWED_LABEL)
    reviewed.append(thread.get('id'))

print(json.dumps({
    'mode': 'create',
    'created': created,
    'reviewed_only': reviewed,
}, indent=2))
PY
