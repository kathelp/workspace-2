#!/bin/bash

set -euo pipefail

# Obsidian Workspace Sync
# Syncs workspace markdown files to the "Kat Workspace" folder in the Obsidian vault.
# Direction is one-way: workspace -> Obsidian.

WORKSPACE_DIR="/Users/kat/.openclaw/workspace"
OBSIDIAN_VAULT="/Users/kat/Documents/gsync"
KAT_WORKSPACE_DIR="$OBSIDIAN_VAULT/Kat Workspace"

mkdir -p "$KAT_WORKSPACE_DIR"

echo "Starting Obsidian Workspace Sync..."

# Remove files in Obsidian that no longer exist in workspace.
# Limit cleanup to markdown files inside Kat Workspace only.
find "$KAT_WORKSPACE_DIR" -type f \( -name "*.md" -o -name "*.markdown" \) | while read -r dest; do
    rel_path="${dest#$KAT_WORKSPACE_DIR/}"
    src_md="$WORKSPACE_DIR/$rel_path"
    if [ ! -f "$src_md" ]; then
        rm -f "$dest"
        echo "  - Removed stale: $rel_path"
    fi
done

# Copy markdown files from workspace to Obsidian, excluding local/runtime clutter.
find "$WORKSPACE_DIR" -type f \( -name "*.md" -o -name "*.markdown" \) \
    -not -path "$WORKSPACE_DIR/.git/*" \
    -not -path "$WORKSPACE_DIR/.openclaw/*" \
    -not -path "$WORKSPACE_DIR/support-agent/*" \
    -not -path "$WORKSPACE_DIR/scripts/*" | while read -r file; do
    rel_path="${file#$WORKSPACE_DIR/}"
    dest_file="$KAT_WORKSPACE_DIR/$rel_path"
    dest_dir="$(dirname "$dest_file")"

    mkdir -p "$dest_dir"
    cp "$file" "$dest_file"
    echo "  + Synced: $rel_path"
done

echo "Obsidian Workspace Sync completed successfully."
echo "Workspace location: $KAT_WORKSPACE_DIR"
