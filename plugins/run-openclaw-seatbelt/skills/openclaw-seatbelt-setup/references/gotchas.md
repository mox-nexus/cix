# Seatbelt Sandbox Gotchas

Hard-won debugging lessons from sandboxing OpenClaw with macOS Seatbelt.

---

## Contents

- [SRT + OpenClaw Telegram is Broken](#1-srt--openclaw-telegram-is-broken)
- [SBPL Regex Syntax](#2-sbpl-regex-syntax)
- [sandbox-exec Not in ps](#3-sandbox-exec-not-in-ps)
- [Port Already in Use](#4-port-already-in-use)
- [Plist Lost After Upgrade](#5-plist-lost-after-upgrade)
- [Seatbelt Denials Invisible on Sonoma](#6-seatbelt-denials-invisible-on-sonoma)
- [`TypeError: fetch failed` is Useless](#7-typeerror-fetch-failed-is-useless)
- [`openclaw status --all` Lies About Telegram](#8-openclaw-status---all-lies-about-telegram)
- [Node 25 Proxy Changes](#9-node-25-proxy-changes)
- [Homebrew Path Issues](#10-homebrew-path-issues-macos)
- [Subprocess Inheritance](#11-subprocess-inheritance)
- [Quick Diagnostic](#quick-diagnostic)

---

## 1. SRT + OpenClaw Telegram is Broken

**This is why we use raw Seatbelt instead of SRT.**

**Symptom:** `TypeError: fetch failed` every ~30s. Telegram polling dies. 164K error lines accumulate.

**Root cause:** OpenClaw issue #13567 — `proxyFetch` is passed to the bot for sending but NOT to grammy's runner for polling/receiving. The gateway creates a `ProxyAgent` via `makeProxyFetch()` but only uses it for `Bot()` construction, not for `run()`.

**Code:** `monitor.js:84` checks `account.config.proxy` for explicit proxy config. When unset, falls back to bare `globalThis.fetch` which tries direct outbound — blocked by SRT's Seatbelt profile.

**What doesn't work:**
- `NODE_OPTIONS=--use-env-proxy` — necessary for Node 25+ but insufficient. OpenClaw wraps fetch with `wrapFetchWithAbortSignal()` which loses any proxy dispatcher.
- Monkey-patching `monitor.js` to read `HTTPS_PROXY` env var — works for initial setup but grammy's runner still bypasses it for getUpdates polling.
- SRT filesystem-only mode — doesn't exist. Config schema requires `network.allowedDomains`, and when defined, both proxy AND Seatbelt network restrictions activate.

**What works:** Raw `sandbox-exec` with a custom `.sb` profile that has `(allow network*)`.

**When to revisit:** Check openclaw/openclaw#13567 periodically.

---

## 2. SBPL Regex Syntax

**Symptom:** `sandbox-exec: undefined sharp expression`

**Cause:** Using Swift-style `#"..."#` raw string syntax in `.sb` files. SBPL uses standard quoted strings.

```scheme
; BAD — Swift syntax, not valid SBPL
(regex #"^/path/to/\.dir"#)

; GOOD — standard SBPL string with escaped backslashes
(regex "^/path/to/\\.dir")
```

In SBPL strings, `\` is the escape character. To get a literal `\` in the regex (for escaping `.`), use `\\`.

---

## 3. sandbox-exec Not in ps

**Why:** POSIX exec pattern — `sandbox-exec` sets up the kernel policy then replaces itself with the child process. The sandbox IS active even though the binary is gone.

**Verify:** Check the plist, not the process table:
```bash
launchctl print gui/$(id -u)/ai.openclaw.gateway | grep "program ="
# Should show: /usr/bin/sandbox-exec
```

---

## 4. Port Already in Use

**Symptom:** Can't start daemon, port 18789 in use.

**Cause:** Stale gateway from manual testing, or launchd restarting too fast.

```bash
lsof -i :18789
kill -9 <PID>
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway
```

---

## 5. Plist Lost After Upgrade

`openclaw daemon install --force` overwrites plist, removing sandbox-exec wrapper.

```bash
launchctl bootout gui/$(id -u)/ai.openclaw.gateway
python3 scripts/patch-plist.py
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist
bash scripts/verify-seatbelt.sh
```

---

## 6. Seatbelt Denials Invisible on Sonoma

**Symptom:** Can't tell if sandbox blocked a request or if it's a network error.

**Cause:** macOS Sonoma doesn't log sandbox violation messages to the system log. The `(with message "OPENCLAW_SANDBOX")` tag in deny rules is for identification but doesn't appear in standard logs.

**Workaround:** Test directly:
```bash
# Does the sandbox block this path?
sandbox-exec -f ~/.openclaw/sandbox.sb cat ~/.ssh/id_ed25519
# "Operation not permitted" = sandbox blocked it
```

---

## 7. `TypeError: fetch failed` is Useless

**Symptom:** Undici throws `TypeError: fetch failed` with zero context.

**Cause:** The actual error (ECONNREFUSED, DNS failure, sandbox denial) is in `error.cause`, which OpenClaw doesn't log.

**Debug:** Look at the nested cause:
```javascript
try { await fetch(...) } catch (e) { console.error(e.cause) }
```

Or test connectivity directly:
```bash
# From within sandbox
sandbox-exec -f ~/.openclaw/sandbox.sb curl -s https://api.telegram.org
```

---

## 8. `openclaw status --all` Lies About Telegram

**Symptom:** Shows `Telegram: ON - OK` but every fetch is failing.

**Cause:** Status check validates config (token present, enabled), not live connectivity. No actual API call is made.

**Real check:** Look for active TCP connections:
```bash
lsof -i -n -P -p $(pgrep -f openclaw) | grep "149.154\|ESTABLISHED"
```

---

## 9. Node 25 Proxy Changes

**Symptom:** Node 25+ apps behind SRT proxy fail even though `HTTP_PROXY` is set.

**Cause:** Node 25 removed automatic `HTTP_PROXY` support from `globalThis.fetch`. Requires `NODE_OPTIONS=--use-env-proxy`.

**Fix:** Add to plist EnvironmentVariables:
```xml
<key>NODE_OPTIONS</key>
<string>--use-env-proxy</string>
```

**Note:** This is necessary but NOT sufficient for OpenClaw specifically (#13567). It IS needed for other Node 25+ apps running under SRT.

---

## 10. Homebrew Path Issues (macOS)

**Symptom:** Command not found in sandbox.

**Cause:** `/opt/homebrew/bin` not in default launchd PATH.

**Fix:** Use absolute paths in plist ProgramArguments (`/opt/homebrew/bin/node`).

---

## 11. Subprocess Inheritance

**Filesystem:** All children inherit the Seatbelt sandbox (kernel-enforced). This is the key strength — no escape through subprocess spawning.

**Network:** With raw Seatbelt `(allow network*)`, no restrictions to inherit or bypass.

**Test:**
```bash
sandbox-exec -f ~/.openclaw/sandbox.sb bash -c 'cat ~/.ssh/id_ed25519'
# Should fail with "Operation not permitted"
```

---

## SRT-Specific Gotchas (for when #13567 is fixed)

These apply when re-enabling full SRT:

### The `--` Separator (Critical)

Commander.js keeps parsing flags. Your command's `-s` becomes SRT's `--settings`.

```bash
# BAD
srt --settings ~/.srt-settings.json curl -s https://api.telegram.org

# GOOD
srt --settings ~/.srt-settings.json -- curl -s https://api.telegram.org
```

### Wildcard Doesn't Match Base Domain

`*.linkedin.com` does NOT match `linkedin.com`. Always include both:
```json
["linkedin.com", "*.linkedin.com"]
```

### SRT Proxy Ports Are Dynamic

Ports change every restart. Can't hardcode in OpenClaw config. Must read from `HTTPS_PROXY` / `HTTP_PROXY` env vars at runtime.

---

## Quick Diagnostic

```bash
# 1. Gateway running?
pgrep -lf "openclaw"

# 2. Sandbox-exec in plist?
launchctl print gui/$(id -u)/ai.openclaw.gateway | grep "program ="

# 3. Profile syntax valid?
sandbox-exec -f ~/.openclaw/sandbox.sb echo "ok"

# 4. Secrets blocked?
sandbox-exec -f ~/.openclaw/sandbox.sb cat ~/.ssh/id_ed25519

# 5. Writes blocked?
sandbox-exec -f ~/.openclaw/sandbox.sb sh -c 'echo x > ~/.bashrc'

# 6. Allowed writes work?
sandbox-exec -f ~/.openclaw/sandbox.sb sh -c 'echo x > ~/.openclaw/test && rm ~/.openclaw/test'

# 7. Telegram connected?
lsof -i -n -P -p $(pgrep -f openclaw) | grep ESTABLISHED

# 8. Port listening?
lsof -i :18789 -sTCP:LISTEN
```
