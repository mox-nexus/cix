---
name: openclaw-srt-setup
description: "Set up OpenClaw with SRT sandbox. Use when: installing OpenClaw securely, configuring network/filesystem restrictions, setting up daemon with sandboxing, troubleshooting SRT issues."
---

# OpenClaw + SRT Setup

Run OpenClaw (personal AI assistant) inside Anthropic's Sandbox Runtime (SRT) for defense-in-depth security.

## Why Sandbox?

OpenClaw can execute code, access network, read/write files. Without sandboxing:

| Risk | Impact |
|------|--------|
| Credential theft | SSH keys, API tokens, cloud configs exposed |
| Network exfiltration | Data sent to arbitrary endpoints |
| Persistence | Shell configs modified for backdoors |

**SRT mitigates** via OS-level sandbox (`sandbox-exec` on macOS, `bubblewrap` on Linux) + network proxy filtering.

## Quick Decision

| Situation | Action |
|-----------|--------|
| Fresh install | Run setup script (Step 1) |
| Existing OpenClaw | Modify plist to add SRT wrapper (Step 3) |
| Just want the config | Copy templates, customize domains |
| Debugging network issues | Check [gotchas.md](references/gotchas.md) |

---

## Setup Flow

### Quick Install (Recommended)

```bash
# Check dependencies first
bash ${CLAUDE_PLUGIN_ROOT}/scripts/check-deps.sh

# Run installer (auto-detects OS)
bash ${CLAUDE_PLUGIN_ROOT}/scripts/install.sh

# Or with specific template
bash ${CLAUDE_PLUGIN_ROOT}/scripts/install.sh --template developer
```

### Manual Setup

#### Step 1: Prerequisites

| OS | Required | Install |
|----|----------|---------|
| **Both** | Node.js 22+ | `brew install node@22` / distro package |
| **Both** | bun (preferred) | `curl -fsSL https://bun.sh/install \| bash` |
| **Both** | OpenClaw | `bun install -g openclaw` |
| **Both** | SRT | `bun install -g @anthropic-ai/sandbox-runtime` |
| **macOS** | uv (preferred) | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| **Linux** | bubblewrap | `apt/dnf/pacman install bubblewrap` |
| **Linux** | socat | `apt/dnf/pacman install socat` |

**Linux extra:** Enable user namespaces: `sudo sysctl -w kernel.unprivileged_userns_clone=1`

### Step 2: Create SRT Config

Use template at `${CLAUDE_PLUGIN_ROOT}/templates/srt-settings.json`:

```bash
cp ${CLAUDE_PLUGIN_ROOT}/templates/srt-settings.json ~/.srt-settings.json
```

Then customize `allowedDomains` for your use case. The template includes:
- Core: `api.anthropic.com`, `api.telegram.org`
- Job sites: LinkedIn, Greenhouse, Lever, etc.
- AI news: Anthropic, OpenAI, DeepMind blogs
- Research: arXiv, HuggingFace

**Key insight:** Wildcard `*.example.com` does NOT match `example.com` itself. Include both:
```json
"linkedin.com",
"*.linkedin.com"
```

### Step 3: Install Daemon with SRT Wrapper

OpenClaw's daemon doesn't natively support SRT. The fix: modify launchd plist to invoke SRT first.

```bash
# Install daemon (creates plist)
openclaw daemon install

# Stop it
launchctl bootout gui/$(id -u)/ai.openclaw.gateway

# Patch plist to add SRT wrapper
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/patch-plist.py

# Restart
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

**What the patch does:** Prepends `srt --settings ~/.srt-settings.json --` to ProgramArguments.

### Step 4: Verify

```bash
# Check daemon is running with SRT
ps aux | grep "srt.*settings"

# Check OpenClaw status
openclaw status --all

# Should show: Gateway reachable, Telegram OK
```

---

## Architecture

```
launchd
   │
   ▼
srt --settings ~/.srt-settings.json -- node openclaw gateway
   │
   ├─► sandbox-exec (OS-level sandbox)
   │      └─► Filesystem: denyRead ~/.ssh, allowWrite ~/.openclaw
   │
   └─► HTTP/SOCKS Proxy (network filtering)
          └─► Only allowedDomains reachable
