# macOS Setup

OpenClaw + SRT on macOS using launchd.

## Prerequisites

| Tool | Install | Common Path |
|------|---------|-------------|
| Node.js 22+ | `brew install node@22` | /opt/homebrew/bin/node |
| OpenClaw | `npm install -g openclaw` | varies |
| SRT | `npm install -g @anthropic-ai/sandbox-runtime` | ~/.bun/bin/srt |

**Find srt:** `which srt` — you'll need the full path for the plist patch.

## Step 1: Initialize OpenClaw

```bash
# Create state directory
mkdir -p ~/.openclaw/credentials ~/.openclaw/logs

# Run doctor to create initial config
openclaw doctor
```

## Step 2: Configure Authentication

### Option A: Anthropic Max (OAuth)

```bash
# Get OAuth token from: https://console.anthropic.com/settings/oauth-tokens
# Create credentials file
cat > ~/.openclaw/credentials/oauth.json << 'EOF'
{
  "anthropic": {
    "oauthToken": "YOUR_OAUTH_TOKEN_HERE"
  }
}
EOF
```

### Option B: API Key

```bash
openclaw config set providers.anthropic.apiKey "sk-ant-api03-..."
```

## Step 3: Configure Gateway

```bash
# Generate secure gateway token
openclaw config set gateway.auth.token "$(openssl rand -hex 16)"

# Set local mode
openclaw config set gateway.mode "local"

# Get your token for later
openclaw config get gateway.auth.token
```

## Step 4: Create SRT Config

Choose a template from `templates/` or create custom:

```bash
# Copy template (pick one that fits your use case)
cp ${CLAUDE_PLUGIN_ROOT}/templates/srt-settings.json ~/.srt-settings.json

# Or for minimal setup
cp ${CLAUDE_PLUGIN_ROOT}/templates/srt-minimal.json ~/.srt-settings.json

# Edit to customize domains
nano ~/.srt-settings.json
```

## Step 5: Install Daemon

```bash
# Install LaunchAgent (creates plist)
openclaw daemon install

# Verify plist was created
ls -la ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

## Step 6: Stop Daemon for Patching

```bash
# Stop the unsandboxed daemon
launchctl bootout gui/$(id -u)/ai.openclaw.gateway 2>/dev/null || true
```

## Step 7: Add SRT Wrapper

```bash
# Run the patch script
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/patch-plist.py

# Or with custom paths
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/patch-plist.py \
  --srt-path ~/.bun/bin/srt \
  --srt-config ~/.srt-settings.json
```

**What the patch does:**

Before:
```xml
<array>
  <string>/opt/homebrew/bin/node</string>
  <string>/opt/homebrew/lib/node_modules/openclaw/dist/index.js</string>
  <string>gateway</string>
  <string>--port</string>
  <string>18789</string>
</array>
```

After:
```xml
<array>
  <string>/Users/you/.bun/bin/srt</string>
  <string>--settings</string>
  <string>/Users/you/.srt-settings.json</string>
  <string>--</string>
  <string>/opt/homebrew/bin/node</string>
  <string>/opt/homebrew/lib/node_modules/openclaw/dist/index.js</string>
  <string>gateway</string>
  <string>--port</string>
  <string>18789</string>
</array>
```

## Step 8: Start Sandboxed Daemon

```bash
# Load and start
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist

# Verify it started
launchctl print gui/$(id -u)/ai.openclaw.gateway | head -20
```

## Step 9: Verify Setup

```bash
# Run verification script
bash ${CLAUDE_PLUGIN_ROOT}/scripts/verify-sandbox.sh

# Or manually:

# Check SRT is in the process
ps aux | grep "srt.*settings" | grep -v grep

# Check port is bound
lsof -i :18789

# Check OpenClaw status
openclaw status --all
```

Expected output:
```
Gateway: local · ws://127.0.0.1:18789 · reachable
Telegram: ON · OK (if configured)
Gateway service: LaunchAgent installed · loaded · running
```

## Step 10: Access Control UI

Open in browser (include your gateway token):

```
http://127.0.0.1:18789/?token=YOUR_GATEWAY_TOKEN
```

Get your token:
```bash
openclaw config get gateway.auth.token
```

## Service Management

```bash
# Restart
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway

# Stop
launchctl bootout gui/$(id -u)/ai.openclaw.gateway

# Start
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist

# Check status
launchctl print gui/$(id -u)/ai.openclaw.gateway

# View logs
tail -f ~/.openclaw/logs/gateway.log
tail -f ~/.openclaw/logs/gateway.err.log
```

## After OpenClaw Upgrades

When you upgrade OpenClaw (`npm update -g openclaw`), if you run `openclaw daemon install --force`, the plist gets overwritten and loses the SRT wrapper.

**Re-apply after upgrades:**

```bash
# Stop
launchctl bootout gui/$(id -u)/ai.openclaw.gateway

# Re-patch
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/patch-plist.py

# Restart
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist

# Verify
ps aux | grep "srt.*settings"
```

## Troubleshooting

### "Port 18789 already in use"

```bash
# Find what's using it
lsof -i :18789

# Kill if stale
kill -9 <PID>

# Or kill by pattern
pkill -9 -f "openclaw.*gateway"
```

### Daemon not starting

```bash
# Check launchd errors
launchctl print gui/$(id -u)/ai.openclaw.gateway

# Check logs
tail -50 ~/.openclaw/logs/gateway.err.log

# Common issues:
# - srt not found: check PATH in plist
# - config not found: check --settings path
# - permission denied: check file permissions
```

### SRT wrapper not appearing in ps

```bash
# Check the plist has SRT
grep -A3 "ProgramArguments" ~/Library/LaunchAgents/ai.openclaw.gateway.plist

# Should show srt as first argument
```

### Network requests failing

See [gotchas.md](gotchas.md) for the `--` separator issue and domain matching rules.

## Quick Reference

| Task | Command |
|------|---------|
| Status | `openclaw status --all` |
| Restart | `launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway` |
| Stop | `launchctl bootout gui/$(id -u)/ai.openclaw.gateway` |
| Logs | `tail -f ~/.openclaw/logs/gateway.log` |
| Verify sandbox | `ps aux \| grep "srt.*settings"` |
| Gateway token | `openclaw config get gateway.auth.token` |
| Control UI | `http://127.0.0.1:18789/?token=TOKEN` |
