# SRT Gotchas

Hard-won debugging lessons.

---

## Contents

- [The `--` Separator (Critical)](#1-the----separator-critical)
- [Wildcard Domain Matching](#2-wildcard-doesnt-match-base-domain)
- [sandbox-exec Not in ps](#3-sandbox-exec-not-in-ps)
- [Port Already in Use](#4-port-already-in-use)
- [Config Not Loading](#5-config-not-loading-silent)
- [Plist Lost After Upgrade](#6-plist-lost-after-upgrade)
- [Debug Output](#7-debug-output-not-appearing)
- [Certificate Pinning](#8-certificate-pinning-apps)
- [Subprocess Inheritance](#9-subprocess-inheritance)
- [Homebrew Path Issues](#10-homebrew-path-issues-macos)
- [Quick Diagnostic](#quick-diagnostic)

---

## 1. The `--` Separator (Critical)

**Symptom:** Network blocked even though domain is allowed.

**Cause:** Commander.js keeps parsing flags. Your command's `-s` becomes SRT's `--settings`.

```bash
# BAD
srt --settings ~/.srt-settings.json curl -s https://api.telegram.org
# -s eaten as --settings, config fails, empty allowlist, everything blocked

# GOOD
srt --settings ~/.srt-settings.json -- curl -s https://api.telegram.org
```

**How we found this:** Flag `-s` vs `-v` behaved differently. The flag being parsed was the problem.

**Note:** The patch-plist.py script adds `--` automatically.

---

## 2. Wildcard Doesn't Match Base Domain

**Symptom:** `*.linkedin.com` allowed but `linkedin.com` blocked.

```typescript
// SRT's matching: *.foo.com requires the dot
hostname.endsWith('.' + baseDomain)  // x.foo.com matches, foo.com doesn't
```

**Fix:** Always include both:
```json
["linkedin.com", "*.linkedin.com"]
```

---

## 3. sandbox-exec Not in ps

**Why:** POSIX exec pattern - replaces itself with target. Sandbox IS active (kernel-enforced).

**Verify:** `ps aux | grep "srt.*settings"`

---

## 4. Port Already in Use

**Symptom:** Can't start daemon, port 18789 in use.

**Cause:** Stale gateway from manual testing.

```bash
lsof -i :18789
kill -9 <PID>
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway
```

---

## 5. Config Not Loading (Silent)

**Symptom:** Network completely blocked. Empty allowedDomains in debug.

**Causes:**
- Wrong path: `ls -la ~/.srt-settings.json`
- Invalid JSON: `python3 -m json.tool ~/.srt-settings.json`
- Path has spaces: Quote it

---

## 6. Plist Lost After Upgrade

`openclaw daemon install --force` overwrites plist.

```bash
launchctl bootout gui/$(id -u)/ai.openclaw.gateway
python3 scripts/patch-plist.py
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

---

## 7. Debug Output Not Appearing

Use the `-d` flag (which sets `SRT_DEBUG=true` internally):

```bash
srt -d --settings ~/.srt-settings.json -- echo "test"
```

If `-d` isn't reaching early enough, set the env var directly:

```bash
SRT_DEBUG=1 srt --settings ~/.srt-settings.json -- echo "test"
```

---

## 8. Certificate Pinning Apps

**Symptom:** App works outside sandbox, fails inside, or bypasses filtering.

**Cause:** App doesn't respect `HTTP_PROXY`.

**Detect:** `sudo tcpdump -i any port 443 | grep -v localhost`

**Mitigation:** Filesystem restrictions still apply. Linux: `--unshare-net` for true isolation.

---

## 9. Subprocess Inheritance

**Filesystem:** Children inherit sandbox (kernel-enforced).

**Network:** Depends on env var inheritance. Most shells pass them; some runtimes (Java, Go) may not.

**Test:**
```bash
srt --settings ~/.srt-settings.json -- bash -c 'cat ~/.ssh/id_rsa'
# Should fail
```

---

## 10. Homebrew Path Issues (macOS)

**Symptom:** Command not found in sandbox.

**Cause:** `/opt/homebrew/bin` not in default PATH.

**Fix:** Use absolute paths in plist.

---

## Quick Diagnostic

```bash
# Checklist - run through in order:

# 1. Config loading?
SRT_DEBUG=1 srt -d --settings ~/.srt-settings.json -- echo "test" 2>&1 | grep allowedHosts

# 2. Domain in allowlist? (Check base AND wildcard)
grep "example.com" ~/.srt-settings.json

# 3. -- separator present in plist?
grep -A 10 "ProgramArguments" ~/Library/LaunchAgents/ai.openclaw.gateway.plist | grep -- '--'

# 4. Process sandboxed?
ps aux | grep "srt.*settings"

# 5. JSON valid?
python3 -m json.tool ~/.srt-settings.json > /dev/null && echo "Valid JSON"

# 6. Patched plist?
launchctl print gui/$(id -u)/ai.openclaw.gateway | grep ProgramArguments -A 10
```
