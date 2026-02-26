#!/bin/bash
# Verify Seatbelt sandbox is active and working for OpenClaw gateway.
#
# Tests:
#   1. Gateway process running with sandbox-exec in plist
#   2. Secret paths blocked (denyRead)
#   3. Persistence vectors blocked (denyWrite)
#   4. Allowed writes work (~/.openclaw)
#   5. Profile file valid
#
# Exit codes:
#   0 - All checks pass
#   1 - One or more checks failed

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

ok()   { echo -e "${GREEN}[PASS]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
fail() { echo -e "${RED}[FAIL]${NC} $1"; }
info() { echo -e "${BLUE}[INFO]${NC} $1"; }

FAILED=0
PROFILE="${HOME}/.openclaw/sandbox.sb"

echo ""
echo "========================================"
echo "  Seatbelt Sandbox Verification"
echo "========================================"
echo ""

# ─────────────────────────────────────────────────
# Test 1: Gateway process + sandbox-exec in plist
# ─────────────────────────────────────────────────

echo "--- Test 1: Gateway Process Detection ---"
echo ""

if pgrep -lf "openclaw" > /dev/null 2>&1; then
    GW_PID=$(pgrep -f "openclaw" | head -1)
    ok "OpenClaw gateway running (PID: $GW_PID)"

    # Check if plist references sandbox-exec
    PLIST_PROGRAM=$(launchctl print "gui/$(id -u)/ai.openclaw.gateway" 2>/dev/null | grep "program = " || true)
    if echo "$PLIST_PROGRAM" | grep -q "sandbox-exec"; then
        ok "Plist uses sandbox-exec wrapper"
    else
        fail "Plist does NOT use sandbox-exec — gateway is unsandboxed"
        FAILED=1
    fi

    # Verify port binding
    if lsof -i :18789 -sTCP:LISTEN > /dev/null 2>&1; then
        ok "Gateway listening on port 18789"
    else
        warn "Gateway not listening on port 18789"
    fi
else
    fail "No OpenClaw gateway process found"
    echo "     Start with: launchctl bootstrap gui/\$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist"
    FAILED=1
fi

echo ""

# ─────────────────────────────────────────────────
# Test 2: Secret paths blocked (denyRead)
# ─────────────────────────────────────────────────

echo "--- Test 2: Secret Path Protection ---"
echo ""

if [[ ! -f "$PROFILE" ]]; then
    fail "Seatbelt profile not found at $PROFILE"
    FAILED=1
else
    BLOCKED_READ_PATHS=("$HOME/.ssh" "$HOME/.aws" "$HOME/.gnupg" "$HOME/.kube" "$HOME/.docker")
    READ_TESTED=0

    for path in "${BLOCKED_READ_PATHS[@]}"; do
        if [[ -e "$path" ]]; then
            READ_TESTED=1
            RESULT=$(/usr/bin/sandbox-exec -f "$PROFILE" /bin/ls "$path" 2>&1 || true)
            if echo "$RESULT" | grep -qi "not permitted\|denied\|operation not allowed"; then
                ok "Read blocked: $path"
            else
                fail "Read NOT blocked: $path"
                FAILED=1
            fi
        fi
    done

    if [[ $READ_TESTED -eq 0 ]]; then
        warn "No secret paths exist to test — create ~/.ssh to enable this check"
    fi
fi

echo ""

# ─────────────────────────────────────────────────
# Test 3: Persistence vectors blocked (denyWrite)
# ─────────────────────────────────────────────────

echo "--- Test 3: Persistence Vector Protection ---"
echo ""

if [[ -f "$PROFILE" ]]; then
    BLOCKED_WRITE_TARGETS=("$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.gitconfig" "$HOME/.profile")
    WRITE_TESTED=0

    for target in "${BLOCKED_WRITE_TARGETS[@]}"; do
        WRITE_TESTED=1
        RESULT=$(/usr/bin/sandbox-exec -f "$PROFILE" /bin/sh -c "echo x >> $target" 2>&1 || true)
        if echo "$RESULT" | grep -qi "not permitted\|denied\|operation not allowed"; then
            ok "Write blocked: $target"
        else
            fail "Write NOT blocked: $target"
            FAILED=1
        fi
    done

    if [[ $WRITE_TESTED -eq 0 ]]; then
        warn "No persistence vector targets tested"
    fi
fi

echo ""

# ─────────────────────────────────────────────────
# Test 4: Allowed writes work
# ─────────────────────────────────────────────────

echo "--- Test 4: Allowed Write Paths ---"
echo ""

if [[ -f "$PROFILE" ]]; then
    # Test ~/.openclaw write
    TEST_FILE="$HOME/.openclaw/seatbelt-verify-test-$$"
    RESULT=$(/usr/bin/sandbox-exec -f "$PROFILE" /bin/sh -c "echo test > $TEST_FILE && cat $TEST_FILE && rm $TEST_FILE" 2>&1 || true)
    if [[ "$RESULT" == "test" ]]; then
        ok "Write allowed: ~/.openclaw/"
    else
        fail "Write BLOCKED for ~/.openclaw/ — gateway cannot store data"
        echo "     Result: $RESULT"
        FAILED=1
    fi

    # Test /tmp write
    TMP_FILE="/tmp/seatbelt-verify-test-$$"
    RESULT=$(/usr/bin/sandbox-exec -f "$PROFILE" /bin/sh -c "echo test > $TMP_FILE && cat $TMP_FILE && rm $TMP_FILE" 2>&1 || true)
    if [[ "$RESULT" == "test" ]]; then
        ok "Write allowed: /tmp/"
    else
        fail "Write BLOCKED for /tmp/ — gateway cannot use temp files"
        FAILED=1
    fi
fi

echo ""

# ─────────────────────────────────────────────────
# Test 5: Profile validation
# ─────────────────────────────────────────────────

echo "--- Test 5: Profile Validation ---"
echo ""

if [[ -f "$PROFILE" ]]; then
    ok "Profile exists at $PROFILE"

    # Check for key directives
    if grep -q "(deny default" "$PROFILE"; then
        ok "Profile has (deny default) baseline"
    else
        fail "Profile missing (deny default) — sandbox may be permissive"
        FAILED=1
    fi

    if grep -q "(allow network\*)" "$PROFILE"; then
        ok "Profile allows all network (expected — SRT blocked by #13567)"
    else
        warn "Profile does not have (allow network*) — network may be restricted"
    fi

    if grep -q "(allow file-read\*)" "$PROFILE"; then
        ok "Profile has file-read rules"
    else
        warn "No file-read* rule found"
    fi

    # Count deny rules
    DENY_READ=$(grep -c "deny file-read" "$PROFILE" 2>/dev/null || echo "0")
    DENY_WRITE=$(grep -c "deny file-write" "$PROFILE" 2>/dev/null || echo "0")
    info "Profile has $DENY_READ read-deny rules and $DENY_WRITE write-deny rules"

    # Quick syntax check — try to sandbox a simple command
    SYNTAX_CHECK=$(/usr/bin/sandbox-exec -f "$PROFILE" /bin/echo "syntax-ok" 2>&1 || true)
    if [[ "$SYNTAX_CHECK" == "syntax-ok" ]]; then
        ok "Profile syntax valid (sandbox-exec accepts it)"
    else
        fail "Profile syntax error — sandbox-exec rejects it"
        echo "     Output: $SYNTAX_CHECK"
        FAILED=1
    fi
else
    fail "Profile not found at $PROFILE"
    echo "     Copy from plugin: cp assets/sandbox.sb ~/.openclaw/sandbox.sb"
    FAILED=1
fi

echo ""

# ─────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────

echo "========================================"
echo "  Summary"
echo "========================================"
echo ""

if [[ $FAILED -eq 0 ]]; then
    echo -e "${GREEN}Seatbelt sandbox verification PASSED${NC}"
    echo ""
    echo "The Seatbelt sandbox is active and working correctly."
    echo "Gateway filesystem access is restricted. Network is unrestricted."
    exit 0
else
    echo -e "${RED}Seatbelt sandbox verification FAILED${NC}"
    echo ""
    echo "One or more checks failed. Review the output above."
    echo ""
    echo "Common fixes:"
    echo "  - Write profile: cp assets/sandbox.sb ~/.openclaw/sandbox.sb"
    echo "  - Patch plist: python3 scripts/patch-plist.py"
    echo "  - Restart: launchctl kickstart -k gui/\$(id -u)/ai.openclaw.gateway"
    exit 1
fi
