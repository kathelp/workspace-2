#!/usr/bin/env python3
import json
import os
import re
import subprocess
import urllib.request
from collections import defaultdict
from pathlib import Path
from datetime import datetime, timedelta

WORKSPACE = Path('/Users/kat/.openclaw/workspace')
ACCOUNT = 'garrett@launchlabs.ai'
GOG_BIN = os.environ.get('GOG_BIN', '/opt/homebrew/bin/gog')
OPENCLAW_BIN = os.environ.get('OPENCLAW_BIN', '/opt/homebrew/bin/openclaw')
STATE_DIR = WORKSPACE / '.openclaw' / 'state'
STATE_DIR.mkdir(parents=True, exist_ok=True)
DIGEST_STATE = STATE_DIR / 'gmail-digest-state.json'
TODO_PROJECT_ID = '6g7Mg937PG4P9g6V'
TODOIST_API_URL = 'https://api.todoist.com/api/v1/tasks'
CALENDAR_ID = 'primary'

FINANCE_ROUTINE_LABEL = 'kat/finance-routine'
READ_LATER_LABEL = 'kat/read-later'
REVIEWED_LABEL = 'kat/reviewed'
TODO_LABEL = 'kat/todo-created'
DAILY_DIGESTS_CHANNEL_ID = '1491060915385405441'

FINANCE_ROUTINE_SENDERS = {
    'hello@mercury.com', 'businessservices@intuit.com', 'quickbooks@notification.intuit.com',
    'notifications@stripe.com', 'notifications@airmail.pilot.com', 'support@mailjet.com',
    'invoices@mailjet.com', 'service@paypal.com', 'mercury@investordelivery.com',
    'no-reply@accrue401k.com', 'noreply@intuit.com', 'workspace-noreply@google.com',
    'noreply@zenbusiness.com'
}

READ_LATER_SENDERS = {
    'donotreply@alerts.airbrake.io', 'hello@theinformation.com', 'noreply@trustmineral.com',
    'hello@ollama.com', 'no-reply@email.claude.com', 'noreply@glassdoor.com',
    'replyto@email.microsoft.com', 'team@mail.cursor.com', 'mariano@trycomp.ai',
    'coursera@m.learn.coursera.org', 'steve@automotive.ventures', 'feedback@slack.com',
    'hello@nubest.com'
}

def gog(*args):
    cmd = ['env', f'GOG_ACCOUNT={ACCOUNT}', GOG_BIN, *args, '--no-input']
    return subprocess.check_output(cmd, text=True)

def extract_email(sender):
    sender = (sender or '').strip().lower()
    m = re.search(r'<([^>]+)>', sender)
    return m.group(1).lower() if m else sender

def search_messages(query, max_items=200):
    raw = gog('gmail', 'messages', 'search', query, '--max', str(max_items), '--json')
    data = json.loads(raw)
    return data.get('messages', [])

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

def load_state():
    if not DIGEST_STATE.exists():
        return {'last_seen': {}}
    try:
        return json.loads(DIGEST_STATE.read_text())
    except Exception:
        return {'last_seen': {}}

def save_state(state):
    DIGEST_STATE.write_text(json.dumps(state, indent=2) + '\n')

def load_todoist_token():
    todoist_env = WORKSPACE / '.env.todoist'
    if todoist_env.exists():
        for line in todoist_env.read_text().splitlines():
            if line.startswith('TODOIST_API_TOKEN='):
                return line.split('=', 1)[1].strip()
    token = os.environ.get('TODOIST_API_TOKEN')
    if token:
        return token
    return None

