#!/bin/bash
# UserPromptSubmit: Inject commit conventions when user asks to commit
set -euo pipefail

INPUT=$(cat)
USER_PROMPT=$(echo "$INPUT" | jq -r '.user_prompt // empty')

# Only trigger on commit-related prompts
if ! echo "$USER_PROMPT" | grep -qiE '\b(commit|git commit)\b'; then
  exit 0
fi

HOOK_DIR="$(cd "$(dirname "$0")" && pwd)"
cat "$HOOK_DIR/commit-message.md"
