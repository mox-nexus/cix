#!/usr/bin/env bash
# Trust-boundaries bundled scanner.
#
# Runs Semgrep against the trust-boundaries rule bundle + Gitleaks against
# the target tree. Both tools must be installed separately:
#   brew install semgrep gitleaks
# or: pip install semgrep && go install github.com/gitleaks/gitleaks/v8@latest
#
# Usage:
#   bash "$CLAUDE_PLUGIN_ROOT/skills/trust-boundaries/scripts/scan.sh" <path>

set -euo pipefail

TARGET="${1:-.}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RULES_DIR="$SCRIPT_DIR/rules"

if [[ ! -d "$TARGET" ]]; then
    echo "Error: target not a directory: $TARGET" >&2
    exit 64
fi

echo "=== Trust-boundaries scan ==="
echo "Target:   $TARGET"
echo "Rules:    $RULES_DIR"
echo ""

# --- Semgrep ---
if command -v semgrep >/dev/null 2>&1; then
    echo "--- Semgrep (trust-boundaries rules) ---"
    semgrep --quiet --config "$RULES_DIR" --error "$TARGET" || SEMGREP_RC=$?
    echo ""
else
    echo "WARNING: semgrep not installed; skipping. Install: brew install semgrep OR pip install semgrep"
    echo ""
fi

# --- Gitleaks ---
if command -v gitleaks >/dev/null 2>&1; then
    echo "--- Gitleaks (secret scan) ---"
    # --no-git scans the working tree even if not a git repo.
    gitleaks detect --source "$TARGET" --no-banner --redact || GITLEAKS_RC=$?
    echo ""
else
    echo "WARNING: gitleaks not installed; skipping. Install: brew install gitleaks OR go install github.com/gitleaks/gitleaks/v8@latest"
    echo ""
fi

# --- Zizmor (GitHub Actions specialist) ---
# Only run if the target has .github/workflows — no point otherwise.
if [[ -d "$TARGET/.github/workflows" ]]; then
    if command -v zizmor >/dev/null 2>&1; then
        echo "--- Zizmor (GitHub Actions security) ---"
        zizmor "$TARGET" || ZIZMOR_RC=$?
        echo ""
    else
        echo "INFO: .github/workflows present but zizmor not installed."
        echo "      Zizmor is the specialist scanner for GHA issues (pwn-request, template injection,"
        echo "      impostor commits, artifact poisoning). Our cicd.yaml Semgrep rules cover the"
        echo "      common cases; zizmor is deeper."
        echo "      Install: brew install zizmor OR cargo install zizmor OR uvx zizmor"
        echo ""
    fi
fi

# --- Exit with worst non-zero code ---
WORST=0
if [[ -n "${SEMGREP_RC:-}" ]]; then WORST=$SEMGREP_RC; fi
if [[ -n "${GITLEAKS_RC:-}" ]] && [[ "${GITLEAKS_RC:-0}" -gt "$WORST" ]]; then WORST=$GITLEAKS_RC; fi
if [[ -n "${ZIZMOR_RC:-}" ]] && [[ "${ZIZMOR_RC:-0}" -gt "$WORST" ]]; then WORST=$ZIZMOR_RC; fi

if [[ "$WORST" -ne 0 ]]; then
    echo "=== Findings detected — review output above ==="
    exit "$WORST"
else
    echo "=== No findings from bundled rules. This does NOT mean the code is secure. ==="
    echo "Semgrep + Gitleaks catch the pattern-matchable subset. Architectural"
    echo "review, threat modeling, and the trifecta walk remain necessary."
fi
