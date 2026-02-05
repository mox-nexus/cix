# openclaw-srt

Set up OpenClaw with SRT sandbox for secure personal AI assistant operation.

## What This Plugin Does

Guides you through running [OpenClaw](https://github.com/anthropics/openclaw) inside Anthropic's [Sandbox Runtime (SRT)](https://github.com/anthropics/sandbox-runtime) for defense-in-depth security.

**Why sandbox?** OpenClaw can execute code, access network, and read/write files. Without sandboxing, a compromised agent could steal credentials, exfiltrate data, or establish persistence.

**What SRT provides:**
- OS-level sandboxing (sandbox-exec on macOS, bubblewrap on Linux)
- Network filtering via HTTP/SOCKS proxy (domain allowlist)
- Filesystem restrictions (block sensitive paths)

## Quick Start

```bash
# 1. Copy SRT config template
cp ~/.claude/plugins/openclaw-srt/skills/openclaw-srt-setup/templates/srt-settings.json ~/.srt-settings.json

# 2. Customize allowedDomains for your use case
# Edit ~/.srt-settings.json

# 3. Install OpenClaw daemon
openclaw daemon install

# 4. Patch plist to add SRT wrapper
python3 ~/.claude/plugins/openclaw-srt/skills/openclaw-srt-setup/scripts/patch-plist.py

# 5. Start daemon
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist

# 6. Verify
openclaw status --all
```

## Contents

### Skill

- **openclaw-srt-setup** - Step-by-step setup guide with decision points

### Scripts

- `patch-plist.py` - Adds SRT wrapper to OpenClaw launchd plist
- `verify-sandbox.sh` - Verifies sandbox is active

### Templates

- `srt-settings.json` - Pre-configured SRT config for job hunting + AI news use case

### References

- `architecture.md` - How SRT sandboxing actually works
- `gotchas.md` - Hard-won debugging lessons (including the critical `--` separator issue)
- `security-model.md` - What's protected and why
- `linux-setup.md` - Setup for Linux with systemd

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

- Node.js 22+
- OpenClaw (`npm install -g openclaw`)
- SRT (`npm install -g @anthropic-ai/sandbox-runtime`)
- macOS (sandbox-exec) or Linux (bubblewrap + socat)

## License

MIT
