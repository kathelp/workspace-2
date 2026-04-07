#!/bin/bash

set -euo pipefail

WORKSPACE_DIR="/Users/kat/.openclaw/workspace"
LOG_DIR="$WORKSPACE_DIR/logs"
DATE="$(date +%F)"
TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S %Z')"
MEMORY_DIR="$WORKSPACE_DIR/memory"
TODAY_NOTE="$MEMORY_DIR/$DATE.md"
YESTERDAY_NOTE="$MEMORY_DIR/$(date -v-1d +%F).md"
MEMORY_INDEX="$WORKSPACE_DIR/MEMORY.md"
LOG_FILE="$LOG_DIR/daily-memory-sync.log"
OBSIDIAN_SYNC_SCRIPT="$WORKSPACE_DIR/scripts/obsidian-sync.sh"
TMP_REVIEW="$(mktemp)"

cleanup() {
  rm -f "$TMP_REVIEW"
}
trap cleanup EXIT

mkdir -p "$MEMORY_DIR" "$LOG_DIR"

exec >> "$LOG_FILE" 2>&1

echo "[$TIMESTAMP] Starting daily memory sync"

cd "$WORKSPACE_DIR"

if [ ! -f "$TODAY_NOTE" ]; then
  {
    echo "# $DATE - Daily Notes"
    echo
  } > "$TODAY_NOTE"
  echo "[$TIMESTAMP] Created daily note: $TODAY_NOTE"
fi

python3 - <<'PY' "$TODAY_NOTE" "$YESTERDAY_NOTE" "$TMP_REVIEW" "$TIMESTAMP"
import pathlib
import re
import sys


def bullets_from(path_str, limit=8):
    path = pathlib.Path(path_str)
    if not path.exists():
        return []
    lines = []
    for raw in path.read_text().splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith('#'):
            continue
        if line == '## Daily Memory Review':
            break
        if line.startswith('Review run:') or line.startswith('Files checked:') or line.startswith('Recent highlights:'):
            continue
        if line.startswith('- Last automated daily memory review:'):
            continue
        line = re.sub(r'^[-*]\s*', '', line).strip()
        if not line:
            continue
        lines.append(line)
        if len(lines) >= limit:
            break
    return lines


today_path = pathlib.Path(sys.argv[1])
yesterday_path = pathlib.Path(sys.argv[2])
out_path = pathlib.Path(sys.argv[3])
timestamp = sys.argv[4]

yesterday = bullets_from(yesterday_path, limit=6)
today = bullets_from(today_path, limit=6)

review = []
review.append(f'Review run: {timestamp}')
review.append('')
review.append('Files checked:')
if yesterday_path.exists():
    review.append(f'- {yesterday_path.name}')
review.append(f'- {today_path.name}')
review.append(f'- MEMORY.md')
review.append('')
review.append('Recent highlights:')

highlights = []
if yesterday:
    highlights.append('From yesterday:')
    highlights.extend(f'- {line}' for line in yesterday)
if today:
    if highlights:
        highlights.append('')
    highlights.append('From today:')
    highlights.extend(f'- {line}' for line in today)

if not highlights:
    highlights.append('- No substantive notes yet. Review ran and sync still completed.')

review.extend(highlights)
out_path.write_text('\n'.join(review) + '\n')
PY

python3 - <<'PY' "$TODAY_NOTE" "$TMP_REVIEW"
import pathlib
import sys

today_path = pathlib.Path(sys.argv[1])
review_path = pathlib.Path(sys.argv[2])
review_text = review_path.read_text().strip()
section_header = '## Daily Memory Review\n'
entry = section_header + review_text + '\n'
text = today_path.read_text() if today_path.exists() else ''
if section_header in text:
    before, _sep, _after = text.partition(section_header)
    today_path.write_text(before.rstrip() + '\n\n' + entry + '\n')
else:
    sep = '' if text.endswith('\n\n') or not text else '\n'
    today_path.write_text(text + sep + entry + '\n')
PY

echo "[$TIMESTAMP] Updated Daily Memory Review section"

python3 - <<'PY' "$MEMORY_INDEX" "$DATE" "$TIMESTAMP"
import pathlib
import sys

memory_path = pathlib.Path(sys.argv[1])
date = sys.argv[2]
timestamp = sys.argv[3]
line = f"- Last automated daily memory review: {date} ({timestamp})"
text = memory_path.read_text()
marker = "## Notes\n"
if marker in text:
    head, sep, tail = text.partition(marker)
    tail_lines = tail.splitlines()
    if tail_lines and tail_lines[0].startswith("- Last automated daily memory review:"):
        tail_lines[0] = line
    else:
        tail_lines.insert(0, line)
    memory_path.write_text(head + sep + "\n".join(tail_lines) + "\n")
PY

echo "[$TIMESTAMP] Updated MEMORY.md review marker"

"$OBSIDIAN_SYNC_SCRIPT"

echo "[$TIMESTAMP] Obsidian sync complete"

if ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git ls-files --others --exclude-standard)" ]; then
  git add -A
  if git commit -m "Daily memory review and sync: $DATE"; then
    echo "[$TIMESTAMP] Commit created"
  else
    echo "[$TIMESTAMP] Nothing new to commit after add"
  fi
  git push
  echo "[$TIMESTAMP] Git sync complete"
else
  echo "[$TIMESTAMP] No git changes to commit"
fi

echo "[$TIMESTAMP] Finished daily memory sync"
