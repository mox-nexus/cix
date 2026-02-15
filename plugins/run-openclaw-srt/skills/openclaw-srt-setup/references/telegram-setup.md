# Telegram Setup

## Create Bot

1. Telegram → `@BotFather` → `/newbot`
2. Choose name and username (must end in `bot`)
3. Save the token (only auth for your bot)

## Configure

```bash
openclaw config set channels.telegram.enabled true
openclaw config set channels.telegram.botToken "TOKEN"
openclaw config set channels.telegram.dmPolicy "pairing"
```

## DM Policy

| Policy | Behavior | Use Case |
|--------|----------|----------|
| `pairing` | Challenge code for unknown users | Personal (recommended) |
| `open` | Anyone can message | Public bots |
| `allowlist` | Only pre-approved IDs | Restricted |

## SRT Config

Ensure `api.telegram.org` in allowedDomains. All templates include it.

## Pair Device

1. Message your bot
2. Bot replies with pairing code
3. `openclaw pairing approve telegram CODE`
4. Done

## Commands

| Task | Command |
|------|---------|
| Enable | `openclaw config set channels.telegram.enabled true` |
| Set token | `openclaw config set channels.telegram.botToken "TOKEN"` |
| Approve | `openclaw pairing approve telegram CODE` |
| List paired | `openclaw pairing list` |
| Revoke | `openclaw pairing revoke DEVICE_ID` |
| Status | `openclaw status --all \| grep telegram` |

## Group Chat

```bash
openclaw config set channels.telegram.groupPolicy "allowlist"
openclaw config set channels.telegram.allowedGroups '[-1001234567890]'
```

| Policy | Behavior |
|--------|----------|
| `disabled` | Ignore all groups |
| `allowlist` | Only listed groups |
| `all` | Any group |

## Troubleshooting

| Problem | Check |
|---------|-------|
| Not responding | `openclaw status --all` |
| Unauthorized | Token correct? `openclaw config get channels.telegram.botToken` |
| No pairing code | Policy set? `openclaw config get channels.telegram.dmPolicy` |
| Already paired? | `openclaw pairing list` |

## Security

- Don't commit bot token to git
- Rotate via BotFather `/revoke`
- Pairing ensures physical access to approve
- With SRT: only `api.telegram.org` reachable
