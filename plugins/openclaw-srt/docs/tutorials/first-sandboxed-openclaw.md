# Tutorial: Your First Sandboxed OpenClaw

**The Problem**: AI assistants with file and network access can read your SSH keys, AWS credentials, and exfiltrate data. This tutorial shows you how to run OpenClaw where it can't touch your secrets.

**Time:** 15-20 minutes
**Prerequisites:** macOS or Linux machine, terminal access
**Outcome:** OpenClaw that talks to Claude but can't read `~/.ssh` or reach arbitrary websites

---

## What You Will Build

A working setup where:
- Claude responds to your messages through OpenClaw
- Your credentials stay protected (SSH keys, cloud tokens)
- Network requests only reach approved domains
- You can verify the sandbox is running anytime

---

## Step 1: Check Dependencies

First, verify you have the tools we'll use.

```bash
bash ~/.claude/plugins/openclaw-srt/skills/openclaw-srt-setup/scripts/check-deps.sh
```

**What this does:** Checks for Node.js, bun, OpenClaw, SRT, and Python.

**Expected output (macOS):**
```
=== Checking OpenClaw + SRT Prerequisites ===

[PASS] Node.js 22.6.0 (>= 22 required)
[PASS] bun 1.1.42 found
[PASS] OpenClaw 0.4.2 found
[PASS] SRT @anthropic-ai/sandbox-runtime found at /Users/you/.bun/bin/srt
[PASS] Python3 3.12.0 found (for plist patching)

All prerequisites satisfied!
```

If anything shows `[FAIL]`, install the missing dependency:

| Missing | Install Command |
|---------|----------------|
| Node.js | `brew install node@22` |
| bun | `curl -fsSL https://bun.sh/install \| bash` |
| OpenClaw | `bun install -g openclaw` |
| SRT | `bun install -g @anthropic-ai/sandbox-runtime` |

**SRT** is Anthropic's Sandbox Runtime - it wraps processes to restrict what they can access.

---

## Step 2: Run the Installer

The installer creates directories, configures OpenClaw, and wraps it with SRT.

```bash
bash ~/.claude/plugins/openclaw-srt/skills/openclaw-srt-setup/scripts/install.sh
```

**What this does:**
1. Creates `~/.openclaw/` for config and logs
2. Generates a secure token for the web interface
3. Copies the SRT sandbox rules to `~/.srt-settings.json`
4. Patches the daemon to run inside SRT (this is the key part)
5. Starts the sandboxed daemon

**Expected output:**
```
=== OpenClaw + SRT Installer ===
Detected: macOS

Step 1/6: Creating directories...
  [OK] ~/.openclaw/credentials
  [OK] ~/.openclaw/logs

Step 2/6: Running OpenClaw doctor...
  [OK] Initial config created

Step 3/6: Configuring gateway...
  [OK] Gateway token generated

Step 4/6: Installing SRT config...
  [OK] ~/.srt-settings.json installed

Step 5/6: Installing daemon with SRT wrapper...
  [OK] Daemon plist patched
  [OK] Daemon started

Step 6/6: Verifying...
  [OK] Process running with SRT wrapper
  [OK] Gateway reachable

Installation complete!

Control UI: http://127.0.0.1:18789/?token=YOUR_TOKEN_HERE
```

**The key piece:** Step 5 modifies the **daemon plist** (macOS service definition) to launch OpenClaw through SRT instead of directly. The plist tells launchd (macOS service manager) how to start OpenClaw.

---

## Step 3: Verify the Sandbox is Active

Confirm SRT is actually wrapping OpenClaw.

```bash
bash ~/.claude/plugins/openclaw-srt/skills/openclaw-srt-setup/scripts/verify-sandbox.sh
```

**What this does:** Runs 4 tests to prove the sandbox is working.

