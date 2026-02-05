#!/bin/bash
# OpenClaw + SRT Unified Installer
#
# Detects OS and runs the appropriate install script.
#
# Usage: ./install.sh [--template NAME]
#
# Templates: minimal, default, ai-research, developer, job-hunting

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

case "$(uname)" in
    Darwin)
        exec "$SCRIPT_DIR/install-macos.sh" "$@"
        ;;
    Linux)
        exec "$SCRIPT_DIR/install-linux.sh" "$@"
        ;;
    *)
        echo "Unsupported OS: $(uname)"
        echo "Supported: macOS (Darwin), Linux"
        exit 1
        ;;
esac
