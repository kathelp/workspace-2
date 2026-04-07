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

{
  echo "Review run: $TIMESTAMP"
  echo
  echo "Files checked:"
  [ -f "$YESTERDAY_NOTE" ] && echo "- $(basename "$YESTERDAY_NOTE")"
  [ -f "$TODAY_NOTE" ] && echo "- $(basename "$TODAY_NOTE")"
  echo "- $(basename "$MEMORY_INDEX")"
  echo
  echo "Recent highlights:"
  if [ -f "$YESTERDAY_NOTE" ]; then
    awk 'NF { print "- " $0; count++; if (count >= 8) exit }' "$YESTERDAY_NOTE"
  fi
  awk 'NF { print "- " $0; count++; if (count >= 8) exit }' "$TODAY_NOTE"
} > "$TMP_REVIEW"

python3 - <<'PY' "$TODAY_NOTE" "$TMP_REVIEW"
import pathlib
import sys

today_path = pathlib.Path(sys.argv[1])
review_path = pathlib.Path(sys.argv[2])
review_text = review_path.read_text()
section_header = '## Daily Memory Review\n'
entry = section_header + review_text.strip() + '\n'
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
