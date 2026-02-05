# Tutorial: Set Up Telegram Bot with Pairing

**The Benefit**: Message Claude from your phone using Telegram. The pairing system ensures only devices you approve can use your OpenClaw instance.

**Time:** 10-15 minutes
**Prerequisites:** Working sandboxed OpenClaw (see [First Sandboxed OpenClaw](first-sandboxed-openclaw.md))
**Outcome:** A Telegram bot that connects to Claude, with access control via pairing codes

---

## What You Will Build

A setup where:
- You message your Telegram bot, Claude responds
- New devices get a pairing code (not automatic access)
- You approve devices from your terminal
- You can revoke devices anytime

**Pairing in brief:** When a new Telegram user messages your bot, they get a random code. You run a command with that code to grant access. This prevents strangers from using your bot even if they know its username.

---

## Step 1: Create Your Bot with BotFather

1. Open Telegram (mobile or desktop)
2. Search for `@BotFather` (the official bot for creating bots)
3. Tap **Start** or send `/start`
4. Send `/newbot`

BotFather will ask two questions:

**Question 1: "What name should I give your bot?"**
- This is the display name users see
- Example: `My AI Assistant`

**Question 2: "Choose a username for your bot"**
- Must end in `bot`
- Must be unique globally
- Example: `myassistant_2024_bot`

**What to look for after completion:**

```
Done! Congratulations on your new bot. You will find it at t.me/myassistant_2024_bot.

Use this token to access the HTTP API:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

Keep your token secure and store it safely, it can be used by anyone to control your bot.
```

**Copy and save the token** - you will need it next.

---

## Step 2: Configure OpenClaw for Telegram

Enable Telegram and set pairing mode:

```bash
# Enable Telegram channel
openclaw config set channels.telegram.enabled true

# Set your bot token (replace with your actual token)
openclaw config set channels.telegram.botToken "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"

# Set DM policy to pairing (recommended for security)
openclaw config set channels.telegram.dmPolicy "pairing"
```

**Expected output:** No output means success. Errors will display clearly.

**dmPolicy "pairing"** means new users must enter a pairing code. Alternative is "open" (anyone can message) or "allowlist" (specific user IDs only).

---

## Step 3: Verify SRT Allows Telegram

Check that `api.telegram.org` is in your network allowlist:

```bash
grep "telegram" ~/.srt-settings.json
```

**Expected output:**
```
    "api.telegram.org",
```

All provided SRT templates include this domain. If you created a custom config without it, add:

```json
"allowedDomains": [
  "api.telegram.org",
  ...your other domains
]
```

---

## Step 4: Restart the Gateway

Restart to pick up the Telegram configuration:

```bash
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway
```

Wait a few seconds, then verify:

```bash
openclaw status --all
```

**What to look for:**

```
Provider: anthropic · claude-sonnet-4-20250514 · API key (sha256:abc... · len 108)
Gateway: local · ws://127.0.0.1:18789 · reachable
Telegram: ON · OK · token config (sha256:def... · len 46)
                  ^^^^^^^^^^^
                  Look for "OK" here
```

If you see `Telegram: ON · error`, check:
- Bot token is correct
- `api.telegram.org` is in your SRT allowlist
- Logs: `tail -20 ~/.openclaw/logs/gateway.err.log`

---

## Step 5: Get Your Pairing Code

1. Open Telegram
2. Search for your bot's username (e.g., `@myassistant_2024_bot`)
3. Tap the bot in search results
4. Tap **Start** or send any message

**What to look for:**

The bot replies with a pairing challenge:

```
OpenClaw: access not configured.
Your Telegram user id: 9876543210
Pairing code: ABC12345

Ask your admin to run:
openclaw pairing approve telegram ABC12345
```

This is expected. The bot is saying "I don't know you yet - get approval first."

---

## Step 6: Approve the Pairing

In your terminal, run the command shown in the Telegram message:

```bash
openclaw pairing approve telegram ABC12345
```

**Expected output:**
```
Approved pairing for telegram user 9876543210
```

**What happened:** Your OpenClaw instance stored the association between your Telegram user ID and "approved" status.

---

## Step 7: Test the Connection

Go back to Telegram and send a message to your bot:

```
Hello! Can you tell me a joke?
```

**Expected:**
- The bot shows "typing..." indicator
- A response from Claude appears
- The conversation continues naturally

You're done. Your phone now has a direct line to Claude through your sandboxed OpenClaw.

---

## Step 8: Test Network Security (Optional)

Ask the bot to access a blocked domain:

```
Can you fetch https://malicious-site-example.com and tell me what's there?
```

**Expected:** The request fails because the domain is not in your `allowedDomains`.

This confirms the sandbox works even through Telegram - the bot can't exfiltrate data through arbitrary domains.

---

## Managing Paired Devices

**List all paired devices:**
```bash
openclaw pairing list
```

**Revoke a device:**
```bash
openclaw pairing revoke <DEVICE_ID>
```

**Add another device:**

Message the bot from the new device - it will prompt for pairing again. Approve with the new code.

---

## What You Built

You now have:

1. **Telegram bot** connected to your AI assistant
2. **Pairing-based access control** - only approved users can interact
3. **Network sandboxing** - the bot can't reach arbitrary domains
4. **Device management** - approve and revoke access anytime

## Next Steps

- **Add group chat support:** `openclaw config set channels.telegram.groupPolicy "allowlist"`
- **Enable streaming:** `openclaw config set channels.telegram.streamMode "partial"`
- **Customize domains:** Edit `~/.srt-settings.json` for your use case

## Troubleshooting

**Bot not responding at all**
```bash
# Check status
openclaw status --all | grep -i telegram

# Check logs
tail -20 ~/.openclaw/logs/gateway.err.log
```

**"Unauthorized" error in logs**

Token may be wrong or revoked. Get a new token:
1. Message BotFather
2. Send `/mybots`
3. Select your bot
4. Tap "API Token"

**Pairing code not appearing**
```bash
# Check DM policy
openclaw config get channels.telegram.dmPolicy
# Should show: pairing

# Check if already paired
openclaw pairing list
```

**Messages delayed**

Check `streamMode` setting and network latency to `api.telegram.org`.