```

**Why SRT works:** It doesn't just set env vars. It:
1. Generates seatbelt profile from config
2. Runs `sandbox-exec -p <profile>` to apply OS restrictions
3. Starts proxy servers that filter by domain
4. Sets `HTTP_PROXY`/`HTTPS_PROXY` to route traffic through filter

See [architecture.md](references/architecture.md) for deep dive.

---

## Critical Gotcha: The `--` Separator

SRT CLI uses Commander.js which doesn't stop parsing at positional arguments.

**Problem:**
```bash
# BAD - curl's -s gets eaten as SRT's --settings short flag
srt --settings ~/.srt-settings.json curl -s https://example.com
```

**Solution:**
```bash
# GOOD - double-dash separates SRT options from command
srt --settings ~/.srt-settings.json -- curl -s https://example.com
```

The daemon plist uses `node ... gateway --port 18789` which doesn't conflict, but the patch script adds `--` for safety.

See [gotchas.md](references/gotchas.md) for more edge cases.

---

## Security Model

### What's Protected

| Category | Protected Items | Why |
|----------|-----------------|-----|
| Credentials | `~/.ssh`, `~/.aws`, `~/.gnupg` | Prevent key theft |
| Cloud configs | `~/.kube`, `~/.docker`, `~/.config/gcloud` | Prevent cloud access |
| Shell configs | `~/.bashrc`, `~/.zshrc` (write-blocked) | Prevent persistence |
| Network | Only allowedDomains reachable | Prevent exfiltration |

### What's Allowed

| Category | Allowed Items | Why |
|----------|---------------|-----|
| State | `~/.openclaw` | OpenClaw needs to store config/logs |
| Temp | `/tmp`, `/var/folders` | Normal operation |
| Network | Explicitly listed domains | Your use case |

### Trust Boundaries

```
Untrusted:
  ├── Incoming Telegram messages (until paired)
  └── External websites (even allowed ones)

Trusted (after verification):
  ├── Paired Telegram users
  ├── Claude API responses
  └── Local Control UI (with token)
```

---

## Telegram Setup

### Create Bot
1. Message `@BotFather` on Telegram
2. `/newbot` → choose name and username
3. Copy bot token

### Configure
```bash
openclaw config set channels.telegram.enabled true
openclaw config set channels.telegram.botToken "YOUR_TOKEN"
openclaw config set channels.telegram.dmPolicy "pairing"
```

### Pair Device
1. Send any message to your bot
2. Bot replies with pairing code (e.g., `ABC12345`)
3. Approve: `openclaw pairing approve telegram ABC12345`

**Why pairing:** Prevents random people from interacting with your AI assistant.

---

## Operational Commands

```bash
# Status
openclaw status --all

# Restart daemon
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway

# View logs
tail -f ~/.openclaw/logs/gateway.log

# Stop
launchctl bootout gui/$(id -u)/ai.openclaw.gateway

# Start
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

---

## After Upgrades

`openclaw daemon install --force` overwrites plist, losing SRT wrapper. Re-apply:

```bash
launchctl bootout gui/$(id -u)/ai.openclaw.gateway
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/patch-plist.py
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

---

## References

| Need | Load |
|------|------|
| macOS step-by-step | [macos-setup.md](references/macos-setup.md) |
| Linux step-by-step | [linux-setup.md](references/linux-setup.md) |
| How SRT sandboxing works | [architecture.md](references/architecture.md) |
| CLI gotchas, edge cases | [gotchas.md](references/gotchas.md) |
| Full security analysis | [security-model.md](references/security-model.md) |
| Telegram bot setup | [telegram-setup.md](references/telegram-setup.md) |
| Logging & debugging | [observability.md](references/observability.md) |

## Config Templates

| Template | Use Case |
|----------|----------|
| `srt-minimal.json` | Bare minimum (Claude + Telegram only) |
| `srt-settings.json` | Full featured (default) |
| `srt-ai-research.json` | AI labs, arXiv, HuggingFace |
| `srt-developer.json` | GitHub, npm, docs sites |
| `srt-job-hunting.json` | LinkedIn, job boards, ATS |

See [templates/README.md](templates/README.md) for details.
