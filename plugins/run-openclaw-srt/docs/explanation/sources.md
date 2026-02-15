# Sources

## Primary Implementation References

### Anthropic Sandbox Runtime (SRT)

**Package:** `@anthropic-ai/sandbox-runtime`
**npm:** https://www.npmjs.com/package/@anthropic-ai/sandbox-runtime

**Why it matters:** This is the actual sandbox we use. Understanding its implementation helps debug issues.

**Key files:**
- `src/cli.ts` - Commander.js CLI setup (explains the `--` separator issue)
- `src/sandbox/sandbox-manager.ts` - Orchestration logic
- `src/sandbox/macos-sandbox-utils.ts` - Seatbelt profile generation
- `src/sandbox/http-proxy.ts` - Domain filtering implementation

---

## OS-Level Sandboxing

### Apple Seatbelt / sandbox-exec (macOS)

**Man page:** `man sandbox-exec`

**Why it matters:** This is the kernel-level enforcement mechanism. It's not just a wrapper - it's TrustedBSD MAC framework security.

**How it works:**
- Uses SBPL (Sandbox Profile Language) policies
- Enforced at kernel level via TrustedBSD MAC
- Process replacement pattern (exec) preserves restrictions

**Why you don't see it in ps:** The exec pattern applies restrictions then replaces itself with the target process. Restrictions persist at kernel level.

### bubblewrap (Linux)

**Repository:** https://github.com/containers/bubblewrap
**Docs:** https://github.com/containers/bubblewrap/blob/main/README.md

**Why it matters:** Linux alternative to sandbox-exec. Used by Flatpak and other sandboxing systems.

**Mechanisms:**
- Network namespace isolation (`--unshare-net`)
- Filesystem bind mounts
- Process isolation

---

## CLI Parsing

### Commander.js

**Repository:** https://github.com/tj/commander.js

**Why it matters:** SRT uses this for CLI parsing. Understanding its behavior explains the `--` separator requirement.

**The gotcha:** Commander does not stop parsing at positional arguments by default. Without `--`, flags in the wrapped command get interpreted as SRT flags.

```bash
# Broken: -s parsed as --settings
srt --settings config.json curl -s https://...

# Fixed: -- tells Commander to stop parsing
srt --settings config.json -- curl -s https://...
```

**POSIX standard:** IEEE Std 1003.1 (POSIX.1) defines `--` as "end of options" delimiter.

---

## OpenClaw

**Package:** `openclaw`

**Why it matters:** This is what we're sandboxing.

**Key paths:**
- `~/.openclaw/openclaw.json` - Main config
- `~/.openclaw/credentials/` - Auth tokens
- `~/.openclaw/logs/` - Gateway logs (check here for errors)
- `~/Library/LaunchAgents/ai.openclaw.gateway.plist` - macOS service definition

**Not widely documented:** Limited public docs at time of writing. This plugin's docs fill that gap.

---

## Service Management

### macOS: launchd

**Man pages:**
- `man launchctl` - Service control
- `man launchd.plist` - Service definition format

**Apple docs:** Daemons and Services Programming Guide

**Key commands:**
- `launchctl bootout` - Stop service
- `launchctl bootstrap` - Start service
- `launchctl kickstart -k` - Restart service

### Linux: systemd

**Man pages:**
- `man systemd.service`
- `man systemctl`

**User services:**
- Location: `~/.config/systemd/user/`
- Persistence: `loginctl enable-linger`

---

## Security Concepts

### Defense in Depth

**Principle:** Multiple independent layers of security. Compromise of one layer doesn't compromise all.

**Our layers:**
1. **Network** - Proxy filtering (domain allowlist)
2. **Filesystem** - Seatbelt rules (deny read/write paths)
3. **Process** - OS sandbox (kernel enforcement)
4. **Application** - OpenClaw pairing (access control)

### Threat Model Assumptions

**This setup assumes:**
- Attacker controls model outputs (prompt injection, compromised weights)
- User has not intentionally weakened config
- OS and SRT are not compromised

**This setup does NOT protect against:**
- Kernel exploits (requires OS patching)
- Physical access (different security domain)
- Supply chain attacks on SRT itself
- Side-channel attacks (timing, cache, spectre)

These limitations are documented honestly in [methodology.md](methodology.md).

---

## Discovery Process

### The `--` Separator

**Problem:** All network requests blocked despite correct `allowedDomains`.

**Investigation:** Structured debugging revealed Commander.js was consuming flags intended for the wrapped command.

**Root cause:** `srt --settings config.json curl -s https://...` interprets `-s` as `--settings` short flag.

**Fix:** POSIX `--` separator tells Commander to stop parsing options.

**Impact:** The patch script now includes `--` automatically in the daemon plist.

**Documented in:** [gotchas.md](../../skills/openclaw-srt-setup/references/gotchas.md)

### The Wildcard Gotcha

**Discovery:** Domains configured with `*.example.com` still blocked when accessing `example.com`.

**Root cause:** Wildcard patterns in SRT's proxy don't match the base domain.

**Pattern:**
- `*.example.com` matches `www.example.com`, `api.example.com`
- `*.example.com` does NOT match `example.com`

**Fix:** Always include both patterns:
```json
"allowedDomains": [
  "example.com",
  "*.example.com"
]
```

---

## Why These Sources Matter

### Production Usage Over Stars

We prioritize:
1. **What actually ships** - Production codebases using these tools
2. **Core maintainers** - Primary knowledge holders (Anthropic for SRT)
3. **Proven adoption** - OpenClaw + SRT deployed in real environments

GitHub stars are social proof, not technical validity.

### Evidence-Based Decisions

Every security choice in this plugin references:
- Actual attack scenarios (prompt injection, credential theft)
- OS-level mechanisms (Seatbelt, bubblewrap)
- Measured limitations (what we protect, what we don't)

No hand-waving. No "should be secure." Specific mechanisms, specific protections, honest limitations.

---

## Further Reading

- [architecture.md](architecture.md) - How the pieces interact
- [methodology.md](methodology.md) - Why these choices
- [security-model.md](../../skills/openclaw-srt-setup/references/security-model.md) - Detailed threat analysis
