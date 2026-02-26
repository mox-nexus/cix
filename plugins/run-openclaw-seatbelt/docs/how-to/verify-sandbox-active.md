# How to Verify the Sandbox Is Active

**When you need this:** After installation, upgrades, or when suspicious about sandbox status.

**What this confirms:** OpenClaw is actually running inside SRT restrictions.

**Time:** 1-2 minutes

---

## Quick Check

```bash
ps aux | grep "srt.*settings" | grep -v grep
```

**If you see output:** Sandbox is wrapping the process. You're protected.

**If empty:** Continue to full verification.

---

## Full Verification Script

```bash
bash ~/.claude/plugins/run-openclaw-srt/skills/openclaw-srt-setup/scripts/verify-sandbox.sh
```

**What it tests:**
1. **Process detection** - Is SRT in the process tree?
2. **Network filtering** - Are blocked domains rejected?
3. **Filesystem restrictions** - Are credentials protected?
4. **Config validation** - Is the JSON valid?

All four must pass for full protection.

---

## Manual Verification (Step by Step)

### Test 1: Check Process Tree

```bash
ps aux | grep "srt.*settings"
```

**Expected:** A line showing `srt --settings ~/.srt-settings.json -- ... node ... gateway`

**Why you won't see `sandbox-exec`:** It uses the POSIX exec pattern - applies restrictions then replaces itself with the target process. The restrictions remain kernel-enforced even though the wrapper process isn't visible.

### Test 2: Test Network Filtering

Test a blocked domain:

```bash
srt --settings ~/.srt-settings.json -- curl -s "https://definitely-not-allowed-domain.invalid" 2>&1
```

**Expected:** "Connection blocked" or DNS error (not a successful response)

Test an allowed domain:

```bash
srt --settings ~/.srt-settings.json -- curl -sI "https://api.anthropic.com" 2>&1 | head -1
```

**Expected:** HTTP status code (401 is fine - means request reached Anthropic)

### Test 3: Test Filesystem Restrictions

Try to read a blocked path:

```bash
srt --settings ~/.srt-settings.json -- cat ~/.ssh/id_rsa 2>&1
```

**Expected:** "Operation not permitted" or "Permission denied"

Try to write to an allowed path:

```bash
srt --settings ~/.srt-settings.json -- sh -c 'echo test > /tmp/srt-test && cat /tmp/srt-test && rm /tmp/srt-test'
```

**Expected:** "test" (write succeeds to /tmp)

### Test 4: Check Daemon Configuration

```bash
grep -A5 "ProgramArguments" ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

**Expected:** First argument should be the path to `srt`:

```xml
<key>ProgramArguments</key>
<array>
  <string>/Users/you/.bun/bin/srt</string>
  <string>--settings</string>
  <string>/Users/you/.srt-settings.json</string>
  <string>--</string>
  ...
```

If it starts with `node` instead of `srt`, the sandbox isn't active.

---

## Interpreting Results

| Result | Meaning |
|--------|---------|
| Process found + network blocked + filesystem denied | Fully protected |
| Process found but tests fail | Config issue |
| No process found | Daemon not sandboxed |

---

## If Sandbox Is Not Active

### Re-run the Patch Script

```bash
# Stop daemon
launchctl bootout gui/$(id -u)/ai.openclaw.gateway

# Re-patch
python3 ~/.claude/plugins/run-openclaw-srt/skills/openclaw-srt-setup/scripts/patch-plist.py

# Restart
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist

# Verify
ps aux | grep "srt.*settings"
```

### Common Reasons Sandbox Is Missing

| Issue | Cause | Fix |
|-------|-------|-----|
| Plist not patched | `openclaw daemon install --force` overwrote it | Re-run patch script |
| SRT not found | PATH issue in launchd environment | Use absolute path in plist |
| Config not found | Relative path in plist | Use absolute path |
| Old plist cached | Plist not reloaded | Bootout and bootstrap |

---

## Quick Reference

```bash
# Quick check
ps aux | grep "srt.*settings" | grep -v grep

# Full verification
bash ~/.claude/plugins/run-openclaw-srt/skills/openclaw-srt-setup/scripts/verify-sandbox.sh

# Fix if needed
launchctl bootout gui/$(id -u)/ai.openclaw.gateway
python3 ~/.claude/plugins/run-openclaw-srt/skills/openclaw-srt-setup/scripts/patch-plist.py
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```
