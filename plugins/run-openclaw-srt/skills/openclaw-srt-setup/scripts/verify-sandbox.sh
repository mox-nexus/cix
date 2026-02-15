#!/bin/bash
# Verify SRT sandbox is actually active and working
#
# Tests:
#   1. Process running under sandbox-exec (macOS) or bwrap (Linux)
#   2. Network filtering via blocked domain test
#   3. Filesystem restrictions
#
# Exit codes:
#   0 - Sandbox is active and working
#   1 - Sandbox not active or verification failed

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

ok() { echo -e "${GREEN}[PASS]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
fail() { echo -e "${RED}[FAIL]${NC} $1"; }
info() { echo -e "${BLUE}[INFO]${NC} $1"; }

FAILED=0
OS=$(uname)

echo ""
echo "========================================"
echo "  SRT Sandbox Verification"
echo "========================================"
echo ""
echo "OS: $OS"
echo ""

# ─────────────────────────────────────────────────
# Test 1: Is process running under sandbox wrapper?
# ─────────────────────────────────────────────────

echo "--- Test 1: Sandbox Process Detection ---"
echo ""

case "$OS" in
    Darwin)
        # On macOS, sandbox-exec replaces itself (exec pattern), so we look for
        # SRT wrapper in process list. The seatbelt is kernel-enforced even
        # though sandbox-exec binary is no longer running.
        
        if pgrep -f "srt.*--settings" > /dev/null 2>&1; then
            SRT_PID=$(pgrep -f "srt.*--settings" | head -1)
            ok "SRT wrapper process found (PID: $SRT_PID)"
            
            # Show what command is being wrapped
            info "Process details:"
            ps -p "$SRT_PID" -o pid,ppid,command 2>/dev/null | tail -1 | sed 's/^/     /'
        else
            # Check if daemon is running without SRT
            if pgrep -f "openclaw.*gateway" > /dev/null 2>&1; then
                fail "OpenClaw gateway running WITHOUT SRT wrapper"
                echo "     The daemon is running but not sandboxed."
                echo "     Re-run the plist patch script and restart daemon."
                FAILED=1
            else
                warn "No OpenClaw gateway process found"
                echo "     Either the daemon is not running, or it's using a different name."
            fi
        fi
        
        # Additional check: look for sandbox-related env vars in process
        if [[ -n "${SRT_PID:-}" ]]; then
            # The child process should have HTTP_PROXY set
            CHILD_PID=$(pgrep -P "$SRT_PID" 2>/dev/null | head -1 || true)
            if [[ -n "$CHILD_PID" ]]; then
                if ps eww -p "$CHILD_PID" 2>/dev/null | grep -q "HTTP_PROXY"; then
                    ok "Child process has HTTP_PROXY set (network filtering active)"
                else
                    warn "Could not verify HTTP_PROXY env var on child process"
                fi
            fi
        fi
        ;;
        
    Linux)
        # On Linux, look for bwrap (bubblewrap) process
        if pgrep -f "bwrap.*unshare-net" > /dev/null 2>&1; then
            BWRAP_PID=$(pgrep -f "bwrap.*unshare-net" | head -1)
            ok "bubblewrap sandbox process found (PID: $BWRAP_PID)"
            
            info "Process details:"
            ps -p "$BWRAP_PID" -o pid,ppid,command 2>/dev/null | tail -1 | sed 's/^/     /'
        elif pgrep -f "srt.*--settings" > /dev/null 2>&1; then
            # SRT running but might not have spawned bwrap yet
            ok "SRT wrapper process found"
            warn "bubblewrap child not detected (may be expected during startup)"
        else
            if pgrep -f "openclaw.*gateway" > /dev/null 2>&1; then
                fail "OpenClaw gateway running WITHOUT sandbox wrapper"
                FAILED=1
            else
                warn "No OpenClaw gateway process found"
            fi
        fi
        ;;
        
    *)
        fail "Unsupported OS: $OS"
        FAILED=1
        ;;
esac

echo ""

# ─────────────────────────────────────────────────
# Test 2: Network Filtering
# ─────────────────────────────────────────────────

