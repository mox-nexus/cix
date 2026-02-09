# Evidence Workflow

Repeatable methodology for building evidence-grounded extensions. Every claim should be traceable.

---

## Contents

- [The Six Steps](#the-six-steps)
- [Step 1: Define Gap](#step-1-define-gap)
- [Step 2: Research Production Codebases](#step-2-research-production-codebases)
- [Step 3: Verify with Maintainers](#step-3-verify-with-maintainers)
- [Step 4: Identify Production Gotchas](#step-4-identify-production-gotchas)
- [Step 5: Draft the Skill](#step-5-draft-the-skill)
- [Step 6: Validate (CoVe)](#step-6-validate-cove)
- [Evidence Tracker Template](#evidence-tracker-template)

---

## The Six Steps

```
1. DEFINE GAP     → What does Claude get wrong or miss?
2. RESEARCH       → What do production codebases actually use?
3. VERIFY         → What do core maintainers recommend?
4. GOTCHAS        → What breaks in production that works in dev?
5. DRAFT          → Write the skill from evidence, not opinion
6. VALIDATE       → CoVe: verify each claim independently
```

---

## Step 1: Define Gap

Test what Claude already knows in the target domain. The gaps become the skill's content.

**Process:**
1. Ask Claude common questions in the domain without the skill loaded
2. Identify where responses are generic, outdated, or wrong
3. Note specific gaps: wrong defaults, missing gotchas, no decision framework

**Expected output:** 3-5 specific gaps that justify the skill's existence.

| Gap Type | Example |
|----------|---------|
| Wrong default | "Claude recommends X, but production uses Y" |
| Missing gotcha | "Claude doesn't warn about Z failure mode" |
| No framework | "Claude lists options but doesn't help decide" |
| Outdated | "Claude recommends deprecated pattern" |

---

## Step 2: Research Production Codebases

Find 3 production codebases in the domain:

| Source | Why |
|--------|-----|
| Most-starred project in ecosystem | Community consensus |
| Tool by domain experts | Expert judgment (e.g., ripgrep for Rust CLI) |
| Company production code | Battle-tested at scale (Cloudflare, Discord, 1Password) |

**For each, find:**
- What libraries/tools do they use?
- What patterns appear repeatedly?
- What did they avoid that's popular?

### Evidence Template

```markdown
## [Codebase Name]

**URL**: [GitHub link]
**What they use**: [specific tool/crate/library]
**Evidence**: [file path or quote]
**Notable absence**: [popular thing they don't use]
```

---

## Step 3: Verify with Maintainers

Find what core maintainers recommend:
- Conference talks or blog posts
- GitHub issues with design decisions
- Downloads/usage stats (crates.io, npm, etc.)
- Recent activity (last commit, last release)
- Known deprecations or migrations

### Evidence Template

```markdown
## [Tool] Maintainer Position

**Maintainer**: [name]
**Source**: [URL]
**Quote**: "[exact quote]"
**Downloads**: [X/week]
**Last release**: [date]
```

---

## Step 4: Identify Production Gotchas

Search for production issues and postmortems:
- "[tool] production issue"
- "[tool] postmortem"
- "[tool] we replaced"
- "[tool] gotcha"

**Look for:**
- Things that work in dev but fail in prod
- Performance cliffs
- Migration regrets

### Evidence Template

```markdown
## [Gotcha Title]

**Source**: [URL]
**The trap**: [what seemed fine]
**The failure**: [what went wrong]
**The fix**: [what to do instead]
```

---

## Step 5: Draft the Skill

Write from evidence, not opinion.

```markdown
---
name: [domain-name]
description: "[What it does]. Use when: [trigger 1], [trigger 2]."
---

# [Domain] Patterns

## Decision Framework

| Situation | Choice | Why |
|-----------|--------|-----|
| [Use case] | **[winner]** | Evidence: [source] |

## Production Gotchas

| Trap | Fix |
|------|-----|
| [Gotcha] | [Solution] |
```

Every decision should trace back to Step 2-4 evidence.

---

## Step 6: Validate (CoVe)

Chain-of-Verification: check each claim independently.

For each claim in the skill:

| Claim | Source | Quality | Contradictions? | Confidence |
|-------|--------|---------|-----------------|------------|
| [claim] | [where] | prod/maintainer/blog | [any?] | high/medium/low |

### Validation Checks

- [ ] Each decision traces to production evidence
- [ ] Gotchas come from real failures, not hypotheticals
- [ ] No unsourced assertions about performance or adoption
- [ ] Contradicting evidence acknowledged
- [ ] Confidence levels honest (not everything is "high")

---

## Evidence Tracker Template

Use this to collect all evidence before writing:

```markdown
# [Skill Name] Evidence

## Gap Analysis
- Gap 1: [Claude said X, but production uses Y]
- Gap 2: [Claude missed gotcha Z]
- Gap 3: [No decision framework for W]

## Production Codebases

### [Codebase 1]
- URL:
- Uses:
- Evidence:
- Avoids:

### [Codebase 2]
- URL:
- Uses:
- Evidence:
- Avoids:

### [Codebase 3]
- URL:
- Uses:
- Evidence:
- Avoids:

## Maintainer Positions

### [Tool 1]
- Maintainer:
- Source:
- Quote:
- Stats:

## Production Gotchas

### [Gotcha 1]
- Source:
- Trap:
- Failure:
- Fix:

## Decisions Ready to Draft

| Question | Answer | Evidence |
|----------|--------|----------|
| Best X for Y? | | |
| When to use Z? | | |
```
