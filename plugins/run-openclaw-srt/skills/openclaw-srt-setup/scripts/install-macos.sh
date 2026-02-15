#!/bin/bash
# OpenClaw + SRT Install Script for macOS
#
# Usage: ./install-macos.sh [--template NAME]
#
# Templates: minimal, default, ai-research, developer, job-hunting

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info() { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[OK]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# Get script directory (for accessing templates)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATES_DIR="$SCRIPT_DIR/../templates"

# Default template
TEMPLATE="${1:-default}"
case "$TEMPLATE" in
    --template) TEMPLATE="${2:-default}" ;;
    minimal|default|ai-research|developer|job-hunting) ;;
    *) TEMPLATE="default" ;;
esac

echo ""
echo "╔════════════════════════════════════════════╗"
echo "║   OpenClaw + SRT Installer (macOS)         ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# ─────────────────────────────────────────────────
# Check Dependencies
# ─────────────────────────────────────────────────

info "Checking dependencies..."

# macOS check
if [[ "$(uname)" != "Darwin" ]]; then
    error "This script is for macOS. Use install-linux.sh for Linux."
fi

# Node.js
if ! command -v node &> /dev/null; then
    error "Node.js not found. Install with: brew install node@22"
fi

NODE_VERSION=$(node --version | sed 's/v//' | cut -d. -f1)
if [[ "$NODE_VERSION" -lt 22 ]]; then
    warn "Node.js $NODE_VERSION found. Version 22+ recommended."
fi
success "Node.js $(node --version)"

# npm
if ! command -v npm &> /dev/null; then
    error "npm not found. Should come with Node.js."
fi
success "npm $(npm --version)"

# uv (preferred) or Python3 for patch script
if command -v uv &> /dev/null; then
    PY_RUN="uv run python3"
    success "uv $(uv --version | cut -d' ' -f2) (preferred)"
elif command -v python3 &> /dev/null; then
    PY_RUN="python3"
    warn "python3 found (uv preferred: curl -LsSf https://astral.sh/uv/install.sh | sh)"
else
    error "Neither uv nor python3 found. Install uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
fi

echo ""

# ─────────────────────────────────────────────────
# Detect Package Manager (bun preferred)
# ─────────────────────────────────────────────────

if command -v bun &> /dev/null; then
    PKG="bun"
    PKG_INSTALL="bun install -g"
    success "Using bun $(bun --version)"
elif command -v npm &> /dev/null; then
    PKG="npm"
    PKG_INSTALL="npm install -g"
    warn "bun not found, using npm (slower)"
else
    error "Neither bun nor npm found. Install bun: curl -fsSL https://bun.sh/install | bash"
fi

# ─────────────────────────────────────────────────
# Install OpenClaw
# ─────────────────────────────────────────────────

info "Checking OpenClaw..."

if command -v openclaw &> /dev/null; then
    success "OpenClaw $(openclaw --version 2>/dev/null || echo 'installed')"
else
    info "Installing OpenClaw via $PKG..."
    $PKG_INSTALL openclaw
    success "OpenClaw installed"
fi

# ─────────────────────────────────────────────────
# Install SRT
# ─────────────────────────────────────────────────

info "Checking SRT..."

if command -v srt &> /dev/null; then
    success "SRT $(srt --version 2>/dev/null || echo 'installed')"
    SRT_PATH=$(which srt)
else
    info "Installing SRT via $PKG..."
    $PKG_INSTALL @anthropic-ai/sandbox-runtime

    # Find where it installed (bun puts it in ~/.bun/bin)
    if [[ -f "$HOME/.bun/bin/srt" ]]; then
        SRT_PATH="$HOME/.bun/bin/srt"
    elif command -v srt &> /dev/null; then
        SRT_PATH=$(which srt)
    elif [[ -f "/usr/local/bin/srt" ]]; then
        SRT_PATH="/usr/local/bin/srt"
    else
        error "SRT installed but not found in PATH"
    fi
    success "SRT installed at $SRT_PATH"
