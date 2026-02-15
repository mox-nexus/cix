# How to Troubleshoot a Blocked Request

**When you need this:** OpenClaw tries to access a site and gets "Connection blocked" or network error.

**What this fixes:** Identifies why the request failed and how to fix it.

**Time:** 5-10 minutes

---

## Quick Diagnosis

| Symptom | Likely Cause | Quick Fix |
|---------|--------------|-----------|
| "Connection blocked" | Domain not in allowlist | Add to `~/.srt-settings.json` |
| Works outside sandbox, fails inside | Missing `--` separator | Patch script handles this |
| Only subdomain blocked (www works, api doesn't) | Incomplete wildcard | Add both `domain.com` and `*.domain.com` |
| All requests blocked | Config not loading | Check path, validate JSON |

---

## The Three-Step Debug

### Step 1: Identify the Domain

What exact domain is being requested?

```bash
# Check gateway logs for the failed request
tail -50 ~/.openclaw/logs/gateway.err.log | grep -i "blocked\|denied\|refused"
```

Look for lines like:
```
Connection blocked: api.example.com
```

That's your domain.

### Step 2: Check If Domain Is Allowed

```bash
grep "example.com" ~/.srt-settings.json
```

**If found:** The domain is in your config. Go to Step 3.

**If not found:** Add it:

```bash
nano ~/.srt-settings.json
# Add to allowedDomains:
#   "example.com",
#   "*.example.com"
```

Then restart:
```bash
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway
```

### Step 3: Check Wildcard Coverage

If you have `*.example.com`, do you also have `example.com`?

```bash
# Check for wildcard
grep "\"\\*\\.example\\.com\"" ~/.srt-settings.json

# Check for base
grep "\"example\\.com\"" ~/.srt-settings.json
```

You need both. Add whichever is missing.

---

## The Wildcard Gotcha

This is the most common cause of "domain allowed but still blocked":

```json
// Wrong: Only subdomain
"allowedDomains": ["*.linkedin.com"]

// Right: Both patterns
"allowedDomains": [
  "linkedin.com",
  "*.linkedin.com"
]
```

`*.example.com` matches `www.example.com` but NOT `example.com`.

---

## Advanced: Test the Request Directly

Test if SRT would allow the request:

```bash
srt --settings ~/.srt-settings.json -- curl -v "https://example.com" 2>&1 | grep -E "(CONNECT|blocked|HTTP/)"
```

**Expected (allowed):** HTTP status code (200, 401, 403, etc.)

**Expected (blocked):** "Connection blocked" or "403 Forbidden" from proxy

---

## Common Causes

| Error Message | Cause | Fix |
|---------------|-------|-----|
| `Connection blocked: example.com` | Not in allowedDomains | Add to config |
| Wildcard allowed but base blocked | Missing base domain | Add `example.com` alongside `*.example.com` |
| Config looks right but still blocked | JSON syntax error | Validate: `python3 -m json.tool ~/.srt-settings.json` |
| Different behavior inside/outside | `--` separator issue | Re-run patch script |

---

## Full Diagnostic (If Still Stuck)

Run the complete verification:

```bash
bash ~/.claude/plugins/run-openclaw-srt/skills/openclaw-srt-setup/scripts/verify-sandbox.sh
```

This checks:
- Is SRT wrapping the process?
- Is network filtering active?
- Is config valid JSON?

Look for which test fails.

---

## Example: Debugging GitHub Access

**Symptom:** "Connection blocked: api.github.com"

**Step 1:** Identify domain: `api.github.com`

**Step 2:** Check config:
```bash
grep "github" ~/.srt-settings.json
```

**Result:** Only has `"github.com"`, missing wildcard.

**Fix:** Add wildcard:
```json
"allowedDomains": [
  "github.com",
  "*.github.com"
]
```

**Restart and test:**
```bash
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway
srt --settings ~/.srt-settings.json -- curl -sI "https://api.github.com"
```

---

## When to Use Full Debug Mode

If the three-step debug doesn't find it, enable SRT debug output:

```bash
SRT_DEBUG=1 srt -d --settings ~/.srt-settings.json -- curl -v "https://failing-domain.com" 2>&1 | tee /tmp/srt-debug.log
```

Look for:
- `CONNECT refused` - proxy blocking HTTPS tunnel
- `No route to host` - network issue (not sandbox)
- Domain mismatches (CDN redirect, etc.)

---

## Quick Reference

```bash
# 1. Find the blocked domain
tail -50 ~/.openclaw/logs/gateway.err.log | grep -i blocked

# 2. Check if in config
grep "DOMAIN" ~/.srt-settings.json

# 3. Add if missing
nano ~/.srt-settings.json

# 4. Validate JSON
python3 -m json.tool ~/.srt-settings.json

# 5. Restart
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway

# 6. Test
srt --settings ~/.srt-settings.json -- curl -sI "https://DOMAIN"
```
