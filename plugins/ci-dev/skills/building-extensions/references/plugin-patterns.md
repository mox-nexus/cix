# Plugin Patterns

Building Claude Code extensions with CI principles.

## Skills

### The Filter

```
Claude already knows this? → YES → Cut it
Non-obvious insight? → NO → Cut it
```

| Include | Cut |
|---------|-----|
| Production gotchas | Basic syntax |
| Decision frameworks | Textbook examples |
| What Claude gets wrong | Complete tutorials |
| Non-obvious tradeoffs | Generic explanations |

### SKILL.md Anatomy

```yaml
---
name: skill-name
description: "What it does. Use when: specific triggers."
---
```

**Body structure:**
1. Brief intro (1-2 sentences)
2. Why this approach (practical motivation)
3. Core content (decision tables, workflows)
4. References section (what to load when)

### Progressive Disclosure

| Level | Content | When Loaded |
|-------|---------|-------------|
| Metadata | ~100 words, triggers | Always |
| SKILL.md | < 500 lines, decisions | When activated |
| References | Unlimited depth | On demand |

### Reference Navigation

```markdown
## References

| Need | Load |
|------|------|
| Detailed patterns | [patterns.md](references/patterns.md) |
| Full examples | [examples.md](references/examples.md) |
| Research sources | [sources.md](references/sources.md) |
```

---

## Agents

### Orthogonality Lock

Each agent = one perspective. Refuse out-of-scope.

```markdown
## Orthogonality Lock

**Cannot discuss**: [out-of-scope topics]
**Must focus on**: [single domain]

If asked outside domain:
"That's outside my orthogonality lock. {Agent} should assess that."
```

### Agent Frontmatter

```yaml
---
name: agent-name
description: |
  What this agent does. When to trigger.

  <example>
  Context: [Situation]
  user: "[Request]"
  assistant: "[How to respond]"
  <commentary>[Why this triggers]</commentary>
  </example>

model: inherit
color: blue
tools: [Read, Grep, Glob]
---
```

### Reasoning Traces

Always show:
- What you observed
- What you concluded
- Why (brief reasoning)
- Uncertainty level

---

## Hooks

### Suggest, Don't Block

```json
{"decision": "allow", "message": "Consider X instead. Proceeding with Y."}
```

**Not:**
```json
{"decision": "block", "message": "Use X instead."}
```

### Hook Events

| Event | When | Use For |
|-------|------|---------|
| `PreToolUse` | Before tool | Validate, suggest alternatives |
| `PostToolUse` | After tool | Log, check results |
| `Stop` | Session ends | Cleanup, summary |
| `SessionStart` | Session begins | Context injection |
| `UserPromptSubmit` | User sends prompt | Pattern detection |

### Opt-Out Required

Every hook must:
- Document how to disable
- Respect `SKIP_HOOKS=1`
- Never hard-block without escape

---

## Commands

### Workflow Checkpoints

```markdown
# /deploy

## Phase 1: Validate
Show what will be deployed. Stop for confirmation.

## Phase 2: Build
Build artifacts. Show progress.

## Phase 3: Deploy
Deploy with rollback plan. Confirm before proceeding.
```

### Command Frontmatter

```yaml
---
name: command-name
description: What this command does
arguments:
  - name: target
    description: What to operate on
    required: true
---
```

---

## MCPs

### Tool Contracts

Each tool must have:
- Clear input schema
- Predictable output format
- Rich error messages

```python
@mcp.tool()
async def search(query: str, limit: int = 20) -> list[SearchResult]:
    """Search the corpus.

    Args:
        query: Search terms
        limit: Maximum results (default 20)

    Returns:
        List of matching results with scores
    """
```

### Error Context

```python
try:
    result = await corpus.search(query)
except ConnectionError:
    raise MCPError(
        code="CONNECTION_FAILED",
        message="Cannot connect to corpus",
        details={"path": str(corpus_path)},
        hint="Check that the corpus file exists"
    )
```

---

## Quality Checklist

### Content
- [ ] Fills gaps (what Claude doesn't know)
- [ ] Decisions, not tutorials
- [ ] Claims have sources

### CI Principles
- [ ] Reasoning visible
- [ ] User can steer/override
- [ ] Explains WHY

### Activation
- [ ] Description has "Use when:"
- [ ] Triggers correctly
- [ ] Doesn't over-activate

### Observability
- [ ] Hooks suggest, don't block
- [ ] Opt-out documented
- [ ] Behavior traceable
