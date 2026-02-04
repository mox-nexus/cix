---
name: building-extensions
description: "Builds extensions that enable effective collaboration. Use when: creating skills, agents, hooks, commands, MCPs, or tools/APIs. Implementation patterns for transparency, control, observability."
---

# Building Extensions

Extensions that enable effective human-AI collaboration.

For templates and structure, use `plugin-dev`. This skill adds implementation patterns for transparency, control, and observability.

---

## Transparency

Make reasoning visible.

| Extension | Implementation |
|-----------|----------------|
| **Skills** | Show sources, link claims to evidence |
| **Agents** | Work aloud (observations → conclusions → reasoning) |
| **Hooks** | Show what triggered the hook |
| **Commands** | Show intent before executing |
| **MCPs** | Rich errors (what + why + fix) |
| **CLI/API** | Verbose mode, explain what's happening |

### Patterns

```
❌ "Use X"
✅ "X instead of Y because Z"

❌ "80% confident"
✅ "I am guessing..." / "I have verified..."
```

---

## Control

Give users agency.

| Extension | Implementation |
|-----------|----------------|
| **Skills** | Decision frameworks (how to decide, not what) |
| **Agents** | Orthogonality (one perspective, user synthesizes) |
| **Hooks** | Suggest don't block, escape hatch, opt-out |
| **Commands** | Checkpoints before irreversible |
| **MCPs** | Bounded output, don't overwhelm |
| **CLI/API** | Dry-run, confirm destructive, 80/20 defaults |

### Patterns

```json
// Hooks: suggest, don't block
{"decision": "allow", "message": "Consider X instead. Proceeding with Y."}
```

```bash
# CLI: control surfaces
--dry-run     # show what would happen
--yes         # confirm destructive
--verbose     # show reasoning
```

---

## Observability

Make behavior traceable.

| Extension | Implementation |
|-----------|----------------|
| **Skills** | Progressive disclosure (metadata → SKILL.md → references) |
| **Agents** | Reasoning traces in output |
| **Hooks** | Structured logging, exit codes |
| **Commands** | Progress visibility |
| **MCPs** | OTel spans (mcp_call, success, duration_ms) |
| **CLI/API** | OTel instrumentation, structured logs |

### OTel Minimum

```python
span.set_attribute("success", True)
span.set_attribute("duration_ms", elapsed)
span.set_attribute("error", str(e) if failed else None)
```

---

## CLI/API for LLM Clients

Build capabilities that Claude can use effectively.

| Pattern | Implementation |
|---------|----------------|
| **LLM-friendly commands** | Structured output, clear contracts |
| **Bundle skill with tool** | Teach Claude how to use the capability |
| **Predictable output** | JSON/structured for parsing |
| **Rich errors** | What + why + fix (LLM can reason about) |

### Bundle Pattern

```
my-tool/
├── src/                    # The capability
├── .claude/skills/         # Skill teaching Claude how to use it
│   └── using-my-tool/
│       └── SKILL.md        # Decision frameworks, gotchas
└── pyproject.toml
```

---

## Pit of Success

Make the right thing obvious.

| Pattern | Implementation |
|---------|----------------|
| Safe defaults | Default to non-destructive |
| Dangerous = extra steps | Require `--yes` or confirmation |
| Constraints > docs | Structure prevents mistakes |

---

## Mistake-Proofing

Catch errors early.

| Pattern | Implementation |
|---------|----------------|
| Validate early | Check assumptions at start |
| Surface uncertainty | At decision points |
| Gotcha sections | "Watch out for" in skills |

---

## Validation Checklist

### Transparency
- [ ] Reasoning visible
- [ ] Sources cited
- [ ] Uncertainty stated
- [ ] Alternatives shown

### Control
- [ ] Decision frameworks, not mandates
- [ ] User can override
- [ ] Hooks suggest, don't block
- [ ] Opt-out documented

### Observability
- [ ] OTel instrumented (if applicable)
- [ ] Structured logging
- [ ] Behavior traceable

### LLM-Ready (CLI/API)
- [ ] Structured output
- [ ] Skill bundled
- [ ] Rich errors

---

## References

| Need | Load |
|------|------|
| CLI/API patterns | [capability-patterns.md](references/capability-patterns.md) |
| OTel instrumentation | [observability.md](references/observability.md) |
| Evidence patterns | [provenance-cove.md](references/provenance-cove.md) |
| Anthropic skill patterns | [skill-authoring.md](references/skill-authoring.md) |

For templates: use `plugin-dev` skill.
For methodology: see `explanations/`.
