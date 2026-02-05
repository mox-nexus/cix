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

**Corollary:** You cannot use `*.example.com` alone expecting it to match everything. The base domain requires an explicit entry.

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

**Symptom:** After `npm update -g openclaw` or `bun update -g openclaw`, sandbox stops working.

**Root cause:** `openclaw daemon install --force` overwrites the plist, removing the SRT wrapper.

**Solution:** Re-run the patch script after upgrades:
```bash
launchctl bootout gui/$(id -u)/ai.openclaw.gateway
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/patch-plist.py
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

**Prevention:** Create a wrapper script that always patches after install:
```bash
#!/bin/bash
# upgrade-openclaw.sh
bun update -g openclaw
python3 ~/.claude/plugins/openclaw-srt/skills/openclaw-srt-setup/scripts/patch-plist.py
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway
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

## 9. HTTPS Upgrade Issues

**Symptom:** HTTP requests work but HTTPS silently fails or hangs.

**Root cause:** Some sites aggressively redirect HTTP to HTTPS. The SRT proxy handles both, but:
1. CONNECT tunneling for HTTPS is different from HTTP proxy
2. Some corporate networks inspect HTTPS and break the tunnel
3. HTTP_PROXY vs HTTPS_PROXY environment variables

**Debug steps:**
```bash
# Test HTTP explicitly
srt --settings ~/.srt-settings.json -- curl -v http://example.com

# Test HTTPS explicitly  
srt --settings ~/.srt-settings.json -- curl -v https://example.com

# Check proxy environment
srt --settings ~/.srt-settings.json -- env | grep -i proxy
```

**Solution:** Ensure both HTTP and HTTPS proxy are configured. SRT should set both `HTTP_PROXY` and `HTTPS_PROXY` to the same local proxy.

---

## 10. Certificate Pinning Apps Bypass Proxy

**Symptom:** App works outside sandbox but fails inside, or requests bypass filtering entirely.

**Root cause:** Some applications implement certificate pinning and refuse to connect through proxies. Others don't respect `HTTP_PROXY` environment variables at all.

**Examples:**
- Native macOS apps may use Network.framework directly
- Electron apps with custom network code
- Apps that shell out to other binaries

**Detection:**
```bash
# If request succeeds but shouldn't (domain not in allowlist)
# the app is bypassing the proxy
srt --settings ~/.srt-settings.json -- ./suspicious-app

# Monitor actual network traffic
sudo tcpdump -i any port 443 | grep -v localhost
```

**Mitigation:**
- SRT's filesystem restrictions still apply
- Consider using `--unshare-net` (Linux) for true network isolation
- On macOS, seatbelt network rules can block by IP (but not domain)

---

## 11. Subprocess Inheritance

**Symptom:** Main process is sandboxed but child processes it spawns appear to bypass restrictions.

**How it actually works:**

**Filesystem restrictions (sandbox-exec/bwrap):**
- Child processes inherit the sandbox
- Kernel enforces restrictions regardless of exec chain
- Spawning `bash`, `python`, etc. stays sandboxed

**Network restrictions (proxy):**
- Depends on environment variable inheritance
- Most shells/runtimes pass env vars to children
- Some runtimes (Java, Go) may ignore `HTTP_PROXY`

**Verification:**
```bash
# Test that child processes are sandboxed
srt --settings ~/.srt-settings.json -- bash -c 'cat ~/.ssh/id_rsa'
# Should fail with permission denied

# Test env var inheritance
srt --settings ~/.srt-settings.json -- bash -c 'python3 -c "import os; print(os.environ.get(\"HTTP_PROXY\"))"'
# Should show the proxy URL
```

**Edge case:** If a child process explicitly unsets `HTTP_PROXY` or uses custom network code, it could bypass network filtering. Filesystem restrictions remain.

---

## 12. Debug Mode Disabling Sandbox

**Symptom:** Debug mode (`-d` flag) changes sandbox behavior.

**What debug mode does:**
- Prints configuration being applied
- Shows proxy setup
- Logs network requests
- May change timing/ordering

**What debug mode does NOT do:**
- Disable filesystem sandbox
- Disable network proxy
- Change security guarantees

**Troubleshooting workflow:**
```bash
# Step 1: Run without sandbox to verify command works
curl -s https://allowed-domain.com

# Step 2: Run with sandbox and debug to see what's happening
DEBUG=1 srt -d --settings ~/.srt-settings.json -- curl -s https://allowed-domain.com

# Step 3: If step 1 works but step 2 fails, the issue is sandbox config
# If both fail, the issue is elsewhere (network, auth, etc.)
```

---

## 13. Multiple SRT Instances

**Symptom:** Strange behavior when running multiple sandboxed commands simultaneously.

**How SRT handles concurrency:**
- Each invocation starts its own proxy servers
- Proxy ports are dynamically assigned
- Filesystem sandbox is per-process

**Potential issues:**
- Port exhaustion with many parallel instances
- Race conditions in proxy startup
- Overlapping Unix sockets (Linux)

**Solution:** For high concurrency, consider:
```bash
# Sequential execution
command1 && command2

# Or use a single long-running sandboxed shell
srt --settings ~/.srt-settings.json -- bash
# Then run commands within that shell
```

---

## 14. Homebrew Path Issues (macOS)

**Symptom:** SRT works but wrapped command fails with "command not found".

**Root cause:** The sandboxed environment may not have the same PATH as your interactive shell. Homebrew on Apple Silicon installs to `/opt/homebrew/bin` which may not be in the default PATH.

**Solution:** Use absolute paths:
```bash
# BAD
srt --settings ~/.srt-settings.json -- node script.js

# GOOD  
srt --settings ~/.srt-settings.json -- /opt/homebrew/bin/node script.js
```

The plist patch script should use absolute paths for the OpenClaw binary.

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

6. **Is JSON valid?**
   ```bash
   python3 -m json.tool ~/.srt-settings.json
   ```

7. **Is the daemon running the patched plist?**
   ```bash
   launchctl print gui/$(id -u)/ai.openclaw.gateway | grep ProgramArguments -A 10
   ```

8. **Any proxy-bypassing apps?**
   ```bash
   sudo tcpdump -i any port 443 | grep -v localhost
   ```
