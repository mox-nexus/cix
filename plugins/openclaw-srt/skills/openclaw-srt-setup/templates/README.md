# SRT Config Templates

Pre-configured network allowlists for different use cases.

## Quick Start

```bash
# Copy the template that fits your use case
cp templates/srt-minimal.json ~/.srt-settings.json

# Or for the full-featured default
cp templates/srt-settings.json ~/.srt-settings.json
```

---

## Available Templates

| Template | File | Domains | Use Case |
|----------|------|---------|----------|
| **Minimal** | `srt-minimal.json` | 2 | Bare minimum - Claude API + Telegram only |
| **Default** | `srt-settings.json` | ~50 | General-purpose personal assistant |
| **AI Research** | `srt-ai-research.json` | ~45 | Monitoring AI labs, papers, news |
| **Developer** | `srt-developer.json` | ~40 | Coding help with external resources |
| **Job Hunting** | `srt-job-hunting.json` | ~50 | Job search and applications |

---

## Template Details

### Minimal (`srt-minimal.json`)

The most restrictive template. Use when you want absolute minimum network access.

**Domains allowed:**
| Domain | Purpose |
|--------|---------|
| `api.anthropic.com` | Claude API calls |
| `api.telegram.org` | Bot notifications |

**When to use:**
- Testing sandbox setup
- High-security environments
- When you don't need web access

**Limitations:**
- No web browsing capability
- No code repository access
- No research paper access

---

### Default (`srt-settings.json`)

A balanced template for general-purpose use. Combines job hunting, AI research, and development access.

**Domains allowed:**

| Category | Domains |
|----------|---------|
| **Core** | `api.anthropic.com`, `api.telegram.org` |
| **Job Sites** | `linkedin.com`, `*.linkedin.com`, `greenhouse.io`, `*.greenhouse.io`, `lever.co`, `*.lever.co`, `levels.fyi`, `*.levels.fyi`, `wellfound.com`, `*.wellfound.com`, `ycombinator.com`, `*.ycombinator.com`, `news.ycombinator.com`, `workatastartup.com`, `*.workatastartup.com` |
| **AI Labs** | `anthropic.com`, `*.anthropic.com`, `openai.com`, `*.openai.com`, `deepmind.google`, `*.deepmind.google` |
| **Research** | `arxiv.org`, `*.arxiv.org`, `huggingface.co`, `*.huggingface.co` |
| **Tech News** | `techcrunch.com`, `*.techcrunch.com`, `theverge.com`, `*.theverge.com`, `arstechnica.com`, `*.arstechnica.com`, `wired.com`, `*.wired.com` |
| **Social** | `x.com`, `*.x.com`, `twitter.com`, `*.twitter.com` |
| **Code** | `github.com`, `*.github.com`, `githubusercontent.com`, `*.githubusercontent.com` |

**When to use:**
- Personal AI assistant
- General research and browsing
- Light job search

---

### AI Research (`srt-ai-research.json`)

Focused on tracking AI developments, papers, and industry news.

**Domains allowed:**

| Category | Domains |
|----------|---------|
| **Core** | `api.anthropic.com`, `api.telegram.org` |
| **AI Labs** | `anthropic.com`, `*.anthropic.com`, `openai.com`, `*.openai.com`, `deepmind.google`, `*.deepmind.google`, `ai.meta.com`, `*.ai.meta.com`, `research.google`, `*.research.google`, `ai.google`, `*.ai.google`, `mistral.ai`, `*.mistral.ai` |
| **Research** | `arxiv.org`, `*.arxiv.org`, `huggingface.co`, `*.huggingface.co`, `paperswithcode.com`, `*.paperswithcode.com`, `semanticscholar.org`, `*.semanticscholar.org` |
| **Code** | `github.com`, `*.github.com`, `githubusercontent.com`, `*.githubusercontent.com` |
| **News** | `techcrunch.com`, `*.techcrunch.com`, `theverge.com`, `*.theverge.com`, `wired.com`, `*.wired.com`, `arstechnica.com`, `*.arstechnica.com`, `venturebeat.com`, `*.venturebeat.com`, `theinformation.com`, `*.theinformation.com` |
| **Social** | `x.com`, `*.x.com`, `twitter.com`, `*.twitter.com` |

**When to use:**
- Monitoring AI research papers
- Following AI lab announcements
- Industry news aggregation
- Building research summaries

---

### Developer (`srt-developer.json`)

Optimized for software development assistance.

**Domains allowed:**

| Category | Domains |
|----------|---------|
| **Core** | `api.anthropic.com`, `api.telegram.org` |
| **Code Hosting** | `github.com`, `*.github.com`, `githubusercontent.com`, `*.githubusercontent.com`, `gitlab.com`, `*.gitlab.com` |
| **Package Registries** | `npmjs.com`, `*.npmjs.com`, `registry.npmjs.org`, `yarnpkg.com`, `*.yarnpkg.com`, `crates.io`, `*.crates.io`, `pypi.org`, `*.pypi.org`, `pkg.go.dev`, `*.pkg.go.dev` |
| **Documentation** | `docs.rs`, `*.docs.rs`, `doc.rust-lang.org`, `*.doc.rust-lang.org`, `docs.python.org`, `*.docs.python.org`, `nodejs.org`, `*.nodejs.org`, `developer.mozilla.org`, `*.developer.mozilla.org`, `devdocs.io`, `*.devdocs.io` |
| **Q&A** | `stackoverflow.com`, `*.stackoverflow.com`, `stackexchange.com`, `*.stackexchange.com` |
| **Language Sites** | `rust-lang.org`, `*.rust-lang.org`, `python.org`, `*.python.org`, `golang.org`, `*.golang.org`, `typescriptlang.org`, `*.typescriptlang.org` |

