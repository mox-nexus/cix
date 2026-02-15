# SRT Architecture

---

## Contents

- [Overview](#overview)
- [macOS: sandbox-exec](#macos-sandbox-exec)
- [Network Filtering](#network-filtering)
- [Linux: bubblewrap](#linux-bubblewrap)
- [Config Schema](#config-schema)
- [Security Guarantees](#security-guarantees)
- [Key Files](#key-files-in-anthropic-aisandbox-runtime)

---

## Overview

```
SRT CLI
   │
   ▼
SandboxManager
   │
   ├─► OS Sandbox (kernel-enforced)
   │   - macOS: sandbox-exec + seatbelt
   │   - Linux: bubblewrap + namespaces
   │
   └─► Network Proxy (domain filtering)
       - HTTP proxy: CONNECT tunneling
       - SOCKS5 proxy: domain allowlist
```

## macOS: sandbox-exec

1. SRT generates seatbelt profile (SBPL) from config
2. `sandbox-exec -p <profile>` applies restrictions
3. sandbox-exec uses POSIX exec - replaces itself with target
4. Restrictions enforced at kernel level, survive process replacement

**Why sandbox-exec doesn't appear in ps:** It exec'd into the target. Sandbox IS active - kernel-enforced, not a running process.

## Network Filtering

Not seatbelt (IP-based). Proxy-based (domain-based).

```
App → HTTP_PROXY → SRT Proxy → filterNetworkRequest(hostname)
                                   │
                                   ├─► In allowedDomains? → Allow
                                   └─► Not in list? → 403
```

### Domain Matching

```typescript
function matchesDomainPattern(hostname: string, pattern: string): boolean {
  if (pattern.startsWith('*.')) {
    return hostname.endsWith('.' + pattern.substring(2))  // *.foo.com matches x.foo.com, NOT foo.com
  }
  return hostname === pattern
}
```

**Key insight:** `*.example.com` does NOT match `example.com`. Include both.

## Linux: bubblewrap

| Aspect | macOS | Linux |
|--------|-------|-------|
| Sandbox | sandbox-exec | bubblewrap |
| Network | Proxy only | Network namespace (`--unshare-net`) + proxy |
| Bridge | Not needed | socat Unix socket |

Linux uses `--unshare-net` for true network isolation. socat bridges to host proxy via Unix sockets.

## Config Schema

```typescript
interface SandboxRuntimeConfig {
  network: {
    allowedDomains: string[]   // Reachable domains
    deniedDomains: string[]    // Blocklist (checked first)
    allowLocalBinding?: boolean
  }
  filesystem: {
    denyRead: string[]         // Cannot read
    allowWrite: string[]       // Can write
    denyWrite: string[]        // Block within allowWrite
  }
}
```

## Security Guarantees

**Guaranteed:**
- `denyRead` paths inaccessible (kernel-enforced)
- Only `allowWrite` paths writable (kernel-enforced)
- Only `allowedDomains` reachable (proxy-enforced)

**NOT guaranteed:**
- Apps that don't respect `HTTP_PROXY`
- Kernel exploits
- Side-channel attacks

## Key Files in @anthropic-ai/sandbox-runtime

| File | Purpose |
|------|---------|
| `src/cli.ts` | Commander.js entry |
| `src/sandbox/sandbox-manager.ts` | Orchestration |
| `src/sandbox/http-proxy.ts` | Domain filtering |
| `src/sandbox/macos-sandbox-utils.ts` | Seatbelt generation |
| `src/sandbox/linux-sandbox-utils.ts` | bwrap args |
