#!/usr/bin/env bash
set -euo pipefail

# Scaffold a craft-rhetoric workspace.
# Usage: ./setup.sh [workspace-path]
# Default: .rhet/ in the current directory.

WORKSPACE="${1:-.rhet}"

if [ -d "$WORKSPACE" ]; then
  echo "Workspace already exists: $WORKSPACE"
  echo "Remove it first or choose a different path."
  exit 1
fi

# Create workspace with all subdirectories
mkdir -p "$WORKSPACE"/{map,discovering,inventio,memoria,arrangement,voicing,figures,staging,evaluation}

# Add workspace to .gitignore if not already present
GITIGNORE=".gitignore"
ENTRY="$(basename "$WORKSPACE")/"

if [ -f "$GITIGNORE" ]; then
  if ! grep -qF "$ENTRY" "$GITIGNORE"; then
    echo "" >> "$GITIGNORE"
    echo "# Rhetoric workspace (working artifacts)" >> "$GITIGNORE"
    echo "$ENTRY" >> "$GITIGNORE"
  fi
else
  echo "# Rhetoric workspace (working artifacts)" > "$GITIGNORE"
  echo "$ENTRY" >> "$GITIGNORE"
fi

echo "Workspace created: $WORKSPACE"
echo "  Added $ENTRY to .gitignore"
echo "  Next: run discourse to generate ground-truth.md"
