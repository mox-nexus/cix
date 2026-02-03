---
name: building-extensions
description: "Builds cognitive extensions with CI principles. Use when: creating skills, agents, hooks, commands, MCPs, or tools/APIs. Provides patterns for complementary (not substitutive) AI design."
---

# Building Extensions

Build things that make humans more capable, not dependent.

## The Core Problem

AI creates a dissociation: system performance goes up while human competence goes down.

| What Improves | What Degrades |
|---------------|---------------|
| Output speed | Critical thinking (r = -0.75) |
| Task completion | Procedural knowledge |
| Artifact quality | Debugging intuition |

**Extensions must preserve human capability, not just boost system performance.**

---

## The Mastery-Performance Split

How users approach AI determines outcomes more than the tool itself.

| Orientation | Behavior | Outcome |
|-------------|----------|---------|
| **Mastery** | Treats AI as collaborator, questions output | OR = 35.78 for critical thinking |
| **Performance** | Treats AI as oracle, accepts output | Z = -6.295 (6.3 std dev below mean) |

**Design for mastery orientation.** Extensions that optimize for speed inadvertently encourage performance orientation.

---

## The Review Pattern

Claude generates. The human reviews. What matters is whether the human CAN evaluate.

| Pattern | Effect |
|---------|--------|
| Output only | Human rubber-stamps (no basis for evaluation) |
| Output + reasoning | Human can evaluate logic |
| Output + alternatives + tradeoffs | Human makes informed judgment |

**Enable evaluation.** Show reasoning. Show what was considered and rejected. Make the logic inspectable.

---

## CI Design Patterns

### 1. Cognitive Friction (Feature, Not Bug)

Frictionless interfaces promote cognitive offloading. Add friction at decision points.

```
❌ [Accept]
✅ confirm --reason "..." (forces articulation)
```

**When to add friction:** Irreversible actions, high-stakes decisions, learning contexts.

### 2. Contrastive Explanations

Don't just recommend. Show the alternative.

```
❌ "Use X"
✅ "I recommend X instead of Y because Z"
```

Forces comparison between mental models. Triggers analytic processing over heuristic acceptance.

### 3. Glass Box (Reasoning Visible)

No black boxes. Show the reasoning trace.

- Link recommendations to source (which Skill justified this?)
- Make decision logic inspectable
- Enable users to fork and modify

### 4. Cognitive Velcro (Hooks for Mind)

Interfaces need texture for the mind to grip. Not Teflon.

**Confidence markers:** Not percentages (ignored). Use language:
- "I am **guessing** that..."
- "I have **verified** that..."

**Alternative acknowledgment:**
> "I considered Y but rejected it because..."

### 5. Observable Agents (Work Aloud)

Silent agents break team situational awareness.

```
❌ [Agent fixes bug silently]
✅ "I am modifying X, which may affect Y"
```

Agents should emit structured logs, mimicking human "chatter."

### 6. Reflection Prompts

Before high-impact actions:

> "What is the primary risk of this operation?"

If user cannot answer, pause or offer risk analysis.

### 7. Socratic Mode

For learning contexts, guide rather than answer:

```
❌ "Here is the fix"
✅ "Have you checked the access.log?"
```

Builds troubleshooting mental models.

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | CI Alternative |
|--------------|--------------|----------------|
| **Frictionless everything** | Promotes offloading | Friction at decision points |
| **Linguistic overconfidence** | Drives over-reliance | Calibrated hedging |
| **Silent agents** | Breaks Common Ground | Work aloud |
| **AI generates, human approves** | Passive reception | Human generates, AI critiques |
| **Efficiency-first refactoring** | Strips security "friction" | Immutable security constraints |
| **Speed metrics only** | Incentivizes offloading | Measure verification quality |

---

## Metrics

### Correction Rate

How often does user modify AI suggestions?

| Rate | Meaning |
|------|---------|
| < 5% | Rubber stamping (over-reliance) |
| 10-30% | Active collaboration |
| > 50% | Poor utility |

### Verification Latency

Time between generation and acceptance.

| Time | Meaning |
|------|---------|
| < 2 seconds | Blind acceptance |
| Sufficient to read | Healthy engagement |

---

## Extension Types

### Skills

| Do | Don't |
|----|-------|
| Decision frameworks | Prescriptions |
| What Claude doesn't know | Textbook basics |
| < 500 lines SKILL.md | Bloat |

### Agents

| Do | Don't |
|----|-------|
| One perspective (orthogonality) | Everything-agent |
| Work aloud | Silent execution |
| Suggest direction | Prescribe actions |

### Hooks

| Do | Don't |
|----|-------|
| Suggest, allow proceed | Block without escape |
| Show what triggered | Silent modification |

```json
{"decision": "allow", "message": "Consider X. Proceeding with Y."}
```

### Commands

| Do | Don't |
|----|-------|
| Checkpoints for verification | Long uninterruptible chains |
| Show what will happen | Surprise side effects |

---

## The Test

For every extension feature, ask:

1. Does this make users more capable or more dependent?
2. Does this preserve the generative step?
3. Does this encourage mastery or performance orientation?
4. Would users be helpless after extended use?

**Core directive:** Don't build tools that think FOR the user. Build tools that help the user think BETTER.

---

## References

| Need | Load |
|------|------|
| Skill authoring patterns | [skill-authoring.md](references/skill-authoring.md) |
| Plugin patterns (agents, hooks, commands) | [plugin-patterns.md](references/plugin-patterns.md) |
| Capability patterns (CLI, API) | [capability-patterns.md](references/capability-patterns.md) |
| Observability | [observability.md](references/observability.md) |
| Provenance/CoVE | [provenance-cove.md](references/provenance-cove.md) |
