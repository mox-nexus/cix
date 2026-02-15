# SRT Templates: Choosing Your Security Profile

## The Decision in 30 Seconds

```
Do you need internet access beyond Claude API?
├── No  → minimal (2 domains)
└── Yes → What kind of tasks?
    ├── General assistant    → default (~20 domains)
    ├── AI/ML research       → ai-research (~30 domains)
    ├── Software development → developer (~50 domains)
    └── Job searching        → job-hunting (~25 domains)
```

**Can't decide?** Start with **default**. Add domains as needed.

---

## Example: What Each Template Allows

### minimal
```json
"allowedDomains": [
  "api.anthropic.com",
  "api.telegram.org"
]
```

Claude works. Telegram works. Nothing else. Maximum security.

### default
Adds:
- Search engines (Google, DuckDuckGo)
- Documentation (MDN, devdocs.io)
- News sources (BBC, Reuters)

Still blocks social media, file sharing, arbitrary webhooks.

### developer
Adds everything from default, plus:
- `github.com`, `*.github.com`
- `npmjs.com`, `pypi.org`
- `stackoverflow.com`
- Package registries, code hosting

### ai-research
Adds everything from default, plus:
- `arxiv.org`, `huggingface.co`
- `paperswithcode.com`
- AI company blogs (Anthropic, OpenAI, DeepMind)

### job-hunting
Adds everything from default, plus:
- `linkedin.com`, `*.linkedin.com`
- `greenhouse.io`, `lever.co`
- `indeed.com`, `glassdoor.com`

---

## The Security Tradeoff

Every allowed domain is a potential exfiltration path.

```
Maximum Security ◄───────────────────────────────► Maximum Functionality
   │                                                      │
   │  Smallest attack surface                              │  Largest attack surface
   │  Most restrictions                                    │  Least restrictions
   │                                                      │
   └── minimal ── default ── developer/ai-research ────────┘
         │           │              │
      2 domains  ~20 domains   ~50 domains
```

**The question:** What's your threat model?

- **High paranoia**: Use minimal, add domains one by one
- **Balanced**: Use default or specialized template
- **Low concern**: Use developer, maybe add more

There's no universal "right" answer. It depends on what you're defending against.

---

## Why Multiple Templates?

Network allowlists embody a security tradeoff: **access vs. attack surface**.

Every allowed domain increases functionality but also creates an exfiltration path. Every blocked domain reduces risk but limits what Claude can do for you.

Templates encode different points on this spectrum. Choose based on your use case and risk tolerance.

---

## Filesystem Rules (Same for All)

All templates share filesystem restrictions:

| Path | Rule | Why |
|------|------|-----|
| `~/.ssh` | denyRead | SSH keys stay protected |
| `~/.aws` | denyRead | Cloud credentials stay protected |
| `~/.gnupg` | denyRead | GPG keys stay protected |
| `~/.kube` | denyRead | Kubernetes credentials stay protected |
| `~/.bashrc`, `~/.zshrc` | denyWrite | Prevents persistence backdoors |
| `~/.openclaw` | allowWrite | Required for operation |
| `/tmp` | allowWrite | Scratch space |

Network allowlists vary by template. Filesystem rules don't - credentials are credentials regardless of use case.

---

## The Wildcard Trap

**Critical gotcha:** Wildcards do NOT match the base domain.

```json
// Wrong: Only subdomain
"allowedDomains": ["*.linkedin.com"]

// Right: Both patterns
"allowedDomains": [
  "linkedin.com",
  "*.linkedin.com"
]
```

`*.linkedin.com` matches `www.linkedin.com` and `api.linkedin.com` but NOT `linkedin.com` itself.

Always include both the base domain and wildcard pattern.

---

## Combining Templates

Templates aren't mutually exclusive.

**Merge with jq:**
```bash
jq -s '.[0].allowedDomains + .[1].allowedDomains | unique' \
  srt-developer.json srt-ai-research.json > combined.json
```

**Start minimal, add specifics:**
```json
{
  "allowedDomains": [
    "api.anthropic.com",
    "api.telegram.org",
    "your-specific-domain.com",
    "*.your-specific-domain.com"
  ]
}
```

---

## Custom Templates

When pre-built templates don't fit:

1. Start with the closest template
2. Copy to `~/.srt-settings.json`
3. Add/remove domains as needed
4. Validate: `python3 -m json.tool ~/.srt-settings.json`
5. Test: `bash scripts/verify-sandbox.sh`

**Document your changes.** Future you will forget why that random domain is there.

---

## Template Philosophy

### minimal

**Threat model:** Assume compromise. Zero trust.

Only allows what's required for OpenClaw core functionality. If the agent gets compromised, it can't reach anything useful to an attacker.

**Use when:** Running untrusted prompts, maximum paranoia, research scenarios.

### default

**Threat model:** Balanced security for general use.

Adds common productivity domains but still blocks high-risk categories (social media, file sharing, pastebin services).

**Use when:** General assistant tasks, don't need specialized access.

### ai-research

**Threat model:** Trust AI/ML ecosystem sites.

Adds research infrastructure for staying current on AI developments, reading papers, exploring models.

**Use when:** Literature review, model exploration, following AI research.

### developer

**Threat model:** Trust developer ecosystem.

Adds development infrastructure for coding assistance, package research, debugging help.

**Use when:** Software development, debugging, dependency research.

### job-hunting

**Threat model:** Trust job platforms.

Adds recruitment infrastructure for job search, application tracking, interview prep.

**Use when:** Actively searching for jobs, researching companies, networking.

---

## Choosing Your Template: The Full Decision Tree

```
┌─ What are you using OpenClaw for?
│
├─ Basic AI assistant (chat, questions)
│  └─→ default
│
├─ Software development
│  ├─ AND also AI/ML research
│  │  └─→ Merge developer + ai-research
│  └─ Just coding
│     └─→ developer
│
├─ AI/ML research only
│  └─→ ai-research
│
├─ Job hunting
│  └─→ job-hunting
│
└─ Maximum security (research, testing)
   └─→ minimal
```

---

## Threat Model Examples

### Personal Productivity (default)

You want Claude to help with research, writing, general questions. You trust the AI but want protection against prompt injection attacks.

**Risk:** Accidental data leakage through clipboard hijacking, malicious prompts.

**Protection:** Credentials blocked, only approved sites reachable.

### Software Development (developer)

You want coding assistance, package lookups, debugging help. You need access to GitHub, Stack Overflow, package registries.

**Risk:** Prompt injection leading to code exfiltration, supply chain attacks.

**Protection:** Credentials blocked, only development sites reachable (not social media, file sharing).

### Research Sandbox (minimal)

You're testing prompt injection techniques, running untrusted inputs, researching AI safety.

**Risk:** Intentionally adversarial inputs, worst-case scenarios.

**Protection:** Only Claude API allowed. Even if compromised, nowhere to send data.

---

## Further Reading

- [methodology.md](methodology.md) - Why sandbox at all
- [add-domain.md](../how-to/add-domain.md) - How to add domains to your template
- [security-model.md](../../skills/openclaw-srt-setup/references/security-model.md) - Detailed threat analysis
