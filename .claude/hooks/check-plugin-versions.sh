#!/usr/bin/env bash
# Hook: PreToolUse (Bash) — plugin version check on git commit
set -uo pipefail

# Require jq — exit silently if unavailable
command -v jq &>/dev/null || exit 0

input=$(cat)

# Only trigger on git commit
command=$(echo "$input" | jq -r '.tool_input.command // ""' 2>/dev/null) || exit 0
[[ "$command" =~ git\ commit ]] || exit 0

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
MARKETPLACE="$PROJECT_DIR/.claude-plugin/marketplace.json"
HOOK_DIR="$(cd "$(dirname "$0")" && pwd)"

# Gather staged files
staged=$(cd "$PROJECT_DIR" && git diff --cached --name-only 2>/dev/null || true)
[[ -n "$staged" ]] || exit 0

# Find plugins with staged changes
changed_plugins=$(echo "$staged" | grep '^plugins/' | cut -d/ -f2 | sort -u || true)
[[ -n "$changed_plugins" ]] || exit 0

# Build context string
context="STAGED PLUGIN CHANGES:"
while IFS= read -r plugin; do
  pj="$PROJECT_DIR/plugins/$plugin/.claude-plugin/plugin.json"
  [[ -f "$pj" ]] || continue

  pj_ver=$(jq -r '.version' "$pj" 2>/dev/null || echo "?")
  mp_ver=$(jq -r --arg n "$plugin" '.plugins[] | select(.name == $n) | .version' "$MARKETPLACE" 2>/dev/null || echo "?")
  pj_staged=$(echo "$staged" | grep -c "^plugins/$plugin/.claude-plugin/plugin.json$" || echo 0)
  mp_staged=$(echo "$staged" | grep -c "^.claude-plugin/marketplace.json$" || echo 0)
  files=$(echo "$staged" | grep "^plugins/$plugin/" || true)

  context+="

--- $plugin ---
plugin.json version: $pj_ver (staged: $( [[ $pj_staged -gt 0 ]] && echo yes || echo no ))
marketplace.json version: $mp_ver (staged: $( [[ $mp_staged -gt 0 ]] && echo yes || echo no ))
changed files:
$files"
done <<< "$changed_plugins"

policy=$(cat "$HOOK_DIR/check-plugin-versions.md")
message="$context

$policy"

# Use jq to produce correctly escaped JSON
jq -n --arg msg "$message" '{"systemMessage": $msg}'
