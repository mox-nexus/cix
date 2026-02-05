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

## Protected Paths (denyRead)

| Path | Risk if Exposed |
|------|-----------------|
| `~/.ssh` | Server access, git push |
| `~/.aws` | Cloud infrastructure |
| `~/.config/gcloud` | GCP access |
| `~/.kube` | Cluster access |
| `~/.gnupg` | Signing keys |
| `~/Library/Keychains` | All credentials |
| `~/.docker` | Registry access |
| `~/.npmrc` | Package publishing |

## Persistence Vectors Blocked (denyWrite)

`~/.bashrc`, `~/.zshrc`, `~/.profile`, `~/.gitconfig`, `.git/hooks`

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
| Proxy-based filtering | Apps ignoring HTTP_PROXY bypass | macOS: seatbelt network; Linux: --unshare-net |
| Same-user context | Can read non-denyRead files | Keep denyRead comprehensive |
| Config tampering | Attacker modifies allowlist | Don't include ~/.srt-settings.json in allowWrite |

## Recommendations

1. Minimal allowedDomains
2. Comprehensive denyRead
3. Monitor `~/.openclaw/logs/`
4. Rotate tokens periodically
5. Review pairing requests
