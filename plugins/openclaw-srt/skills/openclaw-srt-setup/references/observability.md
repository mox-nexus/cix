# Observability

## SRT Debug

```bash
# One-time
DEBUG=1 srt -d --settings ~/.srt-settings.json -- echo "test" 2>&1

# Check config loaded
DEBUG=1 srt -d ... 2>&1 | grep allowedHosts
```

## Log Locations

| Log | Path |
|-----|------|
| Gateway | `~/.openclaw/logs/gateway.log` |
| Gateway errors | `~/.openclaw/logs/gateway.err.log` |
| launchd | `log show --predicate 'subsystem == "com.apple.launchd"'` |

## What to Monitor

| Signal | Where | Indicates |
|--------|-------|-----------|
| "Connection blocked" | gateway.err.log | Domain not in allowlist |
| 403 responses | gateway.log | Proxy rejecting |
| `srt.*settings` in ps | Process list | Sandbox wrapper active |
| Permission denied | gateway.err.log | Filesystem rule triggered |

## Quick Health Check

```bash
openclaw status --all
# Expected: Gateway reachable, Telegram OK
```

## Debug Network Issues

```bash
# Is domain in allowlist?
grep "example.com" ~/.srt-settings.json

# Is proxy active?
srt --settings ... -- env | grep -i proxy
# Should show HTTP_PROXY, HTTPS_PROXY
```

## Find Problems

```bash
# Blocked domains
grep -i "blocked\|forbidden\|403" ~/.openclaw/logs/gateway.err.log | sort | uniq -c | sort -rn

# Connection errors
grep -i "ECONNREFUSED\|ETIMEDOUT\|ENOTFOUND" ~/.openclaw/logs/gateway.err.log
```
