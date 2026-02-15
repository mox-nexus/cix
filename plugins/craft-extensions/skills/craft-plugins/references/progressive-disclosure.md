# Progressive Disclosure

Minimize token usage while maintaining specialized expertise.

---

## Contents

- [The Three Levels](#the-three-levels)
- [What Goes Where](#what-goes-where)
- [Sizing Guidelines](#sizing-guidelines)
- [Reference Organization](#reference-organization)

---

## The Three Levels

### Level 1: Metadata (Always Loaded)

YAML frontmatter appears in Claude's system prompt for all enabled capabilities.

```yaml
---
name: analyzing-data
description: "Statistical analysis for CSV files. Use when: user asks to 'analyze data', uploads .csv, or mentions 'patterns' or 'statistics'."
---
```

**Budget:** ~100 tokens. Every word counts.

### Level 2: Main Content (When Activated)

SKILL.md body loads when Claude determines the capability is relevant.

```markdown
# Analyzing Data

## Decision Framework
[When to use what approach]

## Core Workflow
[Main steps]

## Gotchas
[Common mistakes]
```

**Budget:** < 500 lines. Core instructions only.

### Level 3: References (On Demand)

Additional files Claude can choose to read when needed.

```
references/
├── statistical-methods.md
├── edge-cases.md
└── examples.md
```

**Budget:** Unlimited, but one level deep only.

---

## What Goes Where

| Content Type | Level | Rationale |
|--------------|-------|-----------|
| Name + triggers | 1 (Metadata) | Needed for activation decision |
| When to use | 1 (Metadata) | Must be visible without loading |
| Core workflow | 2 (Main) | Essential instructions |
| Decision frameworks | 2 (Main) | Needed during execution |
| Gotchas, common mistakes | 2 (Main) | Prevent errors |
| Detailed examples | 3 (Reference) | Load only when helpful |
| Edge cases | 3 (Reference) | Rare, load on demand |
| API reference | 3 (Reference) | Detailed, load when needed |
| Historical context | 3 (Reference) | Background, rarely needed |

---

## Sizing Guidelines

### Metadata

- 1-2 sentences max
- Include "Use when:" triggers
- No XML tags (security restriction)

### Main Content

- Target: 200-400 lines
- Max: 500 lines
- If exceeding, move detail to references

### Reference Files

- TOC required if > 100 lines
- One level deep from SKILL.md
- No subdirectories

---

## Reference Organization

### Naming

Use descriptive kebab-case:

| Good | Bad |
|------|-----|
| statistical-methods.md | stats.md |
| error-handling.md | errors.md |
| migration-guide.md | migrate.md |

### Structure

Each reference file should be self-contained:

```markdown
# Title

Brief description of what this covers.

---

## Contents

- [Section 1](#section-1)
- [Section 2](#section-2)

---

## Section 1

[Content]

---

## Section 2

[Content]
```

### Linking

From main content, link clearly:

```markdown
For statistical method details, see [statistical-methods.md](references/statistical-methods.md).
```