def fetch_todoist_tasks(token):
    if not token:
        return []
    req = urllib.request.Request(
        TODOIST_API_URL,
        headers={'Authorization': f'Bearer {token}'},
        method='GET'
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    return data.get('results', []) if isinstance(data, dict) else data

def fetch_upcoming_events(hours=48, max_items=20):
    now = datetime.now().astimezone()
    end = now + timedelta(hours=hours)
    raw = gog(
        'calendar', 'events', CALENDAR_ID,
        '--from', now.isoformat(),
        '--to', end.isoformat(),
        '--json'
    )
    data = json.loads(raw)
    events = data.get('events', []) if isinstance(data, dict) else data

    filtered = []
    for event in events:
        start = (event.get('start') or {}).get('dateTime')
        end_time = (event.get('end') or {}).get('dateTime')
        if not start or not end_time:
            continue
        attendees = event.get('attendees') or []
        self_status = None
        for attendee in attendees:
            if attendee.get('self'):
                self_status = attendee.get('responseStatus')
                break
        if self_status == 'declined':
            continue
        filtered.append(event)

    def event_start(event):
        return (event.get('start') or {}).get('dateTime', '')

    filtered.sort(key=event_start)
    return filtered[:max_items]

def send_discord_digest(text):
    cmd = [
        OPENCLAW_BIN, 'message', 'send',
        '--channel', 'discord',
        '--target', f'channel:{DAILY_DIGESTS_CHANNEL_ID}',
        '--message', text,
        '--json',
    ]
    return subprocess.check_output(cmd, text=True)

def analyze_inbox():
    """Find genuinely actionable inbox items that need a response or decision."""
    unprocessed = search_messages('in:inbox -label:kat/reviewed -label:kat/todo-created newer_than:7d', max_items=100)
    
    actionable = []
    routine_noise = []
    
    for msg in unprocessed:
        sender_email = extract_email(msg.get('from'))
        subject = (msg.get('subject') or '').strip()
        
        # Skip obvious noise
        if sender_email in FINANCE_ROUTINE_SENDERS or sender_email in READ_LATER_SENDERS:
            routine_noise.append(msg)
            continue
            
        # High priority signals
        is_banyan = sender_email.endswith('@banyansoftware.com')
        is_internal = sender_email.endswith('@launchlabs.ai')
        is_doc_comment = sender_email == 'comments-noreply@docs.google.com'
        
        # Check if it's actually from a person needing response
        is_person = '@' in sender_email and not any(x in sender_email for x in [
            'noreply', 'no-reply', 'donotreply', 'notification', 'alert', 'support@'
        ])
        
        has_question = any(x in subject.lower() for x in ['?', 'question', 'thoughts', 'opinion'])
        has_action = any(x in subject.lower() for x in ['action', 'review', 'approve', 'sign', 'decision'])
        
        if is_banyan or is_doc_comment or (is_person and (has_question or has_action)):
            actionable.append(msg)
    
    return actionable, routine_noise

def analyze_sent_mail():
    """Find threads where you sent something but haven't heard back."""
    sent_recent = search_messages('in:sent -label:kat/reviewed newer_than:7d', max_items=50)
    
    awaiting_reply = []
    for msg in sent_recent:
        thread_id = msg.get('threadId') or msg.get('id')
        # Check if there are any newer inbox messages in this thread
        thread_msgs = search_messages(f'in:inbox thread:{thread_id}', max_items=10)
        if not thread_msgs:
            # You sent something, no reply yet
            days_ago = (datetime.now() - datetime.fromisoformat(msg.get('date'))).days if msg.get('date') else 0
            if days_ago >= 2:  # Only flag if 2+ days old
                awaiting_reply.append(msg)
    
    return awaiting_reply

def analyze_calendar(events):
    """Extract calendar insights that need prep or action."""
    now = datetime.now().astimezone()
    insights = []
    
    # Events in next 3 hours that need immediate prep
    soon_threshold = now + timedelta(hours=3)
    
    # Events tomorrow that need prep today
    tomorrow_start = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0)
    tomorrow_end = tomorrow_start + timedelta(days=1)
    
    for event in events:
        start = datetime.fromisoformat(event['start']['dateTime'])
        summary = event.get('summary', '(Untitled)')
        
        # Prep-heavy meetings
        needs_prep = any(x in summary.lower() for x in [
            'review', 'demo', 'presentation', 'planning', 'quarterly', 'board'
        ])
        
        # One-on-ones and leadership meetings
        is_important = any(x in summary.lower() for x in [
            'leadership', 'scott', 'tristan', 'banyan', '1:1', 'weekly'
        ])
        
        if start < soon_threshold:
            insights.append({
                'event': event,
                'urgency': 'immediate',
                'note': f"Starting soon - {summary}"
            })
        elif tomorrow_start <= start < tomorrow_end and (needs_prep or is_important):
            insights.append({
                'event': event,
                'urgency': 'tomorrow',
                'note': f"Tomorrow - {summary}" + (" (needs prep)" if needs_prep else "")
            })
    
    return insights

def analyze_todoist(tasks):
    """Find overdue and urgent tasks."""
    now = datetime.now()
    overdue = []
    due_soon = []
    
    for task in tasks:
        if str(task.get('project_id')) != TODO_PROJECT_ID:
            continue
            
        due = task.get('due')
        if not due:
            continue
            
        due_str = due.get('date')
        if not due_str:
            continue
        
        try:
            due_date = datetime.fromisoformat(due_str.replace('Z', '+00:00'))
            if due_date.tzinfo is None:
                due_date = due_date.replace(tzinfo=now.astimezone().tzinfo)
            
            if due_date < now:
                overdue.append(task)
            elif due_date < now + timedelta(days=1):
                due_soon.append(task)
        except:
            pass
    
    return overdue, due_soon

