#!/bin/bash
# Detects incomplete refactoring after a commit
# Called by PostToolUse hook on Bash tool
# Opt-out: SKIP_REFACTOR_HOOKS=1
#
# After a git commit that renames files, greps the repo for old names.
# Research: CodeScene — 63% of AI refactoring breaks code
# Research: GitClear — refactoring down 60% in AI-assisted codebases

if [[ "${SKIP_REFACTOR_HOOKS:-}" == "1" ]]; then
    echo '{"decision": "allow"}'
    exit 0
fi

INPUT=$(cat)
TOOL_RESULT=$(echo "$INPUT" | jq -r '.tool_result // empty')

# Only trigger after a successful git commit
if ! echo "$TOOL_RESULT" | grep -qE '(^\[|commit [0-9a-f])'; then
    echo '{"decision": "allow"}'
    exit 0
fi

# Check if the commit involved any renames
RENAMES=$(git diff HEAD~1..HEAD --diff-filter=R --name-only 2>/dev/null || true)

if [[ -z "$RENAMES" ]]; then
    echo '{"decision": "allow"}'
    exit 0
fi

# Extract old basenames from renamed files
STALE_REFS=""
while IFS= read -r old_file; do
    old_base=$(basename "$old_file" | sed 's/\.[^.]*$//')

    # Skip very short names (too many false positives)
    if [[ ${#old_base} -lt 4 ]]; then
        continue
    fi

    # Search for remaining references to the old name
    HITS=$(git grep -l "$old_base" 2>/dev/null | grep -v "^\.git/" | head -5 || true)

    if [[ -n "$HITS" ]]; then
        STALE_REFS="${STALE_REFS}\n- \`${old_base}\` still referenced in: $(echo "$HITS" | tr '\n' ', ' | sed 's/,$//')"
    fi
done <<< "$(git diff HEAD~1..HEAD --diff-filter=R --name-status 2>/dev/null | awk '{print $2}' || true)"

if [[ -n "$STALE_REFS" ]]; then
    REFS_ESCAPED=$(echo -e "$STALE_REFS" | sed 's/"/\\"/g' | tr '\n' ' ')
    cat << EOF
{
  "decision": "allow",
  "message": "INCOMPLETE REFACTORING DETECTED. Old names still found in codebase:${REFS_ESCAPED}\n\nThe refactoring isn't done until grep returns zero hits. Search for each old name, update all references, and commit the cleanup."
}
EOF
else
    echo '{"decision": "allow"}'
fi
