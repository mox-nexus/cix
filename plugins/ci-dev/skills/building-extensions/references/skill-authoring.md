# Skill Authoring Patterns

Distilled from Anthropic's best practices.

Source: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

---

## Core Principles

### Conciseness

Context window is a public good. Challenge each token:
- Does Claude need this explanation?
- Can Claude already know this?
- Does this justify its token cost?

**Default assumption**: Claude is already very smart.

### Degrees of Freedom

| Freedom | Use When | Example |
|---------|----------|---------|
| **High** | Multiple valid approaches, context-dependent | Code review guidelines |
| **Medium** | Preferred pattern exists, some variation OK | Report templates with params |
| **Low** | Operations fragile, consistency critical | Database migrations |

**Analogy**: Narrow bridge (low freedom) vs open field (high freedom).

---

## Structure

### Naming

Use **gerund form** (verb + -ing):
- `processing-pdfs`
- `analyzing-spreadsheets`
- `building-extensions`

**Avoid**: `helper`, `utils`, `tools`, vague names.

### Description

Write in **third person**. Include what + when:

```yaml
description: "Builds CI extensions with transparency and control patterns. Use when: creating skills, agents, hooks, commands, MCPs, or tools/APIs."
```

**Avoid**: "I can help you...", "You can use this to..."

### Progressive Disclosure

| Level | Content | Token Cost |
|-------|---------|------------|
| Metadata | name + description | Always loaded |
| SKILL.md | < 500 lines | When activated |
| references/ | Unlimited | On demand |

Keep references **one level deep** from SKILL.md.

---

## Patterns

### Template Pattern

For strict requirements:
```markdown
ALWAYS use this exact template:
[template]
```

For flexible guidance:
```markdown
Sensible default, adapt as needed:
[template]
```

### Examples Pattern

Show input/output pairs:
```markdown
**Example 1:**
Input: [input]
Output: [output]
```

### Conditional Workflow

```markdown
1. Determine type:
   **Creating?** → Follow creation workflow
   **Editing?** → Follow editing workflow
```

### Feedback Loop

Run → validate → fix → repeat:
```markdown
1. Make changes
2. Validate: `python validate.py`
3. If fails: fix and return to step 2
4. Only proceed when validation passes
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Too verbose | Token waste | Assume Claude knows basics |
| Too many options | Decision paralysis | Provide default + escape hatch |
| Windows paths | Cross-platform errors | Always use forward slashes |
| Time-sensitive info | Goes stale | Use "old patterns" section |
| Deep nesting | Partial reads | Keep refs one level deep |
| Vague description | Poor activation | Include "Use when:" triggers |

---

## Checklist

Before shipping:

- [ ] Description specific with "Use when:"
- [ ] SKILL.md < 500 lines
- [ ] References one level deep
- [ ] No time-sensitive info
- [ ] Consistent terminology
- [ ] Concrete examples
- [ ] Workflows have clear steps
