#!/bin/bash
# Detects when user is stuck and triggers Mr. Wolf
# Two signals: consecutive bash failures (PostToolUse) + frustration language (UserPromptSubmit)
# Opt-out: SKIP_MRWOLF_HOOKS=1

if [[ "${SKIP_MRWOLF_HOOKS:-}" == "1" ]]; then
    echo '{"decision": "allow"}'
    exit 0
fi

INPUT=$(cat)
EVENT=$(echo "$INPUT" | jq -r '.hook_event_name // empty')

STATE_FILE="/tmp/claude-mrwolf-state-${PPID:-$$}"
[[ ! -f "$STATE_FILE" ]] && echo "0" > "$STATE_FILE"

TRIGGER=false

if [[ "$EVENT" == "PostToolUse" ]]; then
    # Signal 1: Count consecutive bash failures
    FAIL_COUNT=$(cat "$STATE_FILE")
    TOOL_RESULT=$(echo "$INPUT" | jq -r '.tool_result // empty')

    if echo "$TOOL_RESULT" | grep -qiE "(error|failed|exception|not found|permission denied|command not found|no such file|cannot|unable to|fatal|panic|traceback)"; then
        FAIL_COUNT=$((FAIL_COUNT + 1))
        echo "$FAIL_COUNT" > "$STATE_FILE"
        [[ $FAIL_COUNT -ge 3 ]] && TRIGGER=true && echo "0" > "$STATE_FILE"
    else
        echo "0" > "$STATE_FILE"
    fi
elif [[ "$EVENT" == "UserPromptSubmit" ]]; then
    # Signal 2: Frustration language in user prompt
    USER_PROMPT=$(echo "$INPUT" | jq -r '.user_prompt // empty')
    PROMPT_LOWER=$(echo "$USER_PROMPT" | tr '[:upper:]' '[:lower:]')

    if echo "$PROMPT_LOWER" | grep -qE "(still not working|still doesn't work|still broken|tried everything|nothing works|keeps failing|why won't|why doesn't|what am i missing|this is broken|going crazy|so frustrated)"; then
        TRIGGER=true
    elif echo "$PROMPT_LOWER" | grep -qE "tried .+,.+,.+|i've tried|already tried"; then
        TRIGGER=true
    elif echo "$PROMPT_LOWER" | grep -qE "why (is this|does this|won't|doesn't|can't) .* (still|again|keep)"; then
        TRIGGER=true
    fi
fi
# Unknown events: pass through silently

if [[ "$TRIGGER" == "true" ]]; then
    cat << 'EOF'
{
  "decision": "allow",
  "message": "STUCK DETECTED. You MUST now: 1) Tell the user: 'This isn't converging. Bringing in Mr. Wolf.' 2) Spawn the `mrwolf` agent to break down the problem systematically. Do not continue debugging yourself."
}
EOF
else
    echo '{"decision": "allow"}'
fi
