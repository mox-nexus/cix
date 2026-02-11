#!/usr/bin/env bash
# Hook: PreToolUse (Bash) — plugin version check on git commit
set -euo pipefail

input=$(cat)

# Only trigger on git commit
command=$(echo "$input" | jq -r '.tool_input.command // ""')
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

# Build context: versions for each changed plugin
context="STAGED PLUGIN CHANGES:\n"
while IFS= read -r plugin; do
  pj="$PROJECT_DIR/plugins/$plugin/.claude-plugin/plugin.json"
  [[ -f "$pj" ]] || continue

  pj_ver=$(jq -r '.version' "$pj" 2>/dev/null || echo "?")
  mp_ver=$(jq -r --arg n "$plugin" '.plugins[] | select(.name == $n) | .version' "$MARKETPLACE" 2>/dev/null || echo "?")
  pj_staged=$(echo "$staged" | grep -c "^plugins/$plugin/.claude-plugin/plugin.json$" || true)
  mp_staged=$(echo "$staged" | grep -c "^.claude-plugin/marketplace.json$" || true)
  files=$(echo "$staged" | grep "^plugins/$plugin/" || true)

  context+="\\n--- $plugin ---\\n"
  context+="plugin.json version: $pj_ver (staged: $( [[ $pj_staged -gt 0 ]] && echo yes || echo no ))\\n"
  context+="marketplace.json version: $mp_ver (staged: $( [[ $mp_staged -gt 0 ]] && echo yes || echo no ))\\n"
  context+="changed files:\\n$files\\n"
done <<< "$changed_plugins"

# Output: context + policy
policy=$(cat "$HOOK_DIR/check-plugin-versions.md")
printf '{"systemMessage":"%s\\n\\n%s"}' "$context" "$policy"
