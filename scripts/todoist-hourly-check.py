#!/usr/bin/env python3
import json
import os
import urllib.request
from pathlib import Path

WORKSPACE = Path('/Users/kat/.openclaw/workspace')
STATE_DIR = WORKSPACE / '.openclaw' / 'state'
STATE_DIR.mkdir(parents=True, exist_ok=True)
STATE_FILE = STATE_DIR / 'todoist-hourly-check.json'
TODOIST_API = 'https://api.todoist.com/api/v1'
FOR_KAT_PROJECT_ID = '6gJVwj7Vvqp7X9wF'

INSTRUCTION_HINTS = [
    'do this', 'please do this', 'handle this', 'take care of this', 'follow up',
    'reply to this', 'send this', 'look into this', 'do it'
]
REMOVE_AFTER_SEEN_HINTS = [
    'ignore this', 'ignore these', 'don\'t do this', 'do not do this', 'skip this',
    'remove this task', 'delete this task', 'close this task', 'not needed'
]

def load_token():
    env_file = WORKSPACE / '.env.todoist'
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith('TODOIST_API_TOKEN='):
                return line.split('=', 1)[1].strip()
    token = os.environ.get('TODOIST_API_TOKEN')
    if token:
        return token
    raise SystemExit('Missing TODOIST_API_TOKEN')

def api_get(path, token):
    req = urllib.request.Request(
        f'{TODOIST_API}{path}',
        headers={'Authorization': f'Bearer {token}'},
        method='GET'
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    return data.get('results', []) if isinstance(data, dict) else data

def api_delete(path, token):
    req = urllib.request.Request(
        f'{TODOIST_API}{path}',
        headers={'Authorization': f'Bearer {token}'},
        method='DELETE'
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.status

def load_state():
    if not STATE_FILE.exists():
        return {'seen_comment_ids': [], 'seen_for_kat_task_ids': []}
    try:
        return json.loads(STATE_FILE.read_text())
    except Exception:
        return {'seen_comment_ids': [], 'seen_for_kat_task_ids': []}

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2) + '\n')

def main():
    token = load_token()
    state = load_state()
    seen_comment_ids = set(state.get('seen_comment_ids', []))
    seen_for_kat_task_ids = set(state.get('seen_for_kat_task_ids', []))

    tasks = api_get('/tasks', token)

    task_by_id = {}
    for_kat_tasks = []
    new_for_kat_tasks = []
    relevant_task_ids = []

    for task in tasks:
        task_id = str(task.get('id'))
        if not task_id:
            continue
        task_by_id[task_id] = task

        if str(task.get('project_id')) == FOR_KAT_PROJECT_ID and not task.get('checked', False):
            for_kat_tasks.append(task)
            relevant_task_ids.append(task_id)
            if task_id not in seen_for_kat_task_ids:
                new_for_kat_tasks.append(task)
                seen_for_kat_task_ids.add(task_id)
            continue

        if not task.get('checked', False):
            relevant_task_ids.append(task_id)

    relevant_comments = []
    new_instruction_comments = []
    removed_tasks = []
    removed_task_ids = set()

    for task_id in relevant_task_ids:
        try:
            comments = api_get(f'/comments?task_id={task_id}&object_type=task', token)
        except Exception:
            continue

        for comment in comments:
            content = (comment.get('content') or '').strip()
            content_l = content.lower()
            comment_id = str(comment.get('id'))
            if not content:
                continue

            if any(h in content_l for h in REMOVE_AFTER_SEEN_HINTS):
                relevant_comments.append(comment)
                if task_id not in removed_task_ids and task_id in task_by_id:
                    try:
                        api_delete(f'/tasks/{task_id}', token)
                        removed_tasks.append({
                            'id': task_id,
                            'content': task_by_id[task_id].get('content'),
                            'description': task_by_id[task_id].get('description'),
                            'reason': content,
                        })
                        removed_task_ids.add(task_id)
                    except Exception:
                        pass
                if comment_id not in seen_comment_ids:
                    seen_comment_ids.add(comment_id)
                continue

            if any(h in content_l for h in INSTRUCTION_HINTS):
                relevant_comments.append(comment)
                if comment_id not in seen_comment_ids:
                    new_instruction_comments.append(comment)
                    seen_comment_ids.add(comment_id)

    state['seen_comment_ids'] = sorted(seen_comment_ids)
    state['seen_for_kat_task_ids'] = sorted(seen_for_kat_task_ids)
    save_state(state)

    print(json.dumps({
        'for_kat_open_tasks': [
            {
                'id': t.get('id'),
                'content': t.get('content'),
                'description': t.get('description'),
                'url': t.get('url')
            } for t in for_kat_tasks if str(t.get('id')) not in removed_task_ids
        ],
        'new_for_kat_tasks': [
            {
                'id': t.get('id'),
                'content': t.get('content'),
                'description': t.get('description'),
                'url': t.get('url')
            } for t in new_for_kat_tasks if str(t.get('id')) not in removed_task_ids
        ],
        'instruction_comments': [
            {
                'id': c.get('id'),
                'task_id': c.get('task_id') or c.get('item_id'),
                'content': c.get('content'),
                'posted_at': c.get('posted_at')
            } for c in relevant_comments
        ],
        'new_instruction_comments': [
            {
                'id': c.get('id'),
                'task_id': c.get('task_id') or c.get('item_id'),
                'content': c.get('content'),
                'posted_at': c.get('posted_at')
            } for c in new_instruction_comments
        ],
        'removed_tasks': removed_tasks
    }, indent=2))

if __name__ == '__main__':
    main()
