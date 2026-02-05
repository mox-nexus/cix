# SRT + OpenClaw Gotchas

Hard-won lessons from real debugging sessions.

## 1. The `--` Separator (Critical)

**Symptom:** Network requests blocked even though domain is in `allowedDomains`.

**Root cause:** SRT CLI uses Commander.js which doesn't stop parsing at positional arguments. If your wrapped command has flags like `-s`, `-c`, `-d`, they may be interpreted as SRT options.

**Example failure:**
```bash
# BAD - curl's -s gets eaten as SRT's --settings short flag
srt --settings ~/.srt-settings.json curl -s https://api.telegram.org

# What actually happens:
#   1. Commander sees "-s" and interprets as --settings
#   2. "https://api.telegram.org" becomes the settings path
#   3. Config fails to load, falls back to empty allowlist
#   4. ALL network blocked
```

**Solution:**
```bash
# GOOD - double-dash tells parser "everything after this is the command"
srt --settings ~/.srt-settings.json -- curl -s https://api.telegram.org
```

**Alternative:**
```bash
# Also works - use -c for command string mode
srt --settings ~/.srt-settings.json -c 'curl -s https://api.telegram.org'
```

**For daemons:** The plist patch script adds `--` by default. Commands like `node /path/script --port 18789` don't usually conflict, but `--` adds safety.

**How we found this:** Wolf (structured problem-solving agent) identified that Commander.js was eating the `-s` flag after hours of debugging. The key insight: "if it worked with `-v` but fails with `-s`, the difference IS the flag being parsed."

---

## 2. Wildcard Domains Don't Match Base Domain

**Symptom:** `*.linkedin.com` allowed but `linkedin.com` blocked.

**Root cause:** SRT's `matchesDomainPattern` function:
```typescript
if (pattern.startsWith('*.')) {
  const baseDomain = pattern.substring(2)
  return hostname.endsWith('.' + baseDomain)  // Note: requires the dot!
}
```

The `*.example.com` pattern only matches `www.example.com`, `api.example.com`, etc. NOT `example.com` itself.

**Solution:** Always include both:
```json
"allowedDomains": [
  "linkedin.com",
  "*.linkedin.com"
]
```

---

## 3. sandbox-exec Doesn't Appear in ps

**Symptom:** Can't find `sandbox-exec` in process list, worried sandbox isn't active.

**Why:** macOS's `sandbox-exec` uses the POSIX `exec` pattern - it replaces itself with the target process. The sandbox restrictions persist at kernel level even after the binary exits.

**How to verify sandbox is active:**
```bash
# Check SRT is running with --settings
ps aux | grep "srt.*settings" | grep -v grep

# You should see:
# srt --settings ~/.srt-settings.json -- /opt/homebrew/bin/node ... gateway
```

The seatbelt profile was applied before the child process started. It's enforced by macOS kernel, not by a running process.

---

## 4. Old Gateway Blocking New Daemon

**Symptom:** New daemon can't start, "port 18789 already in use", but `launchctl print` shows it's not running.

**Root cause:** A manually-started gateway (e.g., from testing `srt "openclaw gateway..."`) is still running.

**Solution:**
```bash
# Find the culprit
lsof -i :18789

# Kill it
kill -9 <PID>

# Or kill by pattern
pkill -9 -f "openclaw.*gateway"

# Restart proper daemon
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway
```

---

## 5. Config Not Loading (Silent Failure)

**Symptom:** SRT runs but network is completely blocked. Debug shows empty allowedDomains.

**Possible causes:**

1. **Wrong path:** Config file doesn't exist at specified path
   ```bash
   ls -la ~/.srt-settings.json
   ```

2. **JSON syntax error:** Invalid JSON silently falls back to defaults
   ```bash
   python3 -m json.tool ~/.srt-settings.json
   ```

3. **Path has spaces:** Quote the path
   ```bash
   srt --settings "/Users/My Name/.srt-settings.json" -- ...
   ```

---

## 6. Plist Lost After Upgrade

**Symptom:** After `npm update -g openclaw`, sandbox stops working.

**Root cause:** `openclaw daemon install --force` overwrites the plist, removing the SRT wrapper.

**Solution:** Re-run the patch script after upgrades:
```bash
launchctl bootout gui/$(id -u)/ai.openclaw.gateway
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/patch-plist.py
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

---

## 7. Two curl Progress Bars

**Symptom:** When running curl through SRT, you see TWO progress bars - one succeeds (downloads "Connection blocked" message), one fails with 403.

**What's happening:** This is actually the `--` separator issue (#1). The first "request" is curl trying to connect, the second is the actual request getting blocked.

**Solution:** Add `--` separator.

---

## 8. Debug Output Not Appearing

**Symptom:** Running with `-d` flag but no `[SandboxDebug]` output.

**Solution:** Set environment variable:
```bash
DEBUG=1 srt -d --settings ~/.srt-settings.json -- echo "test"
```

Both `-d` flag AND `DEBUG=1` may be needed depending on version.

---

## Quick Diagnostic Checklist

When something isn't working:

1. **Is config loading?**
   ```bash
   DEBUG=1 srt -d --settings ~/.srt-settings.json -- echo "test" 2>&1 | grep allowedHosts
   ```

2. **Is the domain in allowlist?** (Check both base and wildcard)

3. **Is `--` separator present?** (Check for flag collision)

4. **Is process actually sandboxed?**
   ```bash
   ps aux | grep "srt.*settings"
   ```

5. **Is the right config file being used?** (Absolute paths)
