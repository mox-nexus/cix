# OpenClaw + SRT Architecture

**What this explains:** How OpenClaw and SRT work together to provide secure AI assistance.

**Reading guide:**
- **Just starting?** Read "The Big Picture" and "Why This Architecture?"
- **Understanding OpenClaw?** Read "OpenClaw Architecture" section
- **Understanding SRT?** Read "SRT Architecture" and "How SRT Applies Restrictions"
- **Understanding integration?** Read "Combined: OpenClaw + SRT"
- **Deep dive?** Read all diagrams in sequence

---

## The Big Picture

Two systems, distinct responsibilities:

| System | Purpose | Runs As |
|--------|---------|---------|
| **OpenClaw** | Personal AI assistant | Node.js daemon |
| **SRT** | Security sandbox wrapper | Process wrapper |

Without SRT, OpenClaw has full access to your machine. SRT restricts what it can reach.

**In brief:**
- OpenClaw handles communication (Telegram, web UI, Claude API)
- SRT enforces security (network filtering, filesystem restrictions)
- They compose via process wrapping: `srt -- node openclaw`

---

## OpenClaw Architecture

OpenClaw is a modular gateway connecting you to Claude.

```mermaid
flowchart TB
    subgraph "OpenClaw Gateway"
        direction TB

        subgraph "Channels (Input)"
            TG[Telegram Bot]
            UI[Control UI]
            API[REST API]
        end

        subgraph "Core"
            ROUTER[Message Router]
            CONTEXT[Context Manager]
            PAIR[Pairing System]
        end

        subgraph "Providers (Output)"
            CLAUDE[Claude Provider]
        end

        TG --> ROUTER
        UI --> ROUTER
        API --> ROUTER

        ROUTER --> CONTEXT
        CONTEXT --> CLAUDE
        CLAUDE --> CONTEXT
        CONTEXT --> ROUTER

        ROUTER --> TG
        ROUTER --> UI
        ROUTER --> API
    end

    CLAUDE --> |"HTTPS"| ANTHROPIC((api.anthropic.com))
    TG --> |"HTTPS"| TELEGRAM((api.telegram.org))
```

### OpenClaw Components

**Channels** - How users interact with OpenClaw:

| Channel | Transport | Auth |
|---------|-----------|------|
| Telegram | Bot API polling | Pairing code |
| Control UI | HTTP localhost | Bearer token |
| REST API | HTTP localhost | Bearer token |

**Core** - Message orchestration:

| Component | Responsibility |
|-----------|----------------|
| Message Router | Dispatches to/from channels |
| Context Manager | Maintains conversation state |
| Pairing System | Links Telegram users to instance |

**Providers** - AI backends:

| Provider | Purpose |
|----------|---------|
| Claude | Primary AI (Anthropic API) |

### OpenClaw Message Flow

```mermaid
sequenceDiagram
    participant User
    participant Channel as Channel<br/>(Telegram/UI)
    participant Router as Message Router
    participant Context as Context Manager
    participant Provider as Claude Provider
    participant API as Anthropic API

    User->>Channel: Send message
    Channel->>Router: Incoming message
    Router->>Router: Auth check (paired?)

    alt Not paired
        Router-->>Channel: Pairing code prompt
    else Paired
        Router->>Context: Add to conversation
        Context->>Provider: Get completion
        Provider->>API: Claude API call
        API-->>Provider: Response
        Provider-->>Context: Add response
        Context-->>Router: Response ready
        Router-->>Channel: Send response
        Channel-->>User: Display
    end
```

### OpenClaw Configuration

Config lives at `~/.openclaw/openclaw.json`:

```
~/.openclaw/
├── openclaw.json      # Main config
├── credentials/       # API keys (encrypted)
├── logs/              # Gateway logs
└── state/             # Conversation state
```

Key config sections:

| Section | Controls |
|---------|----------|
| `providers.anthropic` | API key, model selection |
| `channels.telegram` | Bot token, DM policy |
| `gateway.auth` | UI token, port |

---

## SRT Architecture

SRT wraps any process to apply OS-level security restrictions.

```mermaid
flowchart TB
    subgraph "SRT"
        CLI[SRT CLI] --> CONFIG[Parse Config]
        CONFIG --> SANDBOX[Apply OS Sandbox]
        CONFIG --> PROXY[Start Proxy]

        SANDBOX --> |"replace process"| TARGET[Target Process]
        PROXY --> |"HTTP_PROXY"| TARGET
    end

    TARGET --> PROXY
    PROXY --> |"Allowed"| NET((Internet))
    PROXY -.-> |"Blocked"| DROP[403]

    style DROP fill:#f66,color:#fff
```

### SRT Components

| Component | macOS | Linux |
|-----------|-------|-------|
| OS Sandbox | sandbox-exec + Seatbelt | bubblewrap (bwrap) |
| Network Proxy | HTTP/SOCKS proxy | HTTP/SOCKS proxy |
| Config Format | JSON | JSON |

### How SRT Applies Restrictions

```mermaid
sequenceDiagram
    participant Init as launchd/systemd
    participant SRT as SRT CLI
    participant Sandbox as OS Sandbox
    participant Proxy as SRT Proxy
    participant App as OpenClaw

    Init->>SRT: Start srt --settings config -- node openclaw
    SRT->>SRT: Parse config.json
    SRT->>Proxy: Start proxy on localhost:PORT
    SRT->>Sandbox: Generate sandbox profile
    SRT->>Sandbox: Apply restrictions and run
    Sandbox->>App: Process starts sandboxed

    Note over App,Proxy: HTTP_PROXY env var set

    App->>Proxy: Outbound request
    Proxy->>Proxy: Check allowedDomains
    alt Allowed
        Proxy->>Internet: Forward
    else Blocked
        Proxy-->>App: 403 Forbidden
    end
```

---

## Combined: OpenClaw + SRT

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

### Complete Message Flow

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

---

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

---

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

---

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

---

## Daemon Lifecycle

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

---

## Why This Architecture?

### Why Proxy-Based Network Filtering?

**Problem:** Seatbelt (macOS sandbox) network rules are IP-based, not domain-based.

**Challenges with IP filtering:**
- IPs change (CDNs, load balancers)
- Multiple domains share IPs
- DNS is dynamic

**Solution:** Proxy intercepts requests and checks the Host header / SNI.

### Why Process Replacement?

`sandbox-exec` uses the POSIX `exec` pattern - applies restrictions then replaces itself with the target process.

**Benefits:**
- Clean process tree (no visible wrapper)
- Restrictions persist at kernel level
- Minimal overhead

**Consequence:** You won't see `sandbox-exec` in `ps` output. The sandbox IS active - it's kernel-enforced, not process-enforced.

### Why the `--` Separator?

SRT uses Commander.js for CLI parsing. Without `--`, flags in the wrapped command get interpreted as SRT flags.

```
BAD:  srt --settings config curl -s https://...
      └── Commander sees -s as --settings short flag

GOOD: srt --settings config -- curl -s https://...
      └── Everything after -- is the command
```

The patch script handles this automatically.

---

## Further Reading

- [methodology.md](methodology.md) - Why sandbox OpenClaw
- [security-model.md](../../skills/openclaw-srt-setup/references/security-model.md) - What's protected and why
- [gotchas.md](../../skills/openclaw-srt-setup/references/gotchas.md) - Common issues
- [sources.md](sources.md) - Primary references
