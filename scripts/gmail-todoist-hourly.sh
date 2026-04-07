#!/bin/bash
set -euo pipefail

cd /Users/kat/.openclaw/workspace
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
set -a
source .env
set +a
export GOG_BIN="${GOG_BIN:-/opt/homebrew/bin/gog}"

QUERY='in:inbox -label:kat/reviewed -label:kat/todo-created newer_than:14d'
LOG_DIR="$HOME/.openclaw/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/gmail-todoist-hourly.log"

{
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] hourly gmail triage start"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] PATH=$PATH"
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] GOG_BIN=$GOG_BIN"
  ./scripts/gmail-todoist-triage.sh "$QUERY" create 25
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] hourly gmail triage end"
} >> "$LOG_FILE" 2>&1
