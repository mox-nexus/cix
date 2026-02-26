# macOS Setup

Step-by-step OpenClaw + SRT installation for macOS.

---

## Contents

- [Prerequisites](#prerequisites)
- [Setup Checklist](#setup-checklist)
- [Steps](#steps)
- [Service Commands](#service-commands)
- [After Upgrades](#after-upgrades)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

| Tool | Install | Path |
|------|---------|------|
| Node.js 22+ | `brew install node@22` | /opt/homebrew/bin/node |
| OpenClaw | `npm install -g openclaw` | varies |
| SRT | `npm install -g @anthropic-ai/sandbox-runtime` | `which srt` |

---

## Setup Checklist

Work through steps sequentially. Each depends on the previous.

- [ ] Step 1: Initialize directories
- [ ] Step 2: Configure authentication
- [ ] Step 3: Configure gateway
- [ ] Step 4: Create SRT config
- [ ] Step 5: Install daemon
- [ ] Step 6: Patch plist for SRT
- [ ] Step 7: Verify sandbox active

**Validation:** Run `verify-sandbox.sh` at the end to confirm.

---

## Steps

### Step 1: Initialize

```bash
mkdir -p ~/.openclaw/credentials ~/.openclaw/logs
openclaw doctor
```

### Step 2: Auth (pick one)

**OAuth:**
```bash
cat > ~/.openclaw/credentials/oauth.json << 'AUTHEOF'
{"anthropic": {"oauthToken": "YOUR_TOKEN"}}
AUTHEOF
```

**API Key:**
```bash
openclaw config set providers.anthropic.apiKey "sk-ant-..."
```

### Step 3: Gateway Config

```bash
openclaw config set gateway.auth.token "$(openssl rand -hex 16)"
openclaw config set gateway.mode "local"
```

### Step 4: SRT Config

```bash
cp assets/srt-settings.json ~/.srt-settings.json
# Edit allowedDomains as needed
```

### Step 5: Install Daemon

```bash
openclaw daemon install
```

### Step 6: Patch for SRT

```bash
launchctl bootout gui/$(id -u)/ai.openclaw.gateway 2>/dev/null || true
python3 scripts/patch-plist.py
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

**What patch does:** Prepends `srt --settings ~/.srt-settings.json --` to ProgramArguments.

The `--` separator is critical. Without it, flags in the wrapped command get misinterpreted.

### Step 7: Verify

```bash
# Quick check
ps aux | grep "srt.*settings"   # SRT wrapper visible
openclaw status --all           # Gateway reachable

# Full verification (recommended)
bash scripts/verify-sandbox.sh
```

**Feedback loop:** If verification fails, fix the issue and re-run Step 7. Only proceed when all checks pass.

---

## Service Commands

| Task | Command |
|------|---------|
| Status | `openclaw status --all` |
| Restart | `launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway` |
| Stop | `launchctl bootout gui/$(id -u)/ai.openclaw.gateway` |
| Logs | `tail -f ~/.openclaw/logs/gateway.log` |
| Verify sandbox | `ps aux \| grep "srt.*settings"` |
| Gateway token | `openclaw config get gateway.auth.token` |
| Control UI | `http://127.0.0.1:18789/?token=TOKEN` |

---

## After Upgrades

`openclaw daemon install --force` overwrites plist. Re-patch:

```bash
launchctl bootout gui/$(id -u)/ai.openclaw.gateway
python3 scripts/patch-plist.py
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist

# Verify again
bash scripts/verify-sandbox.sh
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Port in use | `lsof -i :18789` then `kill -9 <PID>` |
| Daemon not starting | `tail -50 ~/.openclaw/logs/gateway.err.log` |
| SRT not in ps | Check plist: `grep -A3 "ProgramArguments" ~/Library/LaunchAgents/ai.openclaw.gateway.plist` |
| Network issues | See [gotchas.md](gotchas.md) |

For detailed debugging, see [gotchas.md](gotchas.md).
