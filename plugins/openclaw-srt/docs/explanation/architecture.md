# OpenClaw + SRT Architecture

How the pieces fit together.

## The Big Picture

OpenClaw is a personal AI assistant that runs as a daemon on your machine. It connects to:
- **Claude API** for AI responses
- **Telegram** for mobile messaging
- **Local UI** for direct interaction

Without sandboxing, this daemon has full access to your machine — files, network, everything.

SRT (Sandbox Runtime) wraps OpenClaw to restrict what it can access.

```mermaid
flowchart TB
    subgraph "Your Machine"
        subgraph "SRT Sandbox"
            OC[OpenClaw Gateway]
            OC --> |"Claude API"| PROXY
            OC --> |"Telegram"| PROXY
        end

        PROXY[SRT Proxy<br/>Domain Filter]

        subgraph "Protected"
            SSH[~/.ssh]
            AWS[~/.aws]
            KUBE[~/.kube]
        end
    end

    PROXY --> |"Allowed"| INTERNET((Internet))
    PROXY -.-> |"Blocked"| BLOCKED[403 Forbidden]

    OC -.-> |"denyRead"| SSH
    OC -.-> |"denyRead"| AWS
    OC -.-> |"denyRead"| KUBE

    style SSH fill:#f66,color:#fff
    style AWS fill:#f66,color:#fff
    style KUBE fill:#f66,color:#fff
    style BLOCKED fill:#999,color:#fff
```

## Component Flow

When you send a message via Telegram:

```mermaid
sequenceDiagram
    participant T as Telegram
    participant GW as OpenClaw Gateway
    participant P as SRT Proxy
    participant C as Claude API

    T->>P: Message arrives
    P->>P: Check: api.telegram.org in allowlist?
    P->>GW: Forward (allowed)

    GW->>GW: Process message
    GW->>P: Call Claude API
    P->>P: Check: api.anthropic.com in allowlist?
    P->>C: Forward (allowed)
    C-->>P: AI response
    P-->>GW: Response

    GW->>P: Send reply to Telegram
    P->>T: Forward (allowed)
```

## SRT Sandbox Layers

SRT provides defense in depth through multiple layers:

```mermaid
flowchart TB
    subgraph "Layer 1: Process"
        LAUNCHD[launchd/systemd] --> SRT[SRT CLI]
        SRT --> SANDBOX[OS Sandbox]
        SANDBOX --> APP[OpenClaw]
    end

    subgraph "Layer 2: Filesystem"
        APP -.-> |"denyRead"| CREDS[Credentials]
        APP --> |"allowWrite"| STATE[~/.openclaw]
    end

    subgraph "Layer 3: Network"
        APP --> PROXY[HTTP/SOCKS Proxy]
        PROXY --> |"allowedDomains"| NET[Internet]
        PROXY -.-> |"blocked"| DROP[Dropped]
    end

    style CREDS fill:#f66,color:#fff
    style DROP fill:#999,color:#fff
```

### Layer Details

| Layer | macOS | Linux | What it does |
|-------|-------|-------|--------------|
| Process | sandbox-exec | bubblewrap | OS-level isolation |
| Filesystem | Seatbelt rules | Bind mounts | Path restrictions |
| Network | Proxy filtering | Namespace + proxy | Domain allowlist |

## Network Filtering Flow

The proxy intercepts all HTTP/HTTPS traffic:

```mermaid
flowchart LR
    APP[OpenClaw] --> |"HTTP_PROXY"| PROXY[SRT Proxy]

    PROXY --> CHECK{Domain in<br/>allowedDomains?}

    CHECK --> |"Yes"| ALLOW[Forward request]
    CHECK --> |"No"| BLOCK[Return 403]

    ALLOW --> INTERNET((Internet))

    style BLOCK fill:#f66,color:#fff
```

### Domain Matching

```
Pattern: *.linkedin.com
  ✓ Matches: www.linkedin.com, api.linkedin.com
  ✗ Does NOT match: linkedin.com (no subdomain)

Solution: Include both
  "linkedin.com",
  "*.linkedin.com"
```

## Trust Boundaries

```mermaid
flowchart TB
    subgraph UNTRUSTED["Untrusted"]
        TG_MSG[Telegram Messages]
        WEB[External Websites]
    end

    subgraph PAIRING["Pairing Gate"]
        PAIR[Pairing Code]
    end

    subgraph SEMI["Semi-Trusted"]
        PAIRED[Paired Users]
        CLAUDE[Claude API]
        UI[Local UI + Token]
    end

    subgraph TRUSTED["Trusted"]
        CONFIG[Your Config]
        SHELL[Your Shell]
    end

    TG_MSG --> PAIR
    PAIR --> |"Approved"| PAIRED

    style UNTRUSTED fill:#f96,color:#000
    style SEMI fill:#ff9,color:#000
    style TRUSTED fill:#9f9,color:#000
```

## State Diagram: Daemon Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Stopped

    Stopped --> Starting: launchctl bootstrap
    Starting --> Running: SRT + OpenClaw init
    Running --> Stopped: launchctl bootout

    Running --> Running: Handle messages
    Running --> Error: Crash
    Error --> Starting: Auto-restart (launchd)

    note right of Running
        ps aux | grep "srt.*settings"
        should show process
    end note
```

## Why This Architecture?

### Why proxy-based network filtering?

**Problem**: Seatbelt (macOS sandbox) does IP-based filtering, not domain-based.

**Challenge**:
- IPs change (CDNs, load balancers)
- Multiple domains share IPs
- DNS is dynamic

**Solution**: Proxy intercepts requests and checks the Host header / SNI.

### Why process replacement?

`sandbox-exec` uses the POSIX `exec` pattern — it replaces itself with the target process after applying restrictions.

**Benefits**:
- Clean process tree (no wrapper visible)
- Restrictions persist at kernel level
- Minimal overhead

**Consequence**: You won't see `sandbox-exec` in `ps` output. The sandbox IS active — it's enforced by the kernel, not a running process.

### Why the `--` separator?

SRT uses Commander.js for CLI parsing. Without `--`, flags in the wrapped command get interpreted as SRT flags.

```
BAD:  srt --settings config curl -s https://...
      └── Commander sees -s as --settings short flag

GOOD: srt --settings config -- curl -s https://...
      └── Everything after -- is the command
```

## Further Reading

- [security-model.md](../../skills/openclaw-srt-setup/references/security-model.md) — What's protected and why
- [gotchas.md](../../skills/openclaw-srt-setup/references/gotchas.md) — Common issues
- [sources.md](sources.md) — Primary references
