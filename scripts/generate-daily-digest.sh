#!/usr/bin/env bash
set -euo pipefail

cd /Users/kat/.openclaw/workspace
set -a
source .env 2>/dev/null || true
set +a

./scripts/gmail-digest.py
