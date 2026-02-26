---
name: openclaw-seatbelt-setup
description: "This skill should be used when the user asks to 'install OpenClaw', 'sandbox my AI assistant', 'configure Seatbelt', 'protect my credentials from OpenClaw', or needs macOS Seatbelt sandboxing for secure AI assistant operation."
metadata:
  openclaw:
    emoji: null
    requires: { bins: ["sandbox-exec"] }
    notes:
      - "sandbox-exec ships with macOS — no installation needed"
      - "Network domain filtering NOT available (requires SRT, blocked by openclaw/openclaw#13567)"
---

# OpenClaw + Seatbelt Sandbox

Wrap the OpenClaw gateway process with kernel-enforced filesystem restrictions using macOS Seatbelt (`sandbox-exec`).

## Why Seatbelt (Not SRT)

Anthropic's SRT provides both filesystem AND network sandboxing. However, OpenClaw issue #13567 prevents SRT's network proxy from working with Telegram polling (grammy's runner doesn't receive `proxyFetch`). Until that's fixed, we use raw Seatbelt for filesystem protection with unrestricted network.

| Layer | SRT | Seatbelt (this skill) | Status |
|-------|-----|----------------------|--------|
| Filesystem restrictions | Kernel-enforced | Kernel-enforced | Working |
| Network domain filtering | Proxy-based | Not available | Blocked by #13567 |
| Secret protection | denyRead rules | denyRead rules | Working |
| Persistence vector blocking | denyWrite rules | denyWrite rules | Working |

**When #13567 is fixed:** Re-enable full SRT. The SRT config templates are preserved in `assets/srt-*.json`.

---

## Core Rules

- Require explicit approval before any state-changing action
- Infer OS, existing installation state, and prerequisites before asking user
- Show exact command before executing — never run launchctl silently
- If verification fails, diagnose and offer fix (don't just say "fix and retry")
- Present choices as numbered options so user can reply with a single digit
- macOS only — Seatbelt (sandbox-exec) is a macOS kernel feature

---

## Workflow

Follow these phases in order. Each builds on the previous.

### 1) Infer context (read-only)

Check before asking:
- OS is macOS (`uname`)
- OpenClaw installed? (`which openclaw`)
- Gateway running? (`pgrep -lf openclaw`)
- Already sandboxed? (`launchctl print gui/$(id -u)/ai.openclaw.gateway | grep sandbox-exec`)
- Seatbelt profile exists? (`ls ~/.openclaw/sandbox.sb`)

Report: "Here's what I found: [state]. Here's what's needed: [gaps]."

### 2) Write Seatbelt profile

The profile lives at `~/.openclaw/sandbox.sb`. Use the template from `assets/sandbox.sb`, replacing the home directory path for the target user.

The profile structure:
```
(deny default)              <- Block everything by default
(allow process-exec/fork)   <- Allow running processes
(allow mach-lookup ...)     <- System services (logging, fonts, etc.)
(allow network*)            <- Full network (can't filter without SRT)
(allow file-read*)          <- Read everything...
(deny file-read* secrets)   <- ...except credentials
(allow file-write* openclaw)<- Write only to ~/.openclaw, /tmp, /var/folders
(deny file-write* dotfiles) <- Extra: block persistence vectors
```

**Protected secrets (denyRead):** `~/.ssh`, `~/.gnupg`, `~/.aws`, `~/.config/gcloud`, `~/.azure`, `~/Library/Keychains`, `~/.local/share/keyrings`, `~/.password-store`, `~/.1password`, `~/.kube`, `~/.docker`, `~/.npmrc`, `~/.netrc`, `~/.config/gh`

**Allowed writes:** `~/.openclaw`, `/private/tmp`, `/private/var/folders`

**Blocked persistence vectors (denyWrite):** `~/.bashrc`, `~/.bash_profile`, `~/.zshrc`, `~/.zshenv`, `~/.zprofile`, `~/.profile`, `~/.gitconfig`, `.git/hooks`

### 3) Show plan

Before any changes, present the exact steps:
- "I will: write Seatbelt profile, patch plist to wrap with sandbox-exec, verify sandbox"
- Show the commands that will run
- Wait for approval

### 4) Execute with approval

```bash
# Install daemon (if not running)
openclaw daemon install

# Stop, patch, restart with Seatbelt
launchctl bootout gui/$(id -u)/ai.openclaw.gateway 2>/dev/null || true
python3 scripts/patch-plist.py
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

Each command: show it, explain what it does, get approval before running.

### 5) Verify

```bash
bash scripts/verify-seatbelt.sh
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
bash scripts/verify-seatbelt.sh
```

---

## Architecture

```
launchd -> sandbox-exec -f sandbox.sb -> node (gateway)
                  |
                  +-- Seatbelt kernel policy (TrustedBSD MAC)
                        +-- file-read*: allow all except secrets
                        +-- file-write*: allow ~/.openclaw, /tmp only
                        +-- network*: allow all (no filtering)
```

- **Enforcement:** kernel-level via TrustedBSD MAC framework — cannot be bypassed from userspace
- **Process visibility:** `sandbox-exec` uses POSIX exec, so `ps` shows `node` not `sandbox-exec`
- **Subprocess inheritance:** All child processes inherit the sandbox (kernel-enforced)

See [architecture.md](references/architecture.md) for SRT internals (when re-enabling).

---

## Limitations

| Limitation | Why | Mitigation |
|---|---|---|
| No network domain filtering | openclaw/openclaw#13567 blocks SRT proxy | Monitor outbound; re-enable SRT when fixed |
| Docker socket abuse | Gateway needs Docker for agent containers | Monitor Docker activity |
| Kernel exploits | Beyond application sandbox | Keep macOS patched |
| Seatbelt is undocumented | Apple doesn't officially support SBPL | Based on SRT's proven profiles |
| macOS only | `sandbox-exec` is macOS-specific | Linux: use bubblewrap |

---

## Operational Commands

| Task | Command |
|------|---------|
| Status | `openclaw status --all` |
| Restart | `launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway` |
| Logs | `tail -f ~/.openclaw/logs/gateway.log` |
| Errors | `tail -f ~/.openclaw/logs/gateway.err.log` |
| Stop | `launchctl bootout gui/$(id -u)/ai.openclaw.gateway` |
| Test sandbox | `sandbox-exec -f ~/.openclaw/sandbox.sb cat ~/.ssh/id_ed25519` |

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

| File | Purpose |
|------|---------|
| `assets/sandbox.sb` | Seatbelt profile (filesystem restrictions, open network) |
| `assets/srt-*.json` | SRT domain configs (preserved for when #13567 is fixed) |
