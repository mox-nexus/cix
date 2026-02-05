#!/bin/bash
# OpenClaw + SRT Install Script for Linux
#
# Usage: ./install-linux.sh [--template NAME]
#
# Templates: minimal, default, ai-research, developer, job-hunting
#
# Dependencies:
#   - Node.js 22+
#   - bubblewrap (bwrap)
#   - socat
#   - systemd (for user services)

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
echo "║   OpenClaw + SRT Installer (Linux)         ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# ─────────────────────────────────────────────────
# Detect Package Manager
# ─────────────────────────────────────────────────

detect_pkg_manager() {
    if command -v apt &> /dev/null; then
        echo "apt"
    elif command -v dnf &> /dev/null; then
        echo "dnf"
    elif command -v pacman &> /dev/null; then
        echo "pacman"
    elif command -v zypper &> /dev/null; then
        echo "zypper"
    else
        echo "unknown"
    fi
}

PKG_MANAGER=$(detect_pkg_manager)
info "Detected package manager: $PKG_MANAGER"

# ─────────────────────────────────────────────────
# Check Dependencies
# ─────────────────────────────────────────────────

info "Checking dependencies..."

# Linux check
if [[ "$(uname)" != "Linux" ]]; then
    error "This script is for Linux. Use install-macos.sh for macOS."
fi

# bubblewrap
if ! command -v bwrap &> /dev/null; then
    echo ""
    warn "bubblewrap not found. Install with:"
    case "$PKG_MANAGER" in
        apt) echo "    sudo apt install bubblewrap" ;;
        dnf) echo "    sudo dnf install bubblewrap" ;;
        pacman) echo "    sudo pacman -S bubblewrap" ;;
        zypper) echo "    sudo zypper install bubblewrap" ;;
        *) echo "    <your package manager> install bubblewrap" ;;
    esac
    error "bubblewrap is required for SRT sandbox on Linux"
fi
success "bubblewrap $(bwrap --version 2>/dev/null | head -1 || echo 'installed')"

# socat
if ! command -v socat &> /dev/null; then
    echo ""
    warn "socat not found. Install with:"
    case "$PKG_MANAGER" in
        apt) echo "    sudo apt install socat" ;;
        dnf) echo "    sudo dnf install socat" ;;
        pacman) echo "    sudo pacman -S socat" ;;
        zypper) echo "    sudo zypper install socat" ;;
        *) echo "    <your package manager> install socat" ;;
    esac
    error "socat is required for SRT network bridging on Linux"
fi
success "socat installed"

# Check user namespaces
USERNS=$(cat /proc/sys/kernel/unprivileged_userns_clone 2>/dev/null || echo "1")
if [[ "$USERNS" == "0" ]]; then
    echo ""
    warn "Unprivileged user namespaces are disabled."
    warn "Enable with:"
    echo "    sudo sysctl -w kernel.unprivileged_userns_clone=1"
    echo "    echo 'kernel.unprivileged_userns_clone=1' | sudo tee /etc/sysctl.d/99-userns.conf"
    error "User namespaces required for bubblewrap"
fi
success "User namespaces enabled"

# Node.js
if ! command -v node &> /dev/null; then
    echo ""
    warn "Node.js not found. Install with:"
    case "$PKG_MANAGER" in
        apt) echo "    curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -"
             echo "    sudo apt install -y nodejs" ;;
        dnf) echo "    sudo dnf module install nodejs:22" ;;
        pacman) echo "    sudo pacman -S nodejs npm" ;;
        *) echo "    Install Node.js 22+ from https://nodejs.org/" ;;
    esac
    error "Node.js 22+ is required"
fi

NODE_VERSION=$(node --version | sed 's/v//' | cut -d. -f1)
if [[ "$NODE_VERSION" -lt 22 ]]; then
    warn "Node.js $NODE_VERSION found. Version 22+ recommended."
fi
success "Node.js $(node --version)"

