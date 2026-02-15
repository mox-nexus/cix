# Why the Optimizer Works This Way

The optimizer agent fixes issues identified by the evaluator. This document explains the fix strategies and why they work.

---

## Fix Philosophy

### Surgical, Not Sweeping

The optimizer makes **minimal targeted changes**. Why?

1. **Preserve intent:** Large rewrites lose the author's original purpose
2. **Verify incrementally:** Small changes can be verified; large changes can't
3. **Reduce risk:** Minimal changes have minimal blast radius

### Priority Order

```
Critical → Major → Minor
```

Why this order?
- Critical issues block functionality or violate core principles
- Major issues reduce effectiveness but don't block
- Minor issues are polish—important but not urgent

Fixing in order prevents wasted effort on polish when foundations are broken.

---

## Anti-Pattern Fixes

### LLM Tell-Tales

| Avoid | Use Instead |
|-------|-------------|
| delve | explore, examine |
| leverage | use |
| robust | reliable, solid |
| comprehensive | complete, full |
| utilize | use |
| facilitate | help, enable |

**Why these matter:** Tell-tales signal low-effort AI-generated content. They don't add meaning and waste tokens. Plain language is clearer and more trustworthy.

### Options Without Picks

**Before:**
```markdown
You could use A, B, or C.
```

**After:**
```markdown
| Situation | Use | Why |
|-----------|-----|-----|
| Default | A | Fastest, best maintained |
| Legacy | B | Works with Node 14 |
```

**Why this matters:** Options without picks create decision paralysis. Extensions should provide decision frameworks—HOW to choose—not just catalogs. This preserves user agency (Control β = 0.507) while providing value.

### Missing Sources

**Before:**
```markdown
This approach is 10x faster.
```

**After:**
```markdown
This approach is 10x faster (Source: [Benchmark](url)).
```

**Why this matters:** Unsourced claims can't be verified or trusted. Transparency (β = 0.415) requires traceability. Users need to know where claims come from to calibrate trust.

### Rigid Mandates

**Before:**
```markdown
Always use X. Never use Y.
```

**After:**
```markdown
| Context | Use | Why |
|---------|-----|-----|
| High throughput | X | Better under load |
| Simple scripts | Y | Less overhead |
```

**Why this matters:** Rigid mandates remove agency (Control β = 0.507). Decision frameworks preserve it by showing WHEN and WHY, not just WHAT.

---

## Escalation Rules

### Escalate When

- **Contradictory requirements:** Can't satisfy both without human decision
- **Missing domain expertise:** Fix requires knowledge optimizer doesn't have
- **Major structural change:** Scope exceeds targeted fixes
- **Unclear what to cut:** Removing content requires author intent
- **Sources can't be found:** Can't verify or cite without research

### Don't Escalate

- **Mechanical fixes:** Typos, formatting, boilerplate
- **Clear anti-patterns:** Tell-tales, missing picks, vague triggers
- **Obvious improvements:** Adding "Use when:", citing known sources

The boundary: optimizer fixes execution problems, not strategy problems. Strategy requires human judgment.

---

## Verification

After each fix:

1. **SKILL.md still < 500 lines?** Token budget matters
2. **Frontmatter intact?** Metadata must remain valid
3. **No broken references?** Links and paths still work
4. **Fix actually addresses issue?** Re-check against evaluator criteria

Why verify? Fixes can introduce new problems. Incremental verification catches them early.

---

## The Report

The optimizer produces a report because:

1. **Transparency:** Human can see what changed and why
2. **Learning:** Human can understand the patterns being fixed
3. **Audit:** Changes are traceable and reversible
4. **Handoff:** Deferred issues are clearly documented

This follows the Glass Box pattern—make the process inspectable, not just the output.
