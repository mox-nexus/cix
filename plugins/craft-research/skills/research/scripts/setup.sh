#!/usr/bin/env bash
set -euo pipefail

# Scaffold a craft-research workspace.
# Usage: ./setup.sh [workspace-path]
# Default: .research/ in the current directory.

WORKSPACE="${1:-.research}"

if [ -d "$WORKSPACE" ]; then
  echo "Workspace already exists: $WORKSPACE"
  echo "Remove it first or choose a different path."
  exit 1
fi

# Create workspace with all subdirectories
mkdir -p "$WORKSPACE"/{sources,extraction,verification,synthesis,audit}

# Add workspace to .gitignore if not already present
GITIGNORE=".gitignore"
ENTRY="$(basename "$WORKSPACE")/"

if [ -f "$GITIGNORE" ]; then
  if ! grep -qF "$ENTRY" "$GITIGNORE"; then
    echo "" >> "$GITIGNORE"
    echo "# Research workspace (working artifacts)" >> "$GITIGNORE"
    echo "$ENTRY" >> "$GITIGNORE"
  fi
else
  echo "# Research workspace (working artifacts)" > "$GITIGNORE"
  echo "$ENTRY" >> "$GITIGNORE"
fi

echo "Workspace created: $WORKSPACE"
echo "  Added $ENTRY to .gitignore"
echo "  Next: write scope.md with your research questions"
