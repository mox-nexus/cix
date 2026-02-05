# Observability

Make OpenClaw + SRT behavior visible.

## SRT Debug Logging

### Enable Debug Output

```bash
# One-time test
DEBUG=1 srt -d --settings ~/.srt-settings.json -- echo "test" 2>&1

# See what config was loaded
DEBUG=1 srt -d --settings ~/.srt-settings.json -- echo "test" 2>&1 | grep -E "(allowedHosts|config)"
```

### Persistent Logging for Daemon

Modify the plist to capture SRT debug output:

```bash
# Add to EnvironmentVariables in plist
DEBUG=1
```

Or wrap with logging script:

```bash
#!/bin/bash
# ~/.openclaw/srt-wrapper.sh
exec env DEBUG=1 srt -d --settings ~/.srt-settings.json -- "$@" 2>&1 | \
  tee -a ~/.openclaw/logs/srt-debug.log
```

## What to Monitor

### Network Activity

| Signal | Location | Indicates |
|--------|----------|-----------|
| "Connection blocked" | gateway.err.log | Domain not in allowlist |
| 403 responses | gateway.log | Proxy rejecting requests |
| DNS failures | srt-debug.log | Domain resolution issues |

### Sandbox Activity

| Signal | How to Check | Indicates |
|--------|--------------|-----------|
| `srt.*settings` in ps | `ps aux \| grep srt` | Sandbox wrapper active |
| Permission denied | gateway.err.log | Filesystem rule triggered |
| Proxy env vars | Process environment | Network filtering active |

### OpenClaw Status

```bash
# Quick health check
openclaw status --all

# Expected output when healthy:
# Gateway: local · ws://127.0.0.1:18789 · reachable
# Telegram: ON · OK
# Gateway service: LaunchAgent installed · loaded · running
```

## Log Locations

| Log | Path | Contains |
|-----|------|----------|
| Gateway | `~/.openclaw/logs/gateway.log` | Normal operation |
| Gateway errors | `~/.openclaw/logs/gateway.err.log` | Errors, blocked requests |
| SRT debug | `~/.openclaw/logs/srt-debug.log` | Sandbox activity (if configured) |
| launchd | `log show --predicate 'subsystem == "com.apple.launchd"'` | Service start/stop |

## Debugging Network Issues

### Is the domain in allowlist?

```bash
grep "example.com" ~/.srt-settings.json
```

Remember: `*.example.com` does NOT match `example.com`.

### Is config loading?

```bash
DEBUG=1 srt -d --settings ~/.srt-settings.json -- curl -s https://api.anthropic.com 2>&1 | head -20
```

Look for `allowedHosts` in output.

### Is proxy active?

```bash
# Inside sandboxed process, these should be set:
env | grep -i proxy
# HTTP_PROXY=http://127.0.0.1:XXXXX
# HTTPS_PROXY=http://127.0.0.1:XXXXX
```

## Structured Log Analysis

### Find blocked domains

```bash
grep -i "blocked\|forbidden\|403" ~/.openclaw/logs/gateway.err.log | \
  sort | uniq -c | sort -rn
```

### Find connection errors

```bash
grep -i "ECONNREFUSED\|ETIMEDOUT\|ENOTFOUND" ~/.openclaw/logs/gateway.err.log
```

### Activity timeline

```bash
# Last hour of activity
tail -1000 ~/.openclaw/logs/gateway.log | \
  grep -E "^\d{4}-\d{2}-\d{2}" | \
  cut -d' ' -f1-2 | uniq -c
```

## Alerting (Advanced)

For production monitoring, consider:

```bash
# Simple watchdog - alert if gateway down
#!/bin/bash
if ! curl -s http://127.0.0.1:18789/health > /dev/null 2>&1; then
  # Send alert (customize for your setup)
  echo "OpenClaw gateway down" | mail -s "Alert" you@example.com
fi
```

Add to crontab:
```
*/5 * * * * ~/.openclaw/scripts/watchdog.sh
```
