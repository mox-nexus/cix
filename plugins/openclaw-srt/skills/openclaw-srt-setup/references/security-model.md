# Security Model

Defense-in-depth for OpenClaw with SRT.

## Threat Model

OpenClaw is an AI assistant that can:
- Execute arbitrary shell commands
- Access network
- Read/write files
- Interact with external services via API

### What we're defending against

| Threat | Description | Likelihood |
|--------|-------------|------------|
| Credential theft | Agent reads SSH keys, API tokens, cloud configs | Medium |
| Data exfiltration | Agent sends sensitive data to attacker | Low-Medium |
| Persistence | Agent modifies shell configs for backdoor | Low |
| Lateral movement | Agent accesses cloud infrastructure | Low |
| Supply chain | Malicious dependency in OpenClaw | Very Low |

### What we're NOT defending against

- Kernel exploits (requires OS patching)
- Side-channel attacks (timing, cache)
- Physical access
- Social engineering through the AI
- Bugs in SRT itself

## Defense Layers

```
Layer 1: Network (SRT allowedDomains)
   │
   └─► Only whitelisted domains reachable
       Blocks: C2 servers, exfiltration endpoints

Layer 2: Filesystem (SRT denyRead/allowWrite)
   │
   └─► Credentials inaccessible, writes restricted
       Blocks: SSH key theft, AWS config access

Layer 3: OS Sandbox (sandbox-exec/bubblewrap)
   │
   └─► Process isolation, kernel-enforced
       Blocks: Privilege escalation, raw syscalls

Layer 4: Gateway Auth (token)
   │
   └─► Control UI requires authentication
       Blocks: Unauthorized dashboard access

Layer 5: Channel Auth (pairing)
   │
   └─► Telegram users must be approved
       Blocks: Random people issuing commands
```

## What's Protected

### Credentials (denyRead)

| Path | Contains | Risk if exposed |
|------|----------|-----------------|
| `~/.ssh` | SSH keys | Server access, git push |
| `~/.aws` | AWS credentials | Cloud infrastructure |
| `~/.config/gcloud` | GCP credentials | Cloud infrastructure |
| `~/.kube` | Kubernetes configs | Cluster access |
| `~/.gnupg` | GPG keys | Signing, encryption |
| `~/Library/Keychains` | macOS keychain | All stored credentials |
| `~/.docker` | Docker credentials | Registry access |
| `~/.npmrc` | NPM tokens | Package publishing |
| `~/.password-store` | pass passwords | All passwords |
| `~/.1password` | 1Password data | All passwords |

### Persistence Vectors (denyWrite)

| Path | Why blocked |
|------|-------------|
| `~/.bashrc` | Shell startup script |
| `~/.zshrc` | Shell startup script |
| `~/.profile` | Login script |
| `~/.gitconfig` | Git hooks, aliases |
| `.git/hooks` | Repository hooks |

### Network (allowedDomains)

Only explicitly listed domains are reachable. Everything else returns 403.

Default template allows:
- `api.anthropic.com` - Claude API
- `api.telegram.org` - Bot communication
- Job sites, AI research, tech news
- `github.com` - Code hosting

Blocked by default:
- Any domain not in allowlist
- Local network (unless `allowLocalBinding: true`)
- Raw IPs (domain filtering only)

## What's Allowed

### Filesystem

| Path | Why allowed | Risk accepted |
|------|-------------|---------------|
| `~/.openclaw` | Config, logs, state | Agent can read its own config |
| `/tmp` | Temporary files | Transient data |
| `/var/folders` | macOS temp | Transient data |

### Network

Only domains YOU explicitly add to `allowedDomains`.

### Capabilities

| Capability | Status | Notes |
|------------|--------|-------|
| Run shell commands | Allowed (sandboxed) | Commands run inside sandbox |
| Read files | Allowed (except denyRead) | Most filesystem readable |
| Write files | Restricted to allowWrite | Limited write locations |
| Network access | Restricted to allowedDomains | Proxy-enforced |
| Spawn processes | Allowed (inherit sandbox) | Children are sandboxed |

## Trust Boundaries

```
┌──────────────────────────────────────────────────────────┐
│                    UNTRUSTED                              │
│                                                          │
│  - Telegram messages from unknown users                  │
│  - External websites (even allowed ones)                 │
│  - AI model outputs (could be manipulated)              │
│  - Network responses                                     │
└──────────────────────────────────────────────────────────┘
                         │
                         │ Pairing / Validation
                         ▼
┌──────────────────────────────────────────────────────────┐
│                    SEMI-TRUSTED                           │
│                                                          │
│  - Paired Telegram users (approved by you)              │
│  - Claude API responses (from Anthropic)                │
│  - Local Control UI (with valid token)                  │
└──────────────────────────────────────────────────────────┘
                         │
                         │ Your review / approval
                         ▼
┌──────────────────────────────────────────────────────────┐
│                    TRUSTED                                │
│                                                          │
│  - Local config files you wrote                         │
│  - Commands you explicitly approve                      │
│  - Your own shell session                               │
└──────────────────────────────────────────────────────────┘
```

## Attack Scenarios

### Scenario: Credential Theft

**Attack:** Compromised model tries to read `~/.ssh/id_rsa`

**Defense:**
1. `denyRead: ["~/.ssh"]` in SRT config
2. sandbox-exec blocks the read at kernel level
3. Process gets "Permission denied"

**Result:** Blocked

### Scenario: Exfiltration

**Attack:** Model tries to POST data to `attacker.com`

**Defense:**
1. Request goes to HTTP proxy
2. Proxy checks domain against allowlist
3. `attacker.com` not in list → 403 Forbidden

**Result:** Blocked

### Scenario: Persistence

**Attack:** Model tries to add backdoor to `~/.bashrc`

**Defense:**
1. `denyWrite: ["~/.bashrc"]` in SRT config
2. sandbox-exec blocks the write at kernel level
3. Process gets "Permission denied"

**Result:** Blocked

### Scenario: Proxy Bypass

**Attack:** Model uses raw sockets to bypass HTTP proxy

**Defense:**
1. sandbox-exec restricts network syscalls
2. Only proxy-routed connections allowed
3. Raw socket creation blocked

**Result:** Blocked (on macOS with seatbelt)

**Note:** On Linux, this relies on network namespace isolation (`--unshare-net`), not syscall filtering.

## Limitations

### Proxy-Based Network Filtering

Apps that don't respect `HTTP_PROXY` env var could potentially bypass filtering. Most apps do respect it, but:
- Custom socket code might not
- Some languages need explicit proxy configuration

**Mitigation:** On macOS, seatbelt also restricts network. On Linux, network namespace provides isolation.

### Same-User Context

The sandbox runs as your user. It can't protect against:
- Reading files you can read (except denyRead)
- Processes that don't inherit the sandbox

**Mitigation:** Keep denyRead list comprehensive.

### Config Tampering

If an attacker can modify `~/.srt-settings.json`, they can allow any domain.

**Mitigation:**
- Don't include `~/.srt-settings.json` in allowWrite
- Monitor config file changes

## Recommendations

1. **Minimal allowedDomains** - Only add what you need
2. **Comprehensive denyRead** - Include all credential stores
3. **Monitor logs** - Check `~/.openclaw/logs/` for suspicious activity
4. **Rotate tokens regularly** - Gateway token, Telegram bot token
5. **Review pairing requests** - Don't auto-approve unknown users
6. **Keep SRT updated** - Security patches