def build_actionable_digest():
    """Build a digest focused on what Garrett should actually do."""
    state = load_state()
    
    # Auto-label routine noise
    unlabeled = search_messages('in:inbox -label:kat/reviewed newer_than:14d', max_items=200)
    for msg in unlabeled:
        sender_email = extract_email(msg.get('from'))
        thread_id = msg.get('threadId') or msg.get('id')
        
        if sender_email in FINANCE_ROUTINE_SENDERS:
            add_label(thread_id, FINANCE_ROUTINE_LABEL)
            add_label(thread_id, REVIEWED_LABEL)
        elif sender_email in READ_LATER_SENDERS:
            add_label(thread_id, READ_LATER_LABEL)
            add_label(thread_id, REVIEWED_LABEL)
    
    # Gather intelligence
    actionable_inbox, _ = analyze_inbox()
    awaiting_reply = analyze_sent_mail()
    events = fetch_upcoming_events(hours=48, max_items=20)
    calendar_insights = analyze_calendar(events)
    
    todoist_token = load_todoist_token()
    todoist_tasks = fetch_todoist_tasks(todoist_token)
    overdue_tasks, due_soon_tasks = analyze_todoist(todoist_tasks)
    
    # Build digest
    lines = []
    now = datetime.now()
    time_label = "morning" if now.hour < 12 else "afternoon" if now.hour < 17 else "evening"
    lines.append(f"**{time_label.capitalize()} digest** - {now.strftime('%a %b %-d, %-I:%M %p')}")
    lines.append("")
    
    action_count = 0
    
    # 1. Immediate actions (next 3 hours)
    immediate_calendar = [i for i in calendar_insights if i['urgency'] == 'immediate']
    if immediate_calendar:
        lines.append("**Immediate (next 3h)**")
        for insight in immediate_calendar:
            event = insight['event']
            start = datetime.fromisoformat(event['start']['dateTime'])
            lines.append(f"- {start.strftime('%-I:%M %p')}: {event.get('summary')}")
            action_count += 1
        lines.append("")
    
    # 2. Overdue tasks
    if overdue_tasks:
        lines.append("**Overdue tasks**")
        for task in overdue_tasks[:5]:
            lines.append(f"- {task.get('content')}")
            action_count += 1
        lines.append("")
    
    # 3. Inbox items needing response/decision
    if actionable_inbox:
        lines.append("**Inbox needs response**")
        for msg in actionable_inbox[:8]:
            sender = msg.get('from', '').split('<')[0].strip() or extract_email(msg.get('from'))
            subject = msg.get('subject', '(no subject)')
            thread_id = msg.get('threadId') or msg.get('id')
            link = f"https://mail.google.com/mail/u/0/#inbox/{thread_id}"
            lines.append(f"- {subject} (from {sender})")
            lines.append(f"  {link}")
            action_count += 1
        lines.append("")
    
    # 4. Sent mail awaiting reply (2+ days old)
    if awaiting_reply:
        lines.append("**Sent, no reply yet (2+ days)**")
        for msg in awaiting_reply[:5]:
            to_addr = msg.get('to', '').split('<')[0].strip() or extract_email(msg.get('to', ''))
            subject = msg.get('subject', '(no subject)')
            days_ago = (datetime.now() - datetime.fromisoformat(msg.get('date'))).days if msg.get('date') else 0
            lines.append(f"- {subject} → {to_addr} ({days_ago}d ago)")
            action_count += 1
        lines.append("")
    
    # 5. Tomorrow prep
    tomorrow_calendar = [i for i in calendar_insights if i['urgency'] == 'tomorrow']
    if tomorrow_calendar:
        lines.append("**Tomorrow - prep today**")
        for insight in tomorrow_calendar:
            event = insight['event']
            start = datetime.fromisoformat(event['start']['dateTime'])
            lines.append(f"- {start.strftime('%-I:%M %p')}: {insight['note']}")
            action_count += 1
        lines.append("")
    
    # 6. Tasks due soon
    if due_soon_tasks:
        lines.append("**Due in next 24h**")
        for task in due_soon_tasks[:5]:
            lines.append(f"- {task.get('content')}")
            action_count += 1
        lines.append("")
    
    # 7. Upcoming calendar (next 48h, not already mentioned)
    mentioned_ids = {i['event']['id'] for i in immediate_calendar + tomorrow_calendar}
    remaining_events = [e for e in events if e['id'] not in mentioned_ids]
    
    if remaining_events:
        lines.append("**Upcoming (next 48h)**")
        for event in remaining_events[:8]:
            start = datetime.fromisoformat(event['start']['dateTime'])
            day_label = "Today" if start.date() == now.date() else start.strftime('%a')
            lines.append(f"- {day_label} {start.strftime('%-I:%M %p')}: {event.get('summary')}")
        lines.append("")
    
    # Summary
    if action_count == 0:
        lines.append("No immediate actions needed. Inbox and calendar are current.")
    else:
        lines.append(f"**{action_count} items need attention.**")
    
    return '\n'.join(lines).strip() + '\n', action_count

def main():
    for label in [FINANCE_ROUTINE_LABEL, READ_LATER_LABEL, REVIEWED_LABEL]:
        ensure_label(label)
    
    digest_text, action_count = build_actionable_digest()
    
    state = load_state()
    state['last_run'] = datetime.now().isoformat()
    state['last_action_count'] = action_count
    save_state(state)
    
    send_result = None
    send_error = None
    try:
        send_result = json.loads(send_discord_digest(digest_text))
    except Exception as exc:
        send_error = str(exc)
    
    print(json.dumps({
        'target_channel_id': DAILY_DIGESTS_CHANNEL_ID,
        'digest_text': digest_text,
        'action_count': action_count,
        'discord_send_result': send_result,
        'discord_send_error': send_error,
    }, indent=2))

if __name__ == '__main__':
    main()
