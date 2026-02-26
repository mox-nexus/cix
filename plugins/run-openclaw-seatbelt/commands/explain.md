---
name: explain
description: "Explain OpenClaw + SRT architecture, security model, or templates"
arguments:
  - name: topic
    description: "Topic to explain: architecture, security, templates, or (blank for overview)"
    required: false
---

# Explain OpenClaw + SRT

Explain the architecture, security model, templates, or common gotchas for OpenClaw with SRT sandboxing.

## Usage

```
/explain [topic]
```

**Topics:**
- `architecture` - How the pieces fit together
- `security` - What is protected and why
- `templates` - SRT config templates and when to use each
- (no topic) - Brief overview

---

## Instructions for Claude

### If no topic provided (default)

**Read:** None (provide from memory)

**Provide:**

> **OpenClaw + SRT** runs your personal AI assistant inside a security sandbox.
>
> **What it protects:**
> - Credentials: `~/.ssh`, `~/.aws`, `~/.gnupg`, `~/.kube` (blocked)
> - Network: Only approved domains reachable
> - Persistence: Shell configs like `~/.bashrc` (write-blocked)
>
> **How it works:**
> - **OpenClaw** - Personal AI gateway (Telegram, web UI, Claude API)
> - **SRT** - Sandbox wrapper (network filtering, filesystem restrictions)
> - **Integration** - SRT wraps OpenClaw: `srt --settings config -- node openclaw`
>
> Use `/explain architecture` for how it works, `/explain security` for threat model, or `/explain templates` for config choices.

### If topic is "architecture"

**Read:** `/Users/yza.vyas/mox/cix/plugins/run-openclaw-srt/docs/explanation/architecture.md`

**Summarize:**
- Two systems: OpenClaw (AI gateway) and SRT (sandbox wrapper)
- OpenClaw components: Channels (Telegram, UI) → Router → Claude Provider
- SRT components: OS sandbox (sandbox-exec/bubblewrap) + Network proxy
- How they combine: Process wrapping with domain filtering
- Key insight: Proxy-based network filtering (not IP-based)
- Key gotcha: The `--` separator (Commander.js CLI parsing)

**Point to:** "See `docs/explanation/architecture.md` for full diagrams."

### If topic is "security"

**Read:** `/Users/yza.vyas/mox/cix/plugins/run-openclaw-srt/docs/explanation/methodology.md`

**Summarize:**
- Concrete threat: Prompt injection leading to credential theft
- Three attack surfaces: Filesystem, network, persistence
- How SRT mitigates: OS-level enforcement (kernel, not app-level)
- What's protected: Credentials, shell configs
- What's allowed: OpenClaw config dir, temp files, approved domains
- Honest limitations: Kernel exploits, physical access, side-channels

**Point to:** "See `docs/explanation/methodology.md` for attack scenarios and security rationale."

### If topic is "templates"

**Read:** `/Users/yza.vyas/mox/cix/plugins/run-openclaw-srt/docs/explanation/templates.md`

**Summarize:**
- Five templates: minimal, default, developer, ai-research, job-hunting
- Security tradeoff: Access vs attack surface
- Template spectrum: 2 domains (minimal) to ~50 domains (developer)
- Decision tree: Use case determines template
- Critical gotcha: Wildcard `*.example.com` doesn't match `example.com`
- Filesystem rules: Same for all templates (credentials always blocked)

**Point to:** "See `docs/explanation/templates.md` for the full decision tree and threat model examples."

---

## Example Conversations

**User:** `/explain`

**Claude:**
> **OpenClaw + SRT** runs your personal AI assistant inside a security sandbox.
>
> **What it protects:**
> - Credentials: `~/.ssh`, `~/.aws`, `~/.gnupg` blocked
> - Network: Only approved domains reachable
> - Persistence: Shell configs write-blocked
>
> **How it works:** SRT wraps OpenClaw with OS-level restrictions (kernel-enforced, not app-level).
>
> Use `/explain architecture` for component details, `/explain security` for threat model, or `/explain templates` for config choices.

**User:** `/explain templates`

**Claude:**
> **SRT Templates** let you choose your security profile.
>
> **Quick decision:**
> - General use → `default` (~20 domains)
> - Software dev → `developer` (~50 domains)
> - AI research → `ai-research` (~30 domains)
> - Max security → `minimal` (2 domains: just Claude API + Telegram)
>
> **Security tradeoff:** More domains = more functionality but larger attack surface.
>
> **Critical gotcha:** Wildcard `*.example.com` does NOT match `example.com`. Always include both:
> ```json
> "allowedDomains": ["example.com", "*.example.com"]
> ```
>
> See `docs/explanation/templates.md` for the full decision tree.

---

## Notes

- Keep responses concise (3-4 paragraphs max unless user asks for more)
- Always point to the full doc for details
- Use concrete examples over abstract explanations
- Mention the critical gotchas (wildcard matching, `--` separator)