**When to use:**
- Getting coding help
- Looking up API documentation
- Researching libraries and packages
- Debugging with Stack Overflow

---

### Job Hunting (`srt-job-hunting.json`)

Comprehensive access to job boards, ATS platforms, and company career pages.

**Domains allowed:**

| Category | Domains |
|----------|---------|
| **Core** | `api.anthropic.com`, `api.telegram.org` |
| **Professional Network** | `linkedin.com`, `*.linkedin.com` |
| **ATS Platforms** | `greenhouse.io`, `*.greenhouse.io`, `lever.co`, `*.lever.co`, `ashbyhq.com`, `*.ashbyhq.com`, `workday.com`, `*.workday.com`, `icims.com`, `*.icims.com`, `smartrecruiters.com`, `*.smartrecruiters.com`, `jobvite.com`, `*.jobvite.com` |
| **Job Boards** | `levels.fyi`, `*.levels.fyi`, `glassdoor.com`, `*.glassdoor.com`, `indeed.com`, `*.indeed.com`, `builtin.com`, `*.builtin.com` |
| **Startup Jobs** | `ycombinator.com`, `*.ycombinator.com`, `news.ycombinator.com`, `workatastartup.com`, `*.workatastartup.com`, `wellfound.com`, `*.wellfound.com` |
| **Big Tech Careers** | `careers.google.com`, `jobs.apple.com`, `amazon.jobs`, `*.amazon.jobs`, `careers.microsoft.com`, `*.careers.microsoft.com`, `meta.com`, `*.meta.com` |
| **AI Companies** | `anthropic.com`, `*.anthropic.com`, `openai.com`, `*.openai.com`, `deepmind.google`, `*.deepmind.google` |
| **Code** | `github.com`, `*.github.com` |

**When to use:**
- Active job search
- Researching companies
- Tracking job postings
- Preparing applications

---

## Filesystem Restrictions

All templates share the same filesystem security rules:

### Blocked from reading

These paths contain sensitive credentials and are never accessible:

```
~/.ssh              # SSH keys
~/.gnupg            # GPG keys
~/.aws              # AWS credentials
~/.config/gcloud    # Google Cloud credentials
~/Library/Keychains # macOS keychain
~/.password-store   # pass password manager
~/.1password        # 1Password CLI
~/.kube             # Kubernetes config
~/.docker           # Docker credentials
~/.npmrc            # NPM tokens
```

### Allowed to write

Sandboxed processes can only write to:

```
~/.openclaw         # OpenClaw state and logs
/tmp                # Temporary files
/var/folders        # macOS temp folders
```

### Blocked from writing

Even within allowed areas, these are protected:

```
~/.bashrc           # Shell config
~/.zshrc            # Zsh config
~/.profile          # Profile config
~/.gitconfig        # Git config
.git/hooks          # Git hooks (any repo)
```

---

## Customization

### Adding domains

Edit your `~/.srt-settings.json`:

```json
{
  "network": {
    "allowedDomains": [
      "api.anthropic.com",
      "api.telegram.org",
      
      "mynewdomain.com",
      "*.mynewdomain.com"
    ]
  }
}
```

**Important:** Always add both the base domain and wildcard:
- `*.example.com` matches `www.example.com`, `api.example.com`
- `*.example.com` does NOT match `example.com`

### Combining templates

Merge domain lists from multiple templates:

```bash
# Using jq
jq -s '.[0] * {network: {allowedDomains: (.[0].network.allowedDomains + .[1].network.allowedDomains | unique)}}' \
  srt-developer.json srt-ai-research.json > ~/.srt-settings.json
```

Or manually copy the `allowedDomains` arrays and combine them.

### Changing filesystem rules

To add a new protected path:

```json
{
  "filesystem": {
    "denyRead": [
      "~/.ssh",
      "~/.custom-secrets"
    ]
  }
}
```

To allow writing to a new path:

```json
{
  "filesystem": {
    "allowWrite": [
      "~/.openclaw",
      "/tmp",
      "~/my-project/output"
    ]
  }
}
```

### Removing restrictions

To allow a domain not in the template, add it to `allowedDomains`.

To allow reading a blocked path, remove it from `denyRead` (not recommended for credential directories).

---

## Validation

Check your config is valid JSON:

```bash
# Using Python
python3 -m json.tool ~/.srt-settings.json

# Using jq
jq . ~/.srt-settings.json
```

Test the config:

```bash
# Should succeed (allowed domain)
srt --settings ~/.srt-settings.json -- curl -s https://api.anthropic.com

# Should fail (not in allowlist)
srt --settings ~/.srt-settings.json -- curl -s https://random-blocked-site.com
```

---

## Common Issues

1. **Domain blocked but looks like it should work**
   - Check for both base domain AND wildcard
   - `*.example.com` does NOT match `example.com`

2. **Config changes not taking effect**
   - Restart the daemon: `launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway`

3. **JSON parse errors**
   - Check for trailing commas (not allowed in JSON)
   - Validate with `python3 -m json.tool`

See [gotchas.md](../references/gotchas.md) for more troubleshooting.
