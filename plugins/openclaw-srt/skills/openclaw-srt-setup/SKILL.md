---
name: openclaw-srt-setup
description: "Sets up OpenClaw with SRT sandbox. Use when: installing OpenClaw securely, configuring network/filesystem restrictions, setting up daemon with sandboxing, troubleshooting SRT issues."
---

# OpenClaw + SRT Setup

Run OpenClaw inside SRT (Sandbox Runtime) for defense-in-depth.

## Why Sandbox?

| Risk | Impact | SRT Mitigation |
|------|--------|----------------|
| Credential theft | SSH keys, API tokens exposed | `denyRead: ~/.ssh, ~/.aws` |
| Exfiltration | Data sent to attacker | `allowedDomains` whitelist |
| Persistence | Shell configs backdoored | `denyWrite: ~/.bashrc` |

## Quick Decision

| Situation | Action |
|-----------|--------|
| Fresh install | `bash ${CLAUDE_PLUGIN_ROOT}/scripts/install.sh` |
| Existing OpenClaw | Patch plist (Step 3 below) |
| Just want config | Copy template, customize domains |
| Network issues | See [gotchas.md](references/gotchas.md) |

---

## Setup Checklist

Work through steps sequentially. Each depends on the previous.

- [ ] Prerequisites installed (Node 22+, bun, OpenClaw, SRT)
- [ ] SRT config created (`~/.srt-settings.json`)
- [ ] Daemon installed (`openclaw daemon install`)
- [ ] Plist patched for SRT (`patch-plist.py`)
- [ ] Sandbox verified (`verify-sandbox.sh`)

---

## Setup Flow

### Prerequisites

| OS | Required |
|----|----------|
| Both | Node 22+, bun, OpenClaw, SRT |
| Linux | bubblewrap, socat, `kernel.unprivileged_userns_clone=1` |

### Step 1: Create SRT Config

```bash
cp ${CLAUDE_PLUGIN_ROOT}/templates/srt-settings.json ~/.srt-settings.json
```

**Critical:** `*.example.com` does NOT match `example.com`. Include both.

### Step 2: Install Daemon

```bash
openclaw daemon install
```

### Step 3: Patch for SRT (macOS)

```bash
launchctl bootout gui/$(id -u)/ai.openclaw.gateway
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/patch-plist.py
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

### Step 4: Verify

```bash
bash ${CLAUDE_PLUGIN_ROOT}/scripts/verify-sandbox.sh
```

**Feedback loop:** If verification fails, fix the issue and re-run Step 4. Only proceed when all checks pass.

---

## Critical Gotcha: The `--` Separator

SRT uses Commander.js which keeps parsing flags after the command.

```bash
# BAD - curl's -s eaten as SRT's --settings
srt --settings ~/.srt-settings.json curl -s https://example.com

# GOOD - double-dash stops flag parsing
srt --settings ~/.srt-settings.json -- curl -s https://example.com
```

The patch script adds `--` automatically. If manually running commands through SRT, always include it.

---

## Architecture Summary

```
launchd → srt --settings → sandbox-exec (kernel) + HTTP proxy (network)
```

- Filesystem: kernel-enforced via seatbelt
- Network: proxy-enforced via domain allowlist

See [architecture.md](references/architecture.md) for internals.

---

## Operational Commands

| Task | Command |
|------|---------|
| Status | `openclaw status --all` |
| Restart | `launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway` |
| Logs | `tail -f ~/.openclaw/logs/gateway.log` |
| Stop | `launchctl bootout gui/$(id -u)/ai.openclaw.gateway` |

---

## After Upgrades

`openclaw daemon install --force` overwrites plist. Re-patch:

```bash
launchctl bootout gui/$(id -u)/ai.openclaw.gateway
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/patch-plist.py
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist
bash ${CLAUDE_PLUGIN_ROOT}/scripts/verify-sandbox.sh
```

---

## References

| Need | Load |
|------|------|
| macOS step-by-step | [macos-setup.md](references/macos-setup.md) |
| Linux step-by-step | [linux-setup.md](references/linux-setup.md) |
| How sandboxing works | [architecture.md](references/architecture.md) |
| Edge cases, debugging | [gotchas.md](references/gotchas.md) |
| Security analysis | [security-model.md](references/security-model.md) |
| Telegram bot | [telegram-setup.md](references/telegram-setup.md) |
| Logging | [observability.md](references/observability.md) |

## Templates

| Template | Use Case |
|----------|----------|
| `srt-minimal.json` | Claude + Telegram only |
| `srt-settings.json` | Full featured (default) |
| `srt-developer.json` | GitHub, npm, docs |
| `srt-job-hunting.json` | LinkedIn, job boards |