# Detect JS package manager (bun preferred)
if command -v bun &> /dev/null; then
    JS_PKG="bun"
    JS_PKG_INSTALL="bun install -g"
    success "Using bun $(bun --version)"
elif command -v npm &> /dev/null; then
    JS_PKG="npm"
    JS_PKG_INSTALL="npm install -g"
    warn "bun not found, using npm (slower). Install bun: curl -fsSL https://bun.sh/install | bash"
else
    error "Neither bun nor npm found"
fi

# systemd
if ! command -v systemctl &> /dev/null; then
    warn "systemd not found. Manual service setup required."
fi

echo ""

# ─────────────────────────────────────────────────
# Install OpenClaw
# ─────────────────────────────────────────────────

info "Checking OpenClaw..."

if command -v openclaw &> /dev/null; then
    success "OpenClaw $(openclaw --version 2>/dev/null || echo 'installed')"
else
    info "Installing OpenClaw via $JS_PKG..."
    $JS_PKG_INSTALL openclaw
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
    info "Installing SRT via $JS_PKG..."
    $JS_PKG_INSTALL @anthropic-ai/sandbox-runtime

    # Find where it installed (bun: ~/.bun/bin, npm: varies)
    if [[ -f "$HOME/.bun/bin/srt" ]]; then
        SRT_PATH="$HOME/.bun/bin/srt"
    elif command -v srt &> /dev/null; then
        SRT_PATH=$(which srt)
    elif [[ -f "$HOME/.local/bin/srt" ]]; then
        SRT_PATH="$HOME/.local/bin/srt"
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
mkdir -p ~/.config/systemd/user

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
# Create systemd Service
# ─────────────────────────────────────────────────

info "Creating systemd user service..."

# Find node path
NODE_PATH=$(which node)

# Find openclaw path
OPENCLAW_PATH=$(npm root -g)/openclaw/dist/index.js
if [[ ! -f "$OPENCLAW_PATH" ]]; then
    # Try alternative location
    OPENCLAW_PATH=$(dirname $(which openclaw 2>/dev/null || echo ""))/../lib/node_modules/openclaw/dist/index.js
fi

SERVICE_FILE="$HOME/.config/systemd/user/openclaw-gateway.service"

cat > "$SERVICE_FILE" << EOF
[Unit]
Description=OpenClaw Gateway (SRT Sandboxed)
After=network.target

[Service]
Type=simple
ExecStart=$SRT_PATH --settings $HOME/.srt-settings.json -- $NODE_PATH $OPENCLAW_PATH gateway --port 18789
Restart=on-failure
RestartSec=5
Environment="PATH=$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin"
Environment="HOME=$HOME"

# Logging
StandardOutput=append:$HOME/.openclaw/logs/gateway.log
StandardError=append:$HOME/.openclaw/logs/gateway.err.log

[Install]
WantedBy=default.target
EOF

success "Service file created at $SERVICE_FILE"

# ─────────────────────────────────────────────────
# Enable and Start Service
# ─────────────────────────────────────────────────

info "Enabling and starting service..."

# Reload systemd
systemctl --user daemon-reload

# Enable service
systemctl --user enable openclaw-gateway

# Stop if running
systemctl --user stop openclaw-gateway 2>/dev/null || true

# Start service
systemctl --user start openclaw-gateway

# Wait a moment for startup
sleep 2

# Check status
if systemctl --user is-active --quiet openclaw-gateway; then
    success "Service is running"
else
    warn "Service may have failed to start. Check: systemctl --user status openclaw-gateway"
fi

# Enable linger for persistence
if command -v loginctl &> /dev/null; then
    info "Enabling linger for persistent service..."
    loginctl enable-linger "$USER" 2>/dev/null || warn "Could not enable linger"
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
echo "     systemctl --user status openclaw-gateway"
echo ""
echo "  5. View logs:"
echo "     journalctl --user -u openclaw-gateway -f"
echo ""
echo "  6. Access Control UI:"
echo "     http://127.0.0.1:18789/?token=\$(openclaw config get gateway.auth.token)"
echo ""
