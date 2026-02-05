#!/bin/bash
# Check dependencies for OpenClaw + SRT
#
# Usage: ./check-deps.sh
#
# Exit codes:
#   0 - All dependencies met
#   1 - Missing dependencies

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

ok() { echo -e "${GREEN}✓${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }
fail() { echo -e "${RED}✗${NC} $1"; MISSING=1; }

MISSING=0
OS=$(uname)

echo ""
echo "OpenClaw + SRT Dependency Check"
echo "================================"
echo "OS: $OS"
echo ""

# ─────────────────────────────────────────────────
# Common Dependencies
# ─────────────────────────────────────────────────

echo "Common:"

# Node.js
if command -v node &> /dev/null; then
    NODE_VER=$(node --version | sed 's/v//' | cut -d. -f1)
    if [[ "$NODE_VER" -ge 22 ]]; then
        ok "Node.js $(node --version)"
    else
        warn "Node.js $(node --version) (22+ recommended)"
    fi
else
    fail "Node.js not found"
fi

# bun (preferred) or npm
if command -v bun &> /dev/null; then
    ok "bun $(bun --version) (preferred)"
elif command -v npm &> /dev/null; then
    warn "npm $(npm --version) (bun preferred: curl -fsSL https://bun.sh/install | bash)"
else
    fail "Neither bun nor npm found"
fi

# OpenClaw
if command -v openclaw &> /dev/null; then
    ok "OpenClaw installed"
else
    warn "OpenClaw not installed (npm install -g openclaw)"
fi

# SRT
if command -v srt &> /dev/null; then
    ok "SRT installed"
else
    warn "SRT not installed (npm install -g @anthropic-ai/sandbox-runtime)"
fi

echo ""

# ─────────────────────────────────────────────────
# OS-Specific Dependencies
# ─────────────────────────────────────────────────

echo "OS-Specific ($OS):"

case "$OS" in
    Darwin)
        # macOS
        # uv (preferred) or Python3 for patch script
        if command -v uv &> /dev/null; then
            ok "uv $(uv --version | cut -d' ' -f2) (preferred)"
        elif command -v python3 &> /dev/null; then
            warn "python3 $(python3 --version | cut -d' ' -f2) (uv preferred: curl -LsSf https://astral.sh/uv/install.sh | sh)"
        else
            fail "Neither uv nor python3 found"
        fi

        # sandbox-exec is built-in
        ok "sandbox-exec (built-in)"
        ;;

    Linux)
        # bubblewrap
        if command -v bwrap &> /dev/null; then
            ok "bubblewrap installed"
        else
            fail "bubblewrap not found (apt/dnf/pacman install bubblewrap)"
        fi

        # socat
        if command -v socat &> /dev/null; then
            ok "socat installed"
        else
            fail "socat not found (apt/dnf/pacman install socat)"
        fi

        # User namespaces
        USERNS=$(cat /proc/sys/kernel/unprivileged_userns_clone 2>/dev/null || echo "1")
        if [[ "$USERNS" == "1" ]]; then
            ok "User namespaces enabled"
        else
            fail "User namespaces disabled (sysctl kernel.unprivileged_userns_clone=1)"
        fi

        # systemd
        if command -v systemctl &> /dev/null; then
            ok "systemd available"
        else
            warn "systemd not found (manual service setup needed)"
        fi
        ;;

    *)
        fail "Unsupported OS: $OS"
        ;;
esac

echo ""

# ─────────────────────────────────────────────────
# Config Check
# ─────────────────────────────────────────────────

echo "Configuration:"

if [[ -f "$HOME/.srt-settings.json" ]]; then
    ok "SRT config exists (~/.srt-settings.json)"
else
    warn "SRT config not found (~/.srt-settings.json)"
fi

if [[ -f "$HOME/.openclaw/openclaw.json" ]]; then
    ok "OpenClaw config exists"
else
    warn "OpenClaw config not found (run openclaw doctor)"
fi

echo ""

# ─────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────

if [[ "$MISSING" -eq 0 ]]; then
    echo -e "${GREEN}All required dependencies met.${NC}"
    exit 0
else
    echo -e "${RED}Missing required dependencies.${NC}"
    exit 1
fi
