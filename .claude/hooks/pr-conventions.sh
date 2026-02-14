#!/bin/bash
# UserPromptSubmit: Inject PR conventions when user asks to create a PR
set -euo pipefail

INPUT=$(cat)
USER_PROMPT=$(echo "$INPUT" | jq -r '.user_prompt // empty')

# Only trigger on PR-related prompts
if ! echo "$USER_PROMPT" | grep -qiE '\b(pull request|PR|pr create|gh pr)\b'; then
  exit 0
fi

HOOK_DIR="$(cd "$(dirname "$0")" && pwd)"
cat "$HOOK_DIR/pr-conventions.md"
