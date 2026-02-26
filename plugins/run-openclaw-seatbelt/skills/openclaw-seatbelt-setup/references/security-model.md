# Security Model

## Threat Model

OpenClaw can execute shell, access network, read/write files.

| Threat | Defense | Layer |
|--------|---------|-------|
| Credential theft | `denyRead: ~/.ssh, ~/.aws, ~/.gnupg` | Filesystem |
| Exfiltration | `allowedDomains` whitelist | Network |
| Persistence | `denyWrite: ~/.bashrc, ~/.zshrc` | Filesystem |
| Unauthorized access | Gateway token, Telegram pairing | Auth |

**NOT defending against:** Kernel exploits, side-channels, physical access, SRT bugs.

## Defense Layers

```
Layer 1: Network (allowedDomains) → Only whitelisted domains
Layer 2: Filesystem (denyRead/allowWrite) → Credentials inaccessible
Layer 3: OS Sandbox → Kernel-enforced process isolation
Layer 4: Gateway Auth → Token required for Control UI
Layer 5: Channel Auth → Telegram pairing required
```

## Relationship to OpenClaw's Docker Sandbox

OpenClaw has its own Docker-based sandbox for agent tool execution:
- `--read-only` root, `--network none`, `--cap-drop ALL`, `--security-opt no-new-privileges`
- Exec approval system with allowlists (`deny` | `allowlist` | `full`)
- Tool allow/deny policies per sandbox
- Per-session or per-agent container isolation

SRT protects a different layer: the gateway process itself.

| Layer | Protects | Mechanism | Threat |
|-------|----------|-----------|--------|
| OpenClaw Docker | Agent code execution | Container isolation | Malicious tool output |
| SRT | Gateway process | OS sandbox + domain allowlist | Supply chain, dependency vuln, Node.js zero-day |

The gateway runs outside Docker. If it is compromised (supply chain attack, dependency vulnerability), Docker sandbox is irrelevant — the attacker is the gateway. SRT's kernel-enforced restrictions still hold. Two layers, different holes (Swiss Cheese Model).

## Protected Paths (denyRead)

| Path | Risk if Exposed |
|------|-----------------|
| `~/.ssh` | Server access, git push |
| `~/.aws` | Cloud infrastructure |
| `~/.config/gcloud` | GCP access |
| `~/.kube` | Cluster access |
| `~/.gnupg` | Signing keys |
| `~/Library/Keychains` | All credentials (macOS) |
| `~/.docker` | Registry access |
| `~/.npmrc` | Package publishing |
| `~/.netrc` | HTTP auth credentials (curl, wget, git) |
| `~/.config/gh` | GitHub CLI tokens |
| `~/.azure` | Azure CLI credentials |
| `~/.local/share/keyrings` | Linux keyrings |

## Persistence Vectors Blocked (denyWrite)

`~/.bashrc`, `~/.bash_profile`, `~/.zshrc`, `~/.zshenv`, `~/.zprofile`, `~/.profile`, `~/.gitconfig`, `.git/hooks`

**Note:** `~/.zshenv` is especially dangerous — it executes for ALL zsh invocations including non-interactive shells.

## Allowed Paths

| Path | Why |
|------|-----|
| `~/.openclaw` | Config, logs, state |
| `/tmp`, `/var/folders` | Temp files |

## Trust Boundaries

```
UNTRUSTED: Telegram messages (until paired), external websites, AI outputs
SEMI-TRUSTED: Paired users, Claude API, Control UI with token
TRUSTED: Local config, explicit approvals, your shell
```

## Attack Scenarios

| Attack | Defense | Result |
|--------|---------|--------|
| Read `~/.ssh/id_rsa` | denyRead (kernel) | Blocked |
| POST to attacker.com | Proxy allowlist | 403 |
| Modify `~/.bashrc` | denyWrite (kernel) | Blocked |
| Raw socket bypass | Seatbelt network rules | Blocked (macOS) |

## Limitations

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| Docker socket access | Gateway needs `/var/run/docker.sock` for agent containers; compromised gateway could create privileged containers | Monitor Docker activity, audit container creation |
| Proxy bypass (macOS) | Mitigated: Seatbelt blocks ALL non-localhost outbound at kernel level, not just via proxy | Kernel enforcement is primary; proxy adds domain granularity |
| Proxy bypass (Linux) | `--unshare-net` provides true network namespace isolation | Stronger than macOS for network |
| Same-user context | Can read non-denyRead files | Keep denyRead comprehensive |
| Config tampering | Attacker modifies allowlist | Don't include ~/.srt-settings.json in allowWrite |

**Docker socket is the most significant gap.** The gateway requires Docker access to manage agent sandbox containers. SRT cannot restrict this without breaking legitimate operation. A compromised gateway with Docker socket access could create privileged containers that escape all containment.

## Recommendations

1. Minimal allowedDomains
2. Comprehensive denyRead
3. Monitor `~/.openclaw/logs/`
4. Rotate tokens periodically
5. Review pairing requests
