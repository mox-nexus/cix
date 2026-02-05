# Sources

## Primary Sources

### Anthropic Sandbox Runtime

**Package:** `@anthropic-ai/sandbox-runtime`
**npm:** https://www.npmjs.com/package/@anthropic-ai/sandbox-runtime

Key implementation files referenced in architecture.md:
- `src/cli.ts` - Commander.js CLI setup
- `src/sandbox/sandbox-manager.ts` - Orchestration
- `src/sandbox/macos-sandbox-utils.ts` - Seatbelt profile generation
- `src/sandbox/http-proxy.ts` - Domain filtering logic

### Apple Seatbelt / Sandbox

**Documentation:** Limited official docs. Best reference is sandbox-exec(1) man page.

**How sandbox-exec works:**
- Uses SBPL (Sandbox Profile Language) policies
- Enforced at kernel level via TrustedBSD MAC framework
- Process replacement pattern preserves restrictions

### bubblewrap

**Repository:** https://github.com/containers/bubblewrap
**Documentation:** https://github.com/containers/bubblewrap/blob/main/README.md

Used on Linux for:
- Network namespace isolation (`--unshare-net`)
- Filesystem bind mounts
- Process isolation

### Commander.js

**Repository:** https://github.com/tj/commander.js
**Behavior:** Does not stop parsing at positional arguments by default.

This caused the `--` separator issue. Commander interprets `-s` as `--settings` short flag even when it appears in the wrapped command.

---

## The `--` Separator

**POSIX standard:** IEEE Std 1003.1 (POSIX.1)

The `--` delimiter signals end of options:
> "The first -- argument that is not an option-argument should be accepted as a delimiter indicating the end of options."

Most CLI parsers respect this, but Commander.js requires explicit use.

---

## OpenClaw

**Package:** `openclaw`
**Documentation:** Limited public docs at time of writing.

Key configuration paths:
- `~/.openclaw/openclaw.json` - Main config
- `~/.openclaw/credentials/` - Auth tokens
- `~/.openclaw/logs/` - Gateway logs
- `~/Library/LaunchAgents/ai.openclaw.gateway.plist` - macOS service

---

## launchd / systemd

**macOS launchd:**
- `launchctl(1)` man page
- Apple's Daemons and Services Programming Guide

**Linux systemd:**
- `systemd.service(5)` man page
- User services at `~/.config/systemd/user/`
- `loginctl enable-linger` for persistence

---

## Security Context

### Defense in Depth

The multi-layer approach follows standard security practice:
- Network layer (proxy filtering)
- Filesystem layer (seatbelt rules)
- Process layer (sandbox-exec/bwrap)
- Application layer (OpenClaw's pairing)

No single layer is sufficient; compromise of one doesn't compromise all.

### Threat Model Assumptions

This setup assumes:
- Attacker controls model outputs (prompt injection, compromised weights)
- User has not intentionally weakened config
- OS and SRT are not compromised

It does NOT assume:
- Protection against kernel exploits
- Protection against physical access
- Protection against supply chain attacks on SRT itself