echo "--- Test 2: Network Filtering ---"
echo ""

# We test by running a command THROUGH srt and attempting to reach a domain
# that should be blocked (not in any standard allowlist)

TEST_DOMAIN="blocked-domain-test.invalid"

if command -v srt &> /dev/null && [[ -f "$HOME/.srt-settings.json" ]]; then
    info "Testing network filtering by attempting blocked domain..."
    
    # Run curl through SRT - should fail with connection blocked
    # Using --connect-timeout to avoid hanging
    RESULT=$(srt --settings "$HOME/.srt-settings.json" -- \
        curl -s --connect-timeout 5 "https://$TEST_DOMAIN/" 2>&1 || true)
    
    if echo "$RESULT" | grep -qi "blocked\|denied\|forbidden\|refused" 2>/dev/null; then
        ok "Network filtering working (blocked domain rejected)"
    elif echo "$RESULT" | grep -qi "resolve\|not found\|no such host" 2>/dev/null; then
        # DNS resolution failed - this is also acceptable for a .invalid domain
        # but means we couldn't fully test the proxy blocking
        warn "Domain not resolvable (cannot fully verify proxy blocking)"
        echo "     Try testing with a real domain not in your allowlist"
    else
        warn "Unexpected response - verify manually"
        echo "     Response: ${RESULT:0:100}"
    fi
    
    # Test that an allowed domain DOES work (if config has common domains)
    if grep -q "api.anthropic.com" "$HOME/.srt-settings.json" 2>/dev/null; then
        info "Testing allowed domain (api.anthropic.com)..."
        ALLOWED_RESULT=$(srt --settings "$HOME/.srt-settings.json" -- \
            curl -s --connect-timeout 5 -o /dev/null -w "%{http_code}" \
            "https://api.anthropic.com/v1/messages" 2>&1 || echo "failed")
        
        # We expect 401 (unauthorized) or similar - NOT "blocked"
        if [[ "$ALLOWED_RESULT" =~ ^[2-5][0-9][0-9]$ ]]; then
            ok "Allowed domain reachable (HTTP $ALLOWED_RESULT)"
        elif echo "$ALLOWED_RESULT" | grep -qi "blocked"; then
            fail "Allowed domain was blocked - check SRT config"
            FAILED=1
        else
            warn "Could not verify allowed domain connectivity"
        fi
    fi
else
    warn "Cannot test network filtering (srt not found or config missing)"
    echo "     Install SRT and create ~/.srt-settings.json to enable this test"
fi

echo ""

# ─────────────────────────────────────────────────
# Test 3: Filesystem Restrictions
# ─────────────────────────────────────────────────

echo "--- Test 3: Filesystem Restrictions ---"
echo ""

# Test reading a path that should be blocked (if it exists)
BLOCKED_PATHS=("$HOME/.ssh" "$HOME/.aws" "$HOME/.gnupg")
FOUND_BLOCKED_PATH=""

for path in "${BLOCKED_PATHS[@]}"; do
    if [[ -d "$path" ]]; then
        FOUND_BLOCKED_PATH="$path"
        break
    fi
done

if command -v srt &> /dev/null && [[ -f "$HOME/.srt-settings.json" ]]; then
    if [[ -n "$FOUND_BLOCKED_PATH" ]]; then
        info "Testing filesystem restriction on $FOUND_BLOCKED_PATH..."
        
        # Try to read the blocked directory through SRT
        FS_RESULT=$(srt --settings "$HOME/.srt-settings.json" -- \
            ls "$FOUND_BLOCKED_PATH" 2>&1 || true)
        
        if echo "$FS_RESULT" | grep -qi "denied\|not permitted\|operation not allowed\|permission denied" 2>/dev/null; then
            ok "Filesystem restriction working ($FOUND_BLOCKED_PATH blocked)"
        elif echo "$FS_RESULT" | grep -qi "no such file\|not found" 2>/dev/null; then
            # Directory might have been removed - inconclusive
            warn "Path not accessible (may be restriction or missing)"
        else
            # Could read the directory - might be a problem
            if [[ -n "$FS_RESULT" ]]; then
                fail "Blocked path appears readable - verify SRT config"
                echo "     This may indicate sandbox restrictions are not active"
                FAILED=1
            else
                warn "Empty result - inconclusive"
            fi
        fi
    else
        warn "No blocked paths exist to test (none of: ${BLOCKED_PATHS[*]})"
        echo "     Create ~/.ssh to enable this test"
    fi
    
    # Test that allowed write path works
    info "Testing allowed write path (/tmp)..."
    WRITE_TEST_FILE="/tmp/srt-verify-test-$$"
    WRITE_RESULT=$(srt --settings "$HOME/.srt-settings.json" -- \
        sh -c "echo 'test' > $WRITE_TEST_FILE && cat $WRITE_TEST_FILE && rm $WRITE_TEST_FILE" 2>&1 || true)
    
    if [[ "$WRITE_RESULT" == "test" ]]; then
        ok "Allowed write path working (/tmp)"
    else
        warn "Could not verify write access to /tmp"
    fi
