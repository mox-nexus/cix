#!/bin/bash
# Verify OpenClaw is running with SRT sandbox active

set -e

echo "=== OpenClaw + SRT Verification ==="
echo

# Check 1: Is the daemon running?
echo "1. Checking daemon status..."
if launchctl print gui/$(id -u)/ai.openclaw.gateway &>/dev/null; then
    echo "   ✓ Daemon is loaded"
else
    echo "   ✗ Daemon not loaded"
    echo "   Run: launchctl bootstrap gui/\$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist"
    exit 1
fi

# Check 2: Is SRT wrapper present?
echo
echo "2. Checking SRT wrapper..."
if ps aux | grep -q "srt.*settings.*openclaw" | grep -v grep; then
    echo "   ✓ SRT wrapper active"
    ps aux | grep "srt.*settings" | grep -v grep | head -1
else
    echo "   ✗ SRT wrapper NOT detected"
    echo "   The daemon may be running without sandbox!"
    echo "   Run: python3 patch-plist.py && launchctl kickstart -k gui/\$(id -u)/ai.openclaw.gateway"
fi

# Check 3: Is port bound?
echo
echo "3. Checking port 18789..."
if lsof -i :18789 &>/dev/null; then
    echo "   ✓ Gateway listening on port 18789"
else
    echo "   ✗ Port 18789 not bound"
    echo "   Check logs: tail ~/.openclaw/logs/gateway.err.log"
fi

# Check 4: OpenClaw status
echo
echo "4. Checking OpenClaw status..."
if command -v openclaw &>/dev/null; then
    openclaw status 2>&1 | head -10
else
    echo "   ✗ openclaw command not found"
fi

# Check 5: SRT config exists
echo
echo "5. Checking SRT config..."
if [[ -f ~/.srt-settings.json ]]; then
    echo "   ✓ Config exists at ~/.srt-settings.json"
    # Count allowed domains
    domains=$(grep -c '".*\..*"' ~/.srt-settings.json 2>/dev/null || echo "?")
    echo "   Domains configured: ~$domains"
else
    echo "   ✗ SRT config not found"
    echo "   Create: cp templates/srt-settings.json ~/.srt-settings.json"
fi

echo
echo "=== Verification complete ==="
