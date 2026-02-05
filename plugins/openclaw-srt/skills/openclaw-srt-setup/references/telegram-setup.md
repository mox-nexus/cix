# Telegram Setup

Configure OpenClaw to communicate via Telegram bot.

## Create Bot

1. Open Telegram, search for `@BotFather`
2. Send `/newbot`
3. Choose a display name (e.g., "My AI Assistant")
4. Choose a username (must end in `bot`, e.g., `myassistant_bot`)
5. BotFather gives you a token like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

**Save this token securely** - it's the only authentication for your bot.

## Configure OpenClaw

```bash
# Enable Telegram channel
openclaw config set channels.telegram.enabled true

# Set bot token
openclaw config set channels.telegram.botToken "YOUR_BOT_TOKEN"

# Set DM policy (recommended: pairing)
openclaw config set channels.telegram.dmPolicy "pairing"
```

### DM Policy Options

| Policy | Behavior | Use Case |
|--------|----------|----------|
| `pairing` | Unknown users get challenge code to approve | Personal assistant (recommended) |
| `open` | Anyone can message | Public service bots |
| `allowlist` | Only pre-approved user IDs | Highly restricted |

**Recommendation:** Use `pairing` for personal assistants. It prevents random people from issuing commands while allowing you to easily approve new devices.

## Verify SRT Config

Ensure `api.telegram.org` is in your SRT allowlist:

```json
"allowedDomains": [
  "api.telegram.org",
  // ...
]
```

All provided templates include this.

## Start/Restart Gateway

```bash
# Restart to pick up config changes
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway
```

## Verify Connection

```bash
# Check status
openclaw status --all

# Should show:
# Telegram: ON · OK · token config (sha256:xxx · len 46)
```

## Pair Your Device

1. Open Telegram
2. Find your bot (@yourbotusername)
3. Send any message (e.g., "hello")
4. Bot replies with pairing code:
   ```
   OpenClaw: access not configured.
   Your Telegram user id: 1234567890
   Pairing code: ABC12345

   Ask your admin to run:
   openclaw pairing approve telegram ABC12345
   ```
5. Run the approve command:
   ```bash
   openclaw pairing approve telegram ABC12345
   ```
6. Bot confirms pairing
7. Now you can interact normally

## Managing Paired Devices

```bash
# List paired devices
openclaw pairing list

# Revoke a device
openclaw pairing revoke <DEVICE_ID>
```

## Group Chat Setup

By default, OpenClaw only responds in DMs. For group chats:

```bash
# Set group policy
openclaw config set channels.telegram.groupPolicy "allowlist"

# Add specific groups (get group ID by adding bot, it will log the ID)
openclaw config set channels.telegram.allowedGroups '[-1001234567890]'
```

### Group Policy Options

| Policy | Behavior |
|--------|----------|
| `disabled` | Bot ignores all groups |
| `allowlist` | Only responds in listed groups |
| `all` | Responds in any group it's added to |

## Stream Mode

Control how responses appear:

```bash
# Partial streaming (shows typing, updates message)
openclaw config set channels.telegram.streamMode "partial"

# Full message only (sends complete response)
openclaw config set channels.telegram.streamMode "complete"
```

## Troubleshooting

### Bot not responding

1. **Check gateway is running:**
   ```bash
   openclaw status --all
   ```

2. **Check Telegram channel status:**
   ```bash
   openclaw status --all | grep -i telegram
   ```
   Should show: `Telegram: ON · OK`

3. **Check logs:**
   ```bash
   grep -i telegram ~/.openclaw/logs/gateway.err.log
   ```

4. **Verify SRT allows Telegram:**
   ```bash
   grep telegram ~/.srt-settings.json
   ```

### "Unauthorized" or connection errors

- **Wrong token:** Double-check token in config
  ```bash
  openclaw config get channels.telegram.botToken
  ```

- **Token revoked:** Get new token from BotFather (`/revoke`, then `/newbot` or `/token`)

### Pairing code not appearing

- **DM policy set wrong:**
  ```bash
  openclaw config get channels.telegram.dmPolicy
  # Should be "pairing"
  ```

- **Already paired:** Check if you're already in the list
  ```bash
  openclaw pairing list
  ```

### Messages delayed

- Check gateway logs for errors
- Verify `streamMode` setting
- Check network latency to `api.telegram.org`

## Security Notes

### Bot Token Security

- **Don't commit to git** - bot token is in `~/.openclaw/openclaw.json`
- **Rotate periodically** - BotFather → `/revoke` → get new token
- **Monitor usage** - check for unexpected messages in logs

### Pairing Security

The pairing flow ensures:
1. You must have physical access to approve codes
2. Unknown users can't issue commands
3. Revocation is instant via `pairing revoke`

### Network Security

With SRT:
- Only `api.telegram.org` is reachable (if in allowlist)
- Other Telegram domains (web, desktop) are blocked
- Bot can't be used to exfiltrate to other endpoints

## Quick Reference

| Task | Command |
|------|---------|
| Enable Telegram | `openclaw config set channels.telegram.enabled true` |
| Set bot token | `openclaw config set channels.telegram.botToken "TOKEN"` |
| Set DM policy | `openclaw config set channels.telegram.dmPolicy "pairing"` |
| Approve pairing | `openclaw pairing approve telegram CODE` |
| List paired | `openclaw pairing list` |
| Revoke device | `openclaw pairing revoke DEVICE_ID` |
| Check status | `openclaw status --all \| grep telegram` |
