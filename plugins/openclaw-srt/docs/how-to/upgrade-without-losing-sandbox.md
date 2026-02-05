# How to Upgrade OpenClaw Without Losing the Sandbox

**When you need this:** Updating OpenClaw to a new version.

**What this prevents:** Losing SRT protection during the upgrade.

**Time:** 3-5 minutes

---

## Quick One-Liner

For routine upgrades:

```bash
launchctl bootout gui/$(id -u)/ai.openclaw.gateway && \
bun update -g openclaw && \
python3 ~/.claude/plugins/openclaw-srt/skills/openclaw-srt-setup/scripts/patch-plist.py && \
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist && \
ps aux | grep "srt.*settings" | grep -v grep
```

If you see SRT in the output, you're done.

---

## Why This Is Necessary

**The problem:** Running `openclaw daemon install --force` (which happens during some upgrade flows) overwrites the launchd plist. This removes the SRT wrapper.

**The result:** Your daemon runs without sandbox protection until you re-patch.

**The fix:** Always re-patch after daemon reinstalls.

---

## Step-by-Step Upgrade

### 1. Stop the Daemon

```bash
launchctl bootout gui/$(id -u)/ai.openclaw.gateway
```

### 2. Upgrade OpenClaw

Using bun (preferred):
```bash
bun update -g openclaw
```

Using npm:
```bash
npm update -g openclaw
```

### 3. Reinstall Daemon (If Required)

If the upgrade asks you to reinstall the daemon:
```bash
openclaw daemon install --force
```

**Warning:** This removes the SRT wrapper. Step 4 restores it.

### 4. Re-Patch the Plist

```bash
python3 ~/.claude/plugins/openclaw-srt/skills/openclaw-srt-setup/scripts/patch-plist.py
```

**Expected output:**
```
Patching ~/Library/LaunchAgents/ai.openclaw.gateway.plist...
[OK] Plist patched successfully
```

### 5. Restart the Daemon

```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

### 6. Verify Sandbox Is Active

```bash
ps aux | grep "srt.*settings" | grep -v grep
```

**Expected:** A line showing the SRT wrapper.

Full verification:
```bash
bash ~/.claude/plugins/openclaw-srt/skills/openclaw-srt-setup/scripts/verify-sandbox.sh
```

---

## Create an Upgrade Script (Recommended)

Save this as `~/bin/upgrade-openclaw.sh`:

```bash
#!/bin/bash
set -euo pipefail

echo "=== Upgrading OpenClaw with Sandbox ==="

echo "Stopping daemon..."
launchctl bootout gui/$(id -u)/ai.openclaw.gateway 2>/dev/null || true

echo "Upgrading OpenClaw..."
bun update -g openclaw

echo "Re-patching plist..."
python3 ~/.claude/plugins/openclaw-srt/skills/openclaw-srt-setup/scripts/patch-plist.py

echo "Starting daemon..."
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist

echo "Verifying sandbox..."
sleep 2
if ps aux | grep -q "srt.*settings"; then
    echo "[OK] Sandbox active"
    openclaw status --all
else
    echo "[FAIL] Sandbox not detected - check manually"
    exit 1
fi
```

Make it executable:
```bash
chmod +x ~/bin/upgrade-openclaw.sh
```

Then just run:
```bash
~/bin/upgrade-openclaw.sh
```

---

## What Could Go Wrong

| Symptom | Cause | Fix |
|---------|-------|-----|
| Daemon not starting | Upgrade broke something | Check `openclaw doctor` |
| Sandbox not active after upgrade | Forgot to re-patch | Run patch script |
| Patch script fails | SRT path changed | Reinstall SRT or update path |
| "Port in use" error | Old daemon still running | `pkill -9 -f "openclaw.*gateway"` |

---

## Checking After Auto-Updates

If OpenClaw auto-updates, verify the sandbox is still active:

```bash
ps aux | grep "srt.*settings" | grep -v grep
```

If empty, re-patch:

```bash
python3 ~/.claude/plugins/openclaw-srt/skills/openclaw-srt-setup/scripts/patch-plist.py
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway
```

---

## Quick Reference

```bash
# Stop
launchctl bootout gui/$(id -u)/ai.openclaw.gateway

# Upgrade
bun update -g openclaw

# Re-patch
python3 ~/.claude/plugins/openclaw-srt/skills/openclaw-srt-setup/scripts/patch-plist.py

# Restart
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist

# Verify
ps aux | grep "srt.*settings"
```
