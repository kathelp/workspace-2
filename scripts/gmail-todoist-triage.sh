#!/bin/bash
set -euo pipefail

WORKSPACE="/Users/kat/.openclaw/workspace"
TODOIST_ENV="$WORKSPACE/.env.todoist"
ACCOUNT="garrett@launchlabs.ai"
QUERY="${1:-in:inbox -label:kat/reviewed -label:kat/todo-created newer_than:14d}"
MODE="${2:-dry-run}"
MAX="${3:-25}"
MAILBOX_MODE="${4:-inbox}"

TMP_GMAIL="$(mktemp)"
trap 'rm -f "$TMP_GMAIL"' EXIT

GOG_BIN="${GOG_BIN:-$(command -v gog || true)}"
if [[ -z "$GOG_BIN" ]]; then
  echo "gog not found in PATH=$PATH" >&2
  exit 127
fi

if [[ "$MAILBOX_MODE" == "sent" ]]; then
  env GOG_ACCOUNT="$ACCOUNT" "$GOG_BIN" gmail messages search "$QUERY" --max "$MAX" --json --no-input > "$TMP_GMAIL"
else
  env GOG_ACCOUNT="$ACCOUNT" "$GOG_BIN" gmail search "$QUERY" --max "$MAX" --json --no-input > "$TMP_GMAIL"
fi

python3 - "$TMP_GMAIL" "$TODOIST_ENV" "$MODE" "$MAILBOX_MODE" <<'PY'
import json, re, subprocess, sys, urllib.request
from pathlib import Path

gmail_path, todoist_env_path, mode, mailbox_mode = sys.argv[1:5]
ACCOUNT = 'garrett@launchlabs.ai'
GOG_BIN = '/opt/homebrew/bin/gog'
WORK_PROJECT_ID = '6g7Mg937PG4P9g6V'
FOLLOWUP_PROJECT_ID = '6g7Mg93mCQHHwXmx'
REVIEWED_LABEL = 'kat/reviewed'
TODO_LABEL = 'kat/todo-created'

DIRECT_PEOPLE = [
    'tjordan@banyansoftware.com', 'scastiglione@banyansoftware.com', 'sburgess@banyansoftware.com',
    'mmorgan@launchlabs.ai', 'eric@launchlabs.ai', 'holly@launchlabs.ai', 'matthew@launchlabs.ai',
    'emily@launchlabs.ai', 'harris@launchlabs.ai', 'jkosobucki@morganautogroup.com',
]

FINANCE_ROUTINE_SENDERS = [
    'hello@mercury.com', 'businessservices@intuit.com', 'quickbooks@notification.intuit.com',
    'notifications@stripe.com', 'notifications@airmail.pilot.com', 'support@mailjet.com',
    'invoices@mailjet.com', 'service@paypal.com', 'mercury@investordelivery.com',
    'no-reply@accrue401k.com', 'noreply@intuit.com', 'workspace-noreply@google.com',
    'noreply@zenbusiness.com'
]

READ_LATER_SENDERS = [
    'hello@theinformation.com', 'noreply@trustmineral.com', 'hello@ollama.com',
    'no-reply@email.claude.com', 'noreply@glassdoor.com', 'replyto@email.microsoft.com',
    'team@mail.cursor.com', 'mariano@trycomp.ai', 'coursera@m.learn.coursera.org',
    'steve@automotive.ventures', 'feedback@slack.com', 'hello@nubest.com',
    'donotreply@alerts.airbrake.io'
]

COLD_SOLICITATION_SENDERS = [
    'hit-reply@linkedin.com', 'mariano@trycomp.ai', 'replyto@email.microsoft.com',
    'team@mail.cursor.com', 'hello@ollama.com', 'no-reply@email.claude.com'
]

COLD_SOLICITATION_HINTS = [
    'quick question', 'bottleneck checklist', 'quick thought', 'opportunity', 'workshop',
    'register now', 'hiring', 'meet the new', 'power your team', 'scale and centralize',
    'leverage the ai', 'selling to ai agents'
]

RELATIONSHIP_HINTS = [
    'rsvp', 'invitation', 'celebration', 'quick question', 'question for you',
    'can you', 'need your input', 'awaiting your response', 'please respond', 'please review'
]

HARD_EXCEPTION_HINTS = [
    'fraud', 'suspicious login', 'account locked', 'service interruption', 'failed payment'
]

SCORING_DOC_HINTS = ['scorecard', 'earnout', 'earn-out']

results = json.loads(Path(gmail_path).read_text())

def gog(*args):
    cmd = ['env', f'GOG_ACCOUNT={ACCOUNT}', GOG_BIN, *args, '--no-input']
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

def archive_thread(thread_id):
    try:
        gog('gmail', 'labels', 'modify', thread_id, '--remove', 'INBOX')
    except subprocess.CalledProcessError:
        pass

