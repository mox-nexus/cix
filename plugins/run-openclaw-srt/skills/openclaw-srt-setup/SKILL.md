---
name: openclaw-srt-setup
description: "Restrict what OpenClaw can access on your machine using OS-level sandboxing. Use when: protecting credentials (SSH keys, API tokens) from the gateway process, limiting network to approved domains, preventing unauthorized file writes, hardening OpenClaw deployment, setting up SRT sandbox, troubleshooting sandbox issues. Works with: healthcheck skill for full security posture."
metadata:
  openclaw:
    emoji: null
    requires: { bins: ["srt"] }
    install:
      - id: npm-srt
        kind: npm
        package: "@anthropic-ai/sandbox-runtime"
        bins: ["srt"]
        label: "Install Sandbox Runtime (npm)"
---

# OpenClaw + SRT Sandbox

Wrap the OpenClaw gateway process with OS-level restrictions (filesystem, network) using Anthropic's Sandbox Runtime.

## Why This Matters

OpenClaw's Docker sandbox protects against malicious agent tool execution. SRT protects the **gateway process itself** — the Node.js process that manages sessions, calls APIs, and connects to channels. These are different layers with different failure modes (Swiss Cheese Model).

| Threat | Docker Sandbox | SRT | Both |
|--------|---------------|-----|------|
| Malicious agent tool reads ~/.ssh | Blocked (container) | N/A | Blocked |
| Supply chain attack on gateway dependency | **NOT blocked** | Blocked (kernel denyRead) | Blocked |
| Gateway exfiltrates to attacker.com | **NOT blocked** | Blocked (proxy allowlist) | Blocked |

---

## Core Rules

- Require explicit approval before any state-changing action
- Infer OS, existing installation state, and prerequisites before asking user
- Show exact command before executing — never run launchctl/systemctl silently
- If verification fails, diagnose and offer fix (don't just say "fix and retry")
- Present choices as numbered options so user can reply with a single digit
- Default to minimal security profile — every domain addition is a conscious decision

---

## Workflow

Follow these phases in order. Each builds on the previous.

### 1) Infer context (read-only)

Check before asking:
- OS (macOS or Linux)
- OpenClaw installed? (`which openclaw`)
- SRT installed? (`which srt`)
- Gateway running? (`ps aux | grep openclaw`)
- Already sandboxed? (`ps aux | grep "srt.*settings"`)
- Existing SRT config? (`ls ~/.srt-settings.json`)

Report: "Here's what I found: [state]. Here's what's needed: [gaps]."

### 2) Choose security profile

Present numbered options:

1. **Minimal** (recommended) — Claude API + Telegram only (2 domains). Maximum security.
2. **Developer** — Adds GitHub, npm, docs (~50 domains).
3. **AI Research** — Adds arXiv, HuggingFace, AI blogs (~30 domains).
4. **Custom** — Start minimal, add domains as needed.

Copy the chosen template:
```bash
cp assets/srt-minimal.json ~/.srt-settings.json
```

**Critical wildcard gotcha:** `*.example.com` does NOT match `example.com`. Always include both.

### 3) Show plan

Before any changes, present the exact steps:
- "I will: install daemon, patch plist to wrap with SRT, verify sandbox is active"
- Show the commands that will run
- Wait for approval

### 4) Execute with approval

**macOS:**
```bash
# Install daemon (if not running)
openclaw daemon install

# Stop, patch, restart with SRT
launchctl bootout gui/$(id -u)/ai.openclaw.gateway 2>/dev/null || true
python3 scripts/patch-plist.py
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

**Linux:** See [linux-setup.md](references/linux-setup.md) for systemd equivalent.

Each command: show it, explain what it does, get approval before running.

### 5) Verify

```bash
bash scripts/verify-sandbox.sh
```

If any check fails:
1. Read the error message (the script provides specific diagnostics)
2. Diagnose the cause
3. Offer a fix
4. Re-run verification

Only report success when all checks pass.

---

## After OpenClaw Upgrades

`openclaw daemon install --force` overwrites plist. Re-run from Phase 4:

```bash
launchctl bootout gui/$(id -u)/ai.openclaw.gateway
python3 scripts/patch-plist.py
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist
bash scripts/verify-sandbox.sh
```

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

## Architecture

```
launchd → srt --settings → sandbox-exec (kernel) + HTTP proxy (network)
```

- **Filesystem:** kernel-enforced via Seatbelt (macOS) / bubblewrap (Linux)
- **Network:** macOS: kernel-enforced Seatbelt blocks all non-localhost + proxy filters by domain. Linux: network namespace isolation + proxy.

See [architecture.md](references/architecture.md) for internals.

---

## Limitations

What SRT does **NOT** protect against:

| Limitation | Why | Mitigation |
|---|---|---|
| Docker socket abuse | Gateway needs Docker access to manage agent containers | Monitor Docker activity |
| Kernel exploits | Beyond application sandbox | Keep OS patched |
| Config tampering | If `~/.srt-settings.json` is writable | Not under any allowWrite path by default |
| Side-channel attacks | Timing, cache, spectre | Beyond scope |

SRT is defense-in-depth, not a silver bullet. It raises the bar significantly but does not eliminate all risk. The Docker socket is the most significant remaining gap — a compromised gateway could use it to create privileged containers.

---

## Operational Commands

| Task | Command |
|------|---------|
| Status | `openclaw status --all` |
| Restart | `launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway` |
| Logs | `tail -f ~/.openclaw/logs/gateway.log` |
| Stop | `launchctl bootout gui/$(id -u)/ai.openclaw.gateway` |
| Debug SRT | `srt -d --settings ~/.srt-settings.json -- echo test` |

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

## Config Templates

Available in `assets/`:

| Template | Domains | Use Case |
|----------|---------|----------|
| `srt-minimal.json` | 2 | Claude + Telegram only (recommended default) |
| `srt-developer.json` | ~50 | GitHub, npm, docs |
| `srt-ai-research.json` | ~30 | arXiv, HuggingFace, AI blogs |
| `srt-job-hunting.json` | ~25 | LinkedIn, job boards |
| `srt-settings.json` | ~50 | All-inclusive (use specific templates instead) |
