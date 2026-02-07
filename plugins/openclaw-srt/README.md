# openclaw-srt

Set up OpenClaw with SRT sandbox for secure personal AI assistant operation.

## What This Plugin Does

Guides you through running [OpenClaw](https://github.com/openclaw/openclaw) inside Anthropic's [Sandbox Runtime (SRT)](https://github.com/anthropic-experimental/sandbox-runtime) for defense-in-depth security.

**Why sandbox?** OpenClaw can execute code, access network, and read/write files. Without sandboxing, a compromised agent could steal credentials, exfiltrate data, or establish persistence.

**What SRT provides:**
- OS-level sandboxing (sandbox-exec on macOS, bubblewrap on Linux)
- Network filtering via HTTP/SOCKS proxy (domain allowlist)
- Filesystem restrictions (block sensitive paths)

## Quick Start

```bash
# Check dependencies
bash ~/.claude/plugins/openclaw-srt/skills/openclaw-srt-setup/scripts/check-deps.sh

# Run installer (auto-detects macOS/Linux)
bash ~/.claude/plugins/openclaw-srt/skills/openclaw-srt-setup/scripts/install.sh

# Or with a specific template
bash ~/.claude/plugins/openclaw-srt/skills/openclaw-srt-setup/scripts/install.sh --template developer

# Verify
openclaw status --all
```

**Templates:** `minimal`, `default`, `ai-research`, `developer`, `job-hunting`

## Contents

### Skill

- **openclaw-srt-setup** - Step-by-step setup guide with decision points

### Scripts

- `install.sh` - Unified installer (auto-detects OS)
- `install-macos.sh` - macOS installer (launchd)
- `install-linux.sh` - Linux installer (systemd)
- `check-deps.sh` - Verify prerequisites
- `patch-plist.py` - Adds SRT wrapper to OpenClaw launchd plist
- `verify-sandbox.sh` - Verifies sandbox is active

### Templates

- `srt-settings.json` - Pre-configured SRT config for job hunting + AI news use case

### References (Claude-optimized)

- `architecture.md` - How SRT sandboxing actually works
- `gotchas.md` - Hard-won debugging lessons (including the critical `--` separator issue)
- `security-model.md` - What's protected and why
- `macos-setup.md` / `linux-setup.md` - Platform-specific setup

### Docs (Human verification)

- `docs/explanation/architecture.md` - System architecture with Mermaid diagrams
- `docs/explanation/methodology.md` - Why sandbox? Design rationale
- `docs/explanation/sources.md` - Primary sources, citations

## Key Gotcha

SRT CLI requires `--` to separate its options from the wrapped command:

```bash
# BAD - curl's -s gets eaten as SRT's --settings flag
srt --settings config.json curl -s https://example.com

# GOOD - double-dash separates SRT options from command
srt --settings config.json -- curl -s https://example.com
```

The patch script adds this automatically.

## Requirements

### Common (both platforms)
- Node.js 22+
- bun (preferred) or npm
- OpenClaw (`bun install -g openclaw`)
- SRT (`bun install -g @anthropic-ai/sandbox-runtime`)

### macOS
- uv (preferred) or Python3 (for patch script)
- sandbox-exec (built-in)

### Linux
- bubblewrap (`apt/dnf/pacman install bubblewrap`)
- socat (`apt/dnf/pacman install socat`)
- User namespaces enabled (`sysctl kernel.unprivileged_userns_clone=1`)

## License

MIT
