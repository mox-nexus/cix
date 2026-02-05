# SRT Architecture

How Anthropic's Sandbox Runtime actually works.

## Overview

SRT provides defense-in-depth through multiple layers:

```
┌─────────────────────────────────────────────────────────────┐
│                        SRT CLI                               │
│  srt --settings config.json -- <command>                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    SandboxManager                            │
│  - Reads config                                              │
│  - Starts HTTP/SOCKS proxy                                   │
│  - Generates seatbelt profile (macOS) or bwrap args (Linux) │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│      OS Sandbox          │     │     Network Proxy        │
│  sandbox-exec (macOS)    │     │  HTTP: domain filtering  │
│  bubblewrap (Linux)      │     │  SOCKS: domain filtering │
└─────────────────────────┘     └─────────────────────────┘
```

## macOS: sandbox-exec + Seatbelt

macOS uses Apple's Seatbelt framework via `sandbox-exec`.

### How it works

1. **Profile generation:** SRT converts config to seatbelt profile (SBPL syntax)
2. **Sandbox application:** `sandbox-exec -p <profile>` applies restrictions
3. **Replaces itself:** sandbox-exec uses POSIX exec pattern - replaces itself with target
4. **Kernel enforcement:** Restrictions enforced at kernel level, survive process replacement

### Seatbelt profile example

```scheme
(version 1)
(deny default)

; Allow reading most of filesystem
(allow file-read*)

; Deny specific sensitive paths
(deny file-read* (subpath "/Users/name/.ssh"))
(deny file-read* (subpath "/Users/name/.aws"))

; Allow writing only to specific paths
(allow file-write* (subpath "/Users/name/.openclaw"))
(allow file-write* (subpath "/tmp"))

; Network handled by proxy, not seatbelt
```

### Why sandbox-exec doesn't appear in ps

The sandbox binary uses the POSIX exec pattern, replacing itself with the target process. After this:
- Process tree shows just the target (e.g., `node`)
- The sandbox IS active - enforced by kernel, not a running process
- Verify with: `ps aux | grep "srt.*settings"`

## Network Filtering

SRT doesn't use seatbelt for network filtering. Instead:

1. **Proxy servers:** HTTP and SOCKS5 proxies start on localhost
2. **Environment variables:** `HTTP_PROXY`, `HTTPS_PROXY`, `ALL_PROXY` set
3. **Domain filtering:** Proxy checks each request against allowlist

### Flow

```
App makes HTTPS request to api.telegram.org
    │
    ▼
HTTP_PROXY=localhost:12345 (set by SRT)
    │
    ▼
SRT HTTP Proxy receives CONNECT request
    │
    ▼
filterNetworkRequest(443, "api.telegram.org")
    │
    ├─► In allowedDomains? → Allow, tunnel connection
    │
    └─► Not in allowedDomains? → Return 403 "Connection blocked"
```

### Domain matching logic

```typescript
function matchesDomainPattern(hostname: string, pattern: string): boolean {
  if (pattern.startsWith('*.')) {
    const baseDomain = pattern.substring(2)
    return hostname.endsWith('.' + baseDomain)  // *.foo.com matches x.foo.com, not foo.com
  }
  return hostname === pattern  // Exact match
}
```

**Important:** `*.example.com` does NOT match `example.com`. Include both.

## Linux: bubblewrap

Linux uses bubblewrap (`bwrap`) for sandboxing.

### Key differences from macOS

| Aspect | macOS | Linux |
|--------|-------|-------|
| Sandbox tool | sandbox-exec | bubblewrap |
| Network isolation | Proxy-based | Network namespace (`--unshare-net`) |
| Filesystem | Seatbelt rules | Bind mounts + tmpfs |
| Bridge | Not needed | socat Unix socket bridge |

### Linux network flow

```
┌─────────────────────────────────────────────────────────┐
│                    Host Machine                          │
│                                                          │
│   SRT Proxy ←─── socat ←─── Unix Socket ←───┐          │
│   (HTTP/SOCKS)                               │          │
│                                              │          │
│   ┌──────────────────────────────────────────┼────────┐│
│   │            bubblewrap sandbox            │        ││
│   │            --unshare-net                 │        ││
│   │                                          │        ││
│   │   HTTP_PROXY=localhost:3128 ──► socat ───┘        ││
│   │   (socat bridges to Unix socket)                  ││
│   │                                                    ││
│   │   OpenClaw Gateway                                 ││
│   └────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────┘
```

Because `--unshare-net` creates isolated network namespace, socat bridges are needed to connect to the host's proxy servers via Unix sockets.

## Config Schema

```typescript
interface SandboxRuntimeConfig {
  network: {
    allowedDomains: string[]      // Domains that can be reached
    deniedDomains: string[]       // Explicit blocklist (checked first)
    allowLocalBinding?: boolean   // Allow localhost binding (for servers)
    httpProxyPort?: number        // Use external proxy instead
    socksProxyPort?: number       // Use external SOCKS proxy
  }
  filesystem: {
    denyRead: string[]            // Paths that cannot be read
    allowWrite: string[]          // Paths that can be written
    denyWrite: string[]           // Paths within allowWrite that are blocked
  }
}
```

## Key Implementation Files

In `@anthropic-ai/sandbox-runtime`:

| File | Purpose |
|------|---------|
| `src/cli.ts` | CLI entry point, Commander.js setup |
| `src/sandbox/sandbox-manager.ts` | Orchestrates sandbox setup |
| `src/sandbox/http-proxy.ts` | HTTP proxy with domain filtering |
| `src/sandbox/socks-proxy.ts` | SOCKS5 proxy with domain filtering |
| `src/sandbox/macos-sandbox-utils.ts` | Seatbelt profile generation |
| `src/sandbox/linux-sandbox-utils.ts` | bubblewrap command generation |

## Security Guarantees

**What SRT guarantees:**
- Filesystem paths in `denyRead` are inaccessible (kernel-enforced)
- Only `allowWrite` paths are writable (kernel-enforced)
- Network requests only reach `allowedDomains` (proxy-enforced)

**What SRT does NOT guarantee:**
- Protection against apps that don't respect proxy env vars
- Protection against kernel exploits
- Protection against side-channel attacks
- Network filtering at kernel level (it's proxy-based)

## Why This Architecture?

**Proxy-based network filtering (not seatbelt):**
- Seatbelt network rules are IP-based, not domain-based
- Proxy allows domain-level filtering with wildcards
- Dynamic config updates without restarting sandbox

**Process replacement pattern for sandbox:**
- Standard Unix pattern - minimal overhead
- Sandbox persists across process replacement
- Clean process tree
