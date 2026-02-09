#!/bin/bash
# Catches debug artifacts before commit
# Called by PreToolUse hook on Bash tool
# Opt-out: SKIP_CLEANUP_HOOKS=1
#
# Detects: console.log, TODO, FIXME, debugger, breakpoint(), pdb, etc.
# Research: Cotroneo ISSRE 2025 — AI code has more unused constructs

# Check for opt-out
if [[ "${SKIP_CLEANUP_HOOKS:-}" == "1" ]]; then
    echo '{"decision": "allow"}'
    exit 0
fi

# Get tool input from stdin (JSON with tool_input containing the command)
TOOL_INPUT=$(cat)

# Only trigger on git commit commands
if ! echo "$TOOL_INPUT" | grep -qE 'git commit'; then
    echo '{"decision": "allow"}'
    exit 0
fi

# Check staged files for scaffolding artifacts
STAGED=$(git diff --cached --unified=0 2>/dev/null || true)

if [[ -z "$STAGED" ]]; then
    echo '{"decision": "allow"}'
    exit 0
fi

# Extract only added lines (lines starting with +, not ++ which are headers)
ADDED_LINES=$(echo "$STAGED" | grep '^+[^+]' || true)

if [[ -z "$ADDED_LINES" ]]; then
    echo '{"decision": "allow"}'
    exit 0
fi

# Pattern match for scaffolding artifacts
ISSUES=""

# JavaScript/TypeScript debug artifacts
if echo "$ADDED_LINES" | grep -qE 'console\.(log|debug|warn)\('; then
    ISSUES="${ISSUES}\n- console.log/debug/warn statements"
fi

# Python debug artifacts
if echo "$ADDED_LINES" | grep -qE '(pdb\.set_trace|breakpoint\(\)|import pdb|import ipdb)'; then
    ISSUES="${ISSUES}\n- Python debugger statements"
fi

# JavaScript debugger
if echo "$ADDED_LINES" | grep -qE '\bdebugger\b'; then
    ISSUES="${ISSUES}\n- debugger; statements"
fi

# TODO/FIXME/HACK markers
if echo "$ADDED_LINES" | grep -qE '(TODO:|FIXME:|HACK:|XXX:)'; then
    ISSUES="${ISSUES}\n- TODO/FIXME/HACK markers"
fi

# Hardcoded credential patterns (simple heuristic)
if echo "$ADDED_LINES" | grep -qiE '(password|secret|api_key|token)\s*=\s*["\x27][^"\x27]{8,}'; then
    ISSUES="${ISSUES}\n- Possible hardcoded credentials"
fi

if [[ -n "$ISSUES" ]]; then
    # Escape for JSON
    ISSUES_ESCAPED=$(echo -e "$ISSUES" | sed 's/"/\\"/g' | tr '\n' ' ')
    cat << EOF
{
  "decision": "allow",
  "message": "🧹 SCAFFOLDING DETECTED in staged files. Clean up before committing:${ISSUES_ESCAPED}\n\nRun \`git diff --cached\` to find exact locations. Remove debug artifacts, then re-stage and commit."
}
EOF
else
    echo '{"decision": "allow"}'
fi