fi

echo ""

# ─────────────────────────────────────────────────
# Create Directories
# ─────────────────────────────────────────────────

info "Creating directories..."

mkdir -p ~/.openclaw/credentials
mkdir -p ~/.openclaw/logs
mkdir -p ~/.openclaw/scripts

success "Directories created"

# ─────────────────────────────────────────────────
# Copy SRT Config
# ─────────────────────────────────────────────────

info "Setting up SRT config (template: $TEMPLATE)..."

# Map template name to file
case "$TEMPLATE" in
    minimal) TEMPLATE_FILE="srt-minimal.json" ;;
    default) TEMPLATE_FILE="srt-settings.json" ;;
    ai-research) TEMPLATE_FILE="srt-ai-research.json" ;;
    developer) TEMPLATE_FILE="srt-developer.json" ;;
    job-hunting) TEMPLATE_FILE="srt-job-hunting.json" ;;
esac

if [[ -f "$HOME/.srt-settings.json" ]]; then
    warn "SRT config already exists at ~/.srt-settings.json"
    warn "Skipping (backup at ~/.srt-settings.json.bak if you want to replace)"
    cp "$HOME/.srt-settings.json" "$HOME/.srt-settings.json.bak" 2>/dev/null || true
else
    if [[ -f "$TEMPLATES_DIR/$TEMPLATE_FILE" ]]; then
        cp "$TEMPLATES_DIR/$TEMPLATE_FILE" "$HOME/.srt-settings.json"
        success "SRT config created from $TEMPLATE_FILE"
    else
        warn "Template not found at $TEMPLATES_DIR/$TEMPLATE_FILE"
        warn "Create ~/.srt-settings.json manually"
    fi
fi

echo ""

# ─────────────────────────────────────────────────
# Install Daemon
# ─────────────────────────────────────────────────

info "Installing OpenClaw daemon..."

# Stop existing if running
launchctl bootout gui/$(id -u)/ai.openclaw.gateway 2>/dev/null || true

# Install daemon (creates plist)
openclaw daemon install 2>/dev/null || true

if [[ ! -f "$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist" ]]; then
    error "Daemon install failed. Run 'openclaw daemon install' manually."
fi

success "Daemon plist created"

# ─────────────────────────────────────────────────
# Patch Plist for SRT
# ─────────────────────────────────────────────────

info "Patching plist for SRT wrapper..."

$PY_RUN "$SCRIPT_DIR/patch-plist.py" --srt-path "$SRT_PATH"

success "Plist patched"

echo ""

# ─────────────────────────────────────────────────
# Start Daemon
# ─────────────────────────────────────────────────

info "Starting sandboxed daemon..."

launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist

# Wait a moment for startup
sleep 2

# Verify
if ps aux | grep -q "[s]rt.*settings"; then
    success "Daemon running with SRT sandbox"
else
    warn "Daemon may not have started. Check: ps aux | grep srt"
fi

echo ""

# ─────────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────────

echo "╔════════════════════════════════════════════╗"
echo "║   Installation Complete                    ║"
echo "╚════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo ""
echo "  1. Configure Anthropic credentials:"
echo "     openclaw config set providers.anthropic.apiKey \"sk-ant-...\""
echo ""
echo "  2. Set gateway token:"
echo "     openclaw config set gateway.auth.token \"\$(openssl rand -hex 16)\""
echo ""
echo "  3. (Optional) Set up Telegram:"
echo "     openclaw config set channels.telegram.enabled true"
echo "     openclaw config set channels.telegram.botToken \"YOUR_TOKEN\""
echo ""
echo "  4. Verify status:"
echo "     openclaw status --all"
echo ""
echo "  5. Access Control UI:"
echo "     http://127.0.0.1:18789/?token=\$(openclaw config get gateway.auth.token)"
echo ""
