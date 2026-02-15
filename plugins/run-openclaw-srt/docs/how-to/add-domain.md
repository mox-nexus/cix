# How to Add a Domain to the Allowlist

**When you need this:** Claude tries to access a website and gets "Connection blocked" or "Network error."

**What this fixes:** Adds the domain to your SRT sandbox allowlist so OpenClaw can reach it.

**Time:** 2 minutes

---

## Quick Reference

```bash
# 1. Edit config
nano ~/.srt-settings.json

# 2. Add domain to allowedDomains array (see wildcard rule below)

# 3. Validate
python3 -m json.tool ~/.srt-settings.json > /dev/null && echo "JSON valid"

# 4. Restart
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway

# 5. Test
srt --settings ~/.srt-settings.json -- curl -sI "https://your-domain.com"
```

---

## The Wildcard Rule (Critical)

Wildcards do NOT match the base domain.

| Pattern | Matches | Does NOT Match |
|---------|---------|----------------|
| `*.example.com` | `www.example.com`, `api.example.com` | `example.com` |
| `example.com` | `example.com` | `www.example.com` |

**Always include both** if you need the full domain:

```json
"allowedDomains": [
  "linkedin.com",
  "*.linkedin.com"
]
```

This is the most common mistake when adding domains.

---

## Detailed Steps

### 1. Edit the Config File

Open your SRT settings:

```bash
nano ~/.srt-settings.json
# or
code ~/.srt-settings.json
```

### 2. Add the Domain

Find the `allowedDomains` array and add your domain:

```json
{
  "allowedDomains": [
    "api.anthropic.com",
    "api.telegram.org",
    "your-new-domain.com",
    "*.your-new-domain.com"
  ]
}
```

**Remember:** Add both the base domain and wildcard if you need subdomains.

### 3. Validate JSON Syntax

```bash
python3 -m json.tool ~/.srt-settings.json > /dev/null && echo "JSON valid"
```

Common errors:
- Missing commas between entries
- Trailing comma after last entry (not allowed in JSON)
- Mismatched quotes

### 4. Restart the Daemon

```bash
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway
```

Wait a few seconds for the restart to complete.

### 5. Verify the Domain Works

```bash
srt --settings ~/.srt-settings.json -- curl -sI "https://your-new-domain.com" | head -1
```

**Expected:** HTTP status code (200, 301, 403, etc.)

**Not expected:** "Connection blocked" or timeout

---

## Examples

### Adding GitHub

```json
"allowedDomains": [
  "github.com",
  "*.github.com",
  "api.github.com"
]
```

Why both `*.github.com` and `api.github.com`? Defense in depth. Some clients resolve `api.github.com` directly, others use it as a subdomain pattern.

### Adding a CDN

```json
"allowedDomains": [
  "cdn.example.com",
  "static.example.com",
  "images.example.com"
]
```

CDNs often use specific subdomains. Add the ones you need, not a blanket wildcard.

---

## Troubleshooting

**"JSON syntax error"**

Run validation to see the error:
```bash
python3 -m json.tool ~/.srt-settings.json
```

Fix the line it reports.

**Domain added but still blocked**

Check:
1. Did you restart the daemon?
2. Is the domain spelled exactly right? (case-sensitive)
3. Did you include both base and wildcard?
4. Is the request using a subdomain you didn't add?

**Too many domains to add manually**

Start with a broader template. See [templates.md](../explanation/templates.md) for pre-built configs (developer, ai-research, etc.).