else
    warn "Cannot test filesystem restrictions (srt not found or config missing)"
fi

echo ""

# ─────────────────────────────────────────────────
# Test 4: Config Validation
# ─────────────────────────────────────────────────

echo "--- Test 4: Config Validation ---"
echo ""

if [[ -f "$HOME/.srt-settings.json" ]]; then
    ok "Config file exists at ~/.srt-settings.json"
    
    # Validate JSON syntax
    if command -v python3 &> /dev/null; then
        if python3 -m json.tool "$HOME/.srt-settings.json" > /dev/null 2>&1; then
            ok "Config JSON syntax valid"
        else
            fail "Config JSON syntax INVALID"
            echo "     Run: python3 -m json.tool ~/.srt-settings.json"
            FAILED=1
        fi
    elif command -v jq &> /dev/null; then
        if jq . "$HOME/.srt-settings.json" > /dev/null 2>&1; then
            ok "Config JSON syntax valid"
        else
            fail "Config JSON syntax INVALID"
            FAILED=1
        fi
    else
        warn "No JSON validator available (install jq or python3)"
    fi
    
    # Count domains
    DOMAIN_COUNT=$(grep -c '"[a-z].*\.' "$HOME/.srt-settings.json" 2>/dev/null || echo "0")
    info "Approximately $DOMAIN_COUNT domains configured"
    
    # Check for common gotchas
    if grep -q '"\*\.' "$HOME/.srt-settings.json" 2>/dev/null; then
        # Has wildcards - check for missing base domains
        WILDCARDS=$(grep -o '"\*\.[^"]*"' "$HOME/.srt-settings.json" | sort -u)
        MISSING_BASE=0
        while IFS= read -r wildcard; do
            base=$(echo "$wildcard" | sed 's/"\\*\./"/g')
            if ! grep -q "$base" "$HOME/.srt-settings.json" 2>/dev/null; then
                if [[ $MISSING_BASE -eq 0 ]]; then
                    warn "Wildcard domains without matching base domain:"
                fi
                echo "     $wildcard exists but $base missing"
                MISSING_BASE=$((MISSING_BASE + 1))
            fi
        done <<< "$WILDCARDS"
        
        if [[ $MISSING_BASE -eq 0 ]]; then
            ok "All wildcard domains have matching base domains"
        fi
    fi
else
    fail "Config file not found at ~/.srt-settings.json"
    echo "     Copy a template: cp assets/srt-settings.json ~/.srt-settings.json"
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
    echo -e "${GREEN}Sandbox verification PASSED${NC}"
    echo ""
    echo "The SRT sandbox appears to be active and working correctly."
    exit 0
else
    echo -e "${RED}Sandbox verification FAILED${NC}"
    echo ""
    echo "One or more checks failed. Review the output above."
    echo ""
    echo "Common fixes:"
    echo "  - Re-run plist patch: python3 scripts/patch-plist.py"
    echo "  - Restart daemon: launchctl kickstart -k gui/\$(id -u)/ai.openclaw.gateway"
    echo "  - Validate config: python3 -m json.tool ~/.srt-settings.json"
    exit 1
fi