**Expected output:**
```
========================================
  SRT Sandbox Verification
========================================

OS: Darwin

--- Test 1: Sandbox Process Detection ---

[PASS] SRT wrapper process found (PID: 12345)
[INFO] Process details:
     12345  1234 /Users/you/.bun/bin/srt --settings /Users/you/.srt-settings.json -- ...

--- Test 2: Network Filtering ---

[INFO] Testing network filtering by attempting blocked domain...
[PASS] Network filtering working (blocked domain rejected)
[INFO] Testing allowed domain (api.anthropic.com)...
[PASS] Allowed domain reachable (HTTP 401)

--- Test 3: Filesystem Restrictions ---

[INFO] Testing filesystem restriction on /Users/you/.ssh...
[PASS] Filesystem restriction working (/Users/you/.ssh blocked)
[PASS] Allowed write path working (/tmp)

--- Test 4: Config Validation ---

[PASS] Config file exists at ~/.srt-settings.json
[PASS] Config JSON syntax valid
[INFO] Approximately 47 domains configured

========================================
  Summary
========================================

Sandbox verification PASSED
```

**What each test proves:**
- **Test 1:** The daemon is wrapped by SRT (not running directly)
- **Test 2:** Network requests to random domains fail
- **Test 3:** Reading `~/.ssh` is blocked (your keys are safe)
- **Test 4:** The config file is valid JSON

---

## Step 4: Add Claude Credentials

OpenClaw needs an API key or OAuth token to talk to Claude.

**Option A: API Key** (simpler if you have one)

```bash
openclaw config set providers.anthropic.apiKey "sk-ant-api03-YOUR-KEY-HERE"
```

**Option B: OAuth Token** (for Anthropic Console users)

```bash
cat > ~/.openclaw/credentials/oauth.json << 'EOFCREDS'
{
  "anthropic": {
    "oauthToken": "YOUR_OAUTH_TOKEN_HERE"
  }
}
EOFCREDS
```

Restart the daemon to pick up the credentials:

```bash
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway
```

**launchctl** is macOS's service manager. This command restarts the OpenClaw daemon.

---

## Step 5: Send Your First Message

Get your gateway token (the password for the web UI):

```bash
openclaw config get gateway.auth.token
```

Open the Control UI in your browser:

```
http://127.0.0.1:18789/?token=YOUR_TOKEN_HERE
```

Send a test message: "Hello, what can you help me with?"

**Expected:** Claude responds through the sandboxed gateway.

**What's happening:**
1. Your browser sends the message to OpenClaw (localhost only)
2. OpenClaw sends it to Claude's API through the SRT proxy
3. SRT checks: Is `api.anthropic.com` in the approved list? Yes, allow.
4. Claude responds, OpenClaw shows it to you

---

## Step 6: Test Network Restrictions

Try asking Claude to access a domain not in the approved list:

> "Can you fetch the contents of https://example-malicious-site.com?"

**Expected:** The request fails with a network error.

**Why:** The SRT proxy blocks domains not in `allowedDomains` (in `~/.srt-settings.json`).

This confirms your setup works - even if Claude tried to exfiltrate data (or you accidentally prompted it to), blocked domains return errors.

---

## What You Built

You now have:

1. **Sandboxed OpenClaw** - The AI runs in a restricted environment
2. **Protected credentials** - SSH keys, AWS tokens, etc. are unreadable by OpenClaw
3. **Network allowlist** - Only approved domains are reachable
4. **Verification tools** - Scripts to confirm the sandbox anytime

## Next Steps

- **Add Telegram:** [Telegram Bot Setup Tutorial](telegram-bot-setup.md)
- **Add more domains:** See [How to Add a Domain](../how-to/add-domain.md)
- **Understand how it works:** [Architecture Explanation](../explanation/architecture.md)

## Troubleshooting

**"Port 18789 already in use"**
```bash
lsof -i :18789
kill -9 <PID>
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway
```

**"Sandbox not detected"**
```bash
# Re-run the patch script
python3 ~/.claude/plugins/openclaw-srt/skills/openclaw-srt-setup/scripts/patch-plist.py
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway
```

**Network requests failing for allowed domains**

The `--` separator might be missing. See [Troubleshoot Blocked Request](../how-to/troubleshoot-blocked-request.md) for the fix.