def iter_items(results):
    if mailbox_mode == 'sent':
        return results.get('messages', [])
    return results.get('threads', [])

def item_id(item):
    return item.get('threadId') if mailbox_mode == 'sent' else item.get('id')

def extract_email(sender):
    sender = (sender or '').strip().lower()
    m = re.search(r'<([^>]+)>', sender)
    return m.group(1).lower() if m else sender

def classify(item):
    subject = (item.get('subject') or '').strip()
    subject_l = subject.lower()
    sender = (item.get('from') or '').strip()
    sender_email = extract_email(sender)
    labels = [l.lower() for l in (item.get('labels') or [])]

    if mailbox_mode == 'sent':
        return None

    if sender_email in COLD_SOLICITATION_SENDERS or any(h in subject_l for h in COLD_SOLICITATION_HINTS):
        return {
            'project_id': None,
            'content': None,
            'reason': 'cold solicitation',
            'lane': 'archive',
        }

    if sender_email in FINANCE_ROUTINE_SENDERS:
        if any(h in subject_l for h in HARD_EXCEPTION_HINTS):
            return {
                'project_id': WORK_PROJECT_ID,
                'content': f'Review finance exception: {subject}',
                'reason': 'hard finance exception language',
                'lane': 'high-signal',
            }
        return None

    if sender_email == 'donotreply@alerts.airbrake.io':
        return None

    if sender_email in READ_LATER_SENDERS or 'category_promotions' in labels:
        return None

    if sender_email.endswith('@banyansoftware.com'):
        return {
            'project_id': WORK_PROJECT_ID,
            'content': f'Review Banyan email: {subject}',
            'reason': 'banyan sender',
            'lane': 'high-signal',
        }

    if sender_email == 'comments-noreply@docs.google.com' and any(h in subject_l for h in SCORING_DOC_HINTS):
        return {
            'project_id': WORK_PROJECT_ID,
            'content': f'Review doc comment: {subject}',
            'reason': 'scorecard or earnout doc comment',
            'lane': 'high-signal',
        }

    if sender_email in DIRECT_PEOPLE:
        return {
            'project_id': FOLLOWUP_PROJECT_ID,
            'content': f'Reply or review: {subject}',
            'reason': 'direct person / known relationship',
            'lane': 'reply-needed',
        }

    if any(h in subject_l for h in RELATIONSHIP_HINTS):
        return {
            'project_id': FOLLOWUP_PROJECT_ID,
            'content': f'Reply or review: {subject}',
            'reason': 'relationship or response language',
            'lane': 'reply-needed',
        }

    return None

matches = []
review_only = []
for item in iter_items(results):
    decision = classify(item)
    if decision:
        matches.append((item, decision))
    else:
        review_only.append(item)

ensure_label(REVIEWED_LABEL)
ensure_label(TODO_LABEL)

if mode != 'create':
    print(json.dumps({
        'mode': 'dry-run',
        'mailbox_mode': mailbox_mode,
        'matches': [
            {
                'thread_id': item_id(t),
                'from': t.get('from'),
                'subject': t.get('subject'),
                'project_id': d['project_id'],
                'task_content': d['content'],
                'reason': d['reason'],
                'lane': d.get('lane'),
            }
            for t, d in matches
        ],
        'review_only': [
            {
                'thread_id': item_id(t),
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
for item, decision in matches:
    thread_id = item_id(item)

    if decision.get('lane') == 'archive':
        archive_thread(thread_id)
        add_label(thread_id, REVIEWED_LABEL)
        created.append({
            'thread_id': thread_id,
            'task_id': None,
            'content': None,
            'reason': decision['reason'],
            'lane': decision.get('lane'),
        })
        continue

    desc = (
        f"From: {item.get('from')}\n"
        f"Subject: {item.get('subject')}\n"
        f"Date: {item.get('date')}\n"
        f"Lane: {decision.get('lane')}\n"
        f"Gmail thread id: {thread_id}\n"
        f"Gmail thread: https://mail.google.com/mail/u/0/#inbox/{thread_id}\n"
        f"Reason: {decision['reason']}"
    )
    task = create_task(decision['content'], decision['project_id'], desc)
    add_label(thread_id, TODO_LABEL)
    add_label(thread_id, REVIEWED_LABEL)
    created.append({
        'thread_id': thread_id,
        'task_id': task.get('id'),
        'content': task.get('content'),
        'reason': decision['reason'],
        'lane': decision.get('lane'),
    })

reviewed = []
for item in review_only:
    reviewed_id = item_id(item)
    add_label(reviewed_id, REVIEWED_LABEL)
    reviewed.append(reviewed_id)

print(json.dumps({
    'mode': 'create',
    'mailbox_mode': mailbox_mode,
    'created': created,
    'reviewed_only': reviewed,
}, indent=2))
PY
