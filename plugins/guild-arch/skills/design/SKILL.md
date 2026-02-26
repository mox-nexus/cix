---
name: design
description: This skill should be used when the user asks to "review code design", "check API design", "evaluate abstractions", "review naming", "design an API", or discusses code quality, interface design, API contracts, or developer experience.
---

# Design

Multi-perspective design evaluation through Guild reasoning.

## What This Adds

Claude already knows SOLID, REST, GraphQL, gRPC, naming conventions, and design patterns. This skill doesn't reteach those — it adds **orthogonal architectural perspectives** that catch issues no single viewpoint reveals.

## The Three Design Lenses

### Karman (Ontological) — Does the model match reality?

The question isn't "is this clean code?" — it's "does this model the actual domain?"

**Karman's Tests:**
- Can you explain each entity without referencing implementation?
- Would a domain expert recognize these names?
- If the business changes, which abstractions break?
- Are you modeling the domain or modeling the database?

**What Karman catches that Claude alone misses:**
- Anemic domain models (data bags without behavior)
- Abstraction drift (code says "Order" but means "ShoppingCartSnapshot")
- Naming that satisfies developers but confuses domain experts
- God classes that merge distinct bounded contexts

### Ace (Psychocentric) — Can the next developer understand this?

Not "is this well-documented?" — but "is the door handle visible?"

**Ace's Tests:**
- Can a new team member understand this in 15 minutes?
- Are the errors actionable or cryptic?
- Does the API surface guide correct usage?
- How many files must you read to understand one behavior?

**The ACES Check:**
- **A**daptable — Can behavior be changed without rewriting?
- **C**omposable — Can pieces combine in new ways?
- **E**xtensible — Can new cases be added without modifying existing code?
- **S**eparable — Can components be understood in isolation?

### Burner (Structural) — Are the boundaries clean?

Not "does this follow patterns?" — but "where does logic bleed?"

**Burner's Tests:**
- Do dependencies point inward? (domain never imports infrastructure)
- Can you swap the database without touching business logic?
- Is there a clear boundary between "what" and "how"?
- Are internal data structures leaking through interfaces?

**What Burner catches:**
- Circular dependencies (A → B → A)
- Logic bleeding across layers (controller doing domain work)
- Port violations (domain importing infrastructure types)
- Coupling disguised as "convenience"

## Design Decision Routing

| Decision | Primary | Secondary | Why |
|----------|---------|-----------|-----|
| Entity naming | Karman | Ace | Domain truth + comprehension |
| API surface | Ace | Vector | DX + attack surface |
| Abstraction boundaries | Burner | Karman | Coupling + domain alignment |
| State management | Dijkstra | Lamport | Correctness + distribution |
| Auth/permissions design | Vector | Dijkstra | Security + correctness |
| Performance-sensitive paths | Knuth | Erlang | Complexity + flow |

## Review Methodology

1. **Karman first** — Does the model match reality?
2. **Burner second** — Are boundaries clean? Dependencies inverted?
3. **Ace third** — Would a new developer understand this?
4. **Route to specialists** if context triggers (auth → Vector, critical logic → Dijkstra)
5. **Synthesize** — Where do the lenses agree? Where do they conflict?

## Output Format

```
## Design Review: {Component}

### Karman (Domain Alignment)
- {Finding — does the model match reality?}

### Burner (Boundaries)
- {Finding — are boundaries clean?}

### Ace (Developer Experience)
- {Finding — is the door handle visible?}

### Specialists Invoked
- {Agent}: {finding} (if applicable)

### Conflicts
{Where lenses disagree — e.g., Karman wants richer model but Ace says it's too complex}

### Recommendations
1. {Action with perspective attribution}
```
