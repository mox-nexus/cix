# SRT Config Templates

Pre-configured network allowlists for different use cases.

## Available Templates

| Template | Use Case | Domains |
|----------|----------|---------|
| `srt-minimal.json` | Bare minimum | Claude API + Telegram only |
| `srt-settings.json` | Full featured | Job hunting + AI news + dev (default) |
| `srt-ai-research.json` | AI researcher | Labs, arXiv, HuggingFace, papers |
| `srt-developer.json` | Developer | GitHub, npm, docs, Stack Overflow |
| `srt-job-hunting.json` | Job seeker | LinkedIn, Greenhouse, Lever, job boards |

## Usage

```bash
# Copy the template that fits your use case
cp ~/.claude/plugins/openclaw-srt/skills/openclaw-srt-setup/templates/srt-minimal.json ~/.srt-settings.json

# Customize as needed
nano ~/.srt-settings.json
```

## Combining Templates

Need multiple use cases? Merge the `allowedDomains` arrays:

```bash
# Use jq to merge (if installed)
jq -s '.[0] * {network: {allowedDomains: (.[0].network.allowedDomains + .[1].network.allowedDomains | unique)}}' \
  srt-developer.json srt-ai-research.json > ~/.srt-settings.json
```

Or manually copy domains from multiple templates into one file.

## Template Details

### srt-minimal.json

**For:** Testing, locked-down environments

**Allows:**
- `api.anthropic.com` - Claude API
- `api.telegram.org` - Bot notifications

**Use when:** You want absolute minimum network access.

---

### srt-settings.json (Default)

**For:** Personal AI assistant with broad utility

**Allows:**
- Claude API + Telegram
- Job sites (LinkedIn, Greenhouse, Lever, etc.)
- AI labs (Anthropic, OpenAI, DeepMind)
- Research (arXiv, HuggingFace)
- Tech news (TechCrunch, Verge, Ars Technica)
- Social (X/Twitter)
- Dev (GitHub)

**Use when:** You want a general-purpose assistant.

---

### srt-ai-research.json

**For:** Tracking AI research and industry news

**Allows:**
- All major AI labs (Anthropic, OpenAI, DeepMind, Meta AI, Google AI, Mistral)
- Research platforms (arXiv, HuggingFace, Papers With Code, Semantic Scholar)
- Tech news sources
- GitHub for code repos
- X/Twitter for announcements

**Use when:** You're monitoring AI developments.

---

### srt-developer.json

**For:** Software development assistance

**Allows:**
- Code hosting (GitHub, GitLab)
- Package registries (npm, crates.io, PyPI, Go modules)
- Documentation sites (docs.rs, MDN, DevDocs)
- Q&A (Stack Overflow)
- Language sites (Rust, Python, Go, TypeScript)

**Use when:** You want coding help with external resources.

---

### srt-job-hunting.json

**For:** Job search assistance

**Allows:**
- LinkedIn (networking, jobs)
- ATS platforms (Greenhouse, Lever, Ashby, Workday, etc.)
- Job boards (Indeed, Glassdoor, Levels.fyi, Built In)
- Startup jobs (Y Combinator, Wellfound)
- Big tech careers (Google, Apple, Amazon, Microsoft, Meta)
- AI companies (Anthropic, OpenAI, DeepMind)

**Use when:** You're actively job hunting.

---

## Security Notes

All templates include the same filesystem restrictions:

**Blocked from reading:**
- `~/.ssh` - SSH keys
- `~/.aws`, `~/.kube`, `~/.docker` - Cloud credentials
- `~/.gnupg` - GPG keys
- `~/Library/Keychains` - macOS keychain
- `~/.password-store`, `~/.1password` - Password managers
- `~/.npmrc` - NPM tokens

**Allowed to write:**
- `~/.openclaw` - OpenClaw state
- `/tmp`, `/var/folders` - Temp files

**Blocked from writing:**
- `~/.bashrc`, `~/.zshrc`, `~/.profile` - Shell configs
- `~/.gitconfig`, `.git/hooks` - Git configs

## Adding Custom Domains

Edit your `~/.srt-settings.json`:

```json
"allowedDomains": [
  // ... existing domains ...

  "mycustomdomain.com",
  "*.mycustomdomain.com"
]
```

**Remember:** `*.example.com` does NOT match `example.com`. Include both if needed.
