---
name: ci-extension-design
description: "Design cognitive extensions for collaborative intelligence. Composes with plugin-dev for structure. Use when: building extensions that enhance human capability, applying transparency/control patterns, creating dual-content structure."
---

# CI Extension Design

Build extensions that make humans more capable, not dependent.

> **Composes with**: `plugin-dev` (structure, schemas) — this skill adds CI methodology.

## The Core Principle

```
Substitutive: AI does work → human approves → capability atrophies
Collaborative: AI amplifies → human decides → capability compounds
```

Every extension must be collaborative.

## Dual-Content Model

| For Claude | For Humans |
|------------|------------|
| `SKILL.md` (< 500 lines) | `docs/explanation/methodology.md` |
| `references/` (load on demand) | `docs/explanation/sources.md` |
| `templates/`, `scripts/` | |

**Claude ignores `docs/`** — human content wastes tokens and confuses actionable guidance.

**Goal**: Humans can learn, verify, and enhance.

## Transparency (β = 0.415)

Show reasoning so humans can evaluate:

```markdown
## When Recommending

| Show | Why |
|------|-----|
| The claim | What you're recommending |
| The reasoning | Why this approach |
| Alternatives | What you considered |
| Uncertainty | Confidence level |
| Sources | Where this comes from |
```

## Control Plane (β = 0.507, strongest)

Not "human initiates everything" — that's a bottleneck.

Control plane = ability to observe, steer, override when needed.

```markdown
## Control Patterns

| Pattern | Implementation |
|---------|----------------|
| Decision frameworks | Teach HOW to decide, not WHAT |
| Tradeoff tables | Options with tradeoffs, user chooses |
| Observability | Make behavior visible |
| Override capability | User can intervene when needed |
```

## Orthogonality Lock (for agents)

Each agent = one perspective. Refuse out-of-scope topics.

```markdown
## Orthogonality Lock

**Cannot discuss**: [out-of-scope topics]
**Must focus on**: [single domain]

If asked outside domain: "That's outside my orthogonality lock. {Agent} should assess that."
```

Forces synthesis across perspectives rather than single-agent tunnel vision.

## Hook Patterns

| Type | Purpose | Pattern |
|------|---------|---------|
| **Validation** | Review actions | Suggest, don't block |
| **Action-triggering** | Detect patterns | Directive: "You MUST now..." |

Validation hooks preserve agency. Action-triggering hooks interrupt problematic patterns.

## Extension Checklist

Before shipping:

- [ ] Collaborative, not substitutive
- [ ] Dual-content (Claude vs Human)
- [ ] Claude ignores `docs/`
- [ ] Transparency built in (reasoning visible)
- [ ] Control plane (observe, steer, override)
- [ ] Orthogonality (agents) or focused scope (skills)
- [ ] Sources traceable in `docs/explanation/sources.md`

## Structure Reference

```
plugin-name/
├── .claude-plugin/plugin.json
├── README.md
├── skills/
│   └── skill-name/
│       ├── SKILL.md           # Claude
│       └── references/        # Claude (load on demand)
├── agents/                    # With Orthogonality Locks
├── hooks/
├── templates/
├── scripts/
└── docs/
    └── explanation/           # Human only
        ├── methodology.md
        └── sources.md
```

For structural details (frontmatter, hooks API, etc.): use `plugin-dev` skills.
