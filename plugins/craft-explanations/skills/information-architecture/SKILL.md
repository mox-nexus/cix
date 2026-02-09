---
name: information-architecture
description: "Collection-level explanation architecture. Use when: organizing multiple documents, structuring documentation sites, designing content hierarchy, ensuring single source of truth."
version: 0.1.0
---

# Information Architecture

> Where content lives matters as much as what it says. The prior question before "how do I write this?" is "where does this go?"

## Why This Skill Exists

Document-level craft (cognitive load, Diataxis, Feynman) applies to individual pages. When applied independently to a collection, you get redundancy, inconsistency, and unfindable content. Collections need their own architecture.

## Single Source of Truth

Each piece of information lives in exactly one place. Everywhere else links to it.

| Instead of | Do this |
|------------|---------|
| Explain research in every doc that needs it | Explain once in reference, link |
| Define concept wherever used | Define once, link to definition |
| Repeat tables across docs | One canonical location, reference it |

**Why**: Redundancy increases cognitive load, creates inconsistency on update, dilutes impact through repetition.

## The Layer Model

Structure collections as progressive depth:

```
Layer 1: Entry point (30 seconds) — bottom line, why it matters, where to go
    |
Layer 2: Explanation (5 minutes) — concepts, mental models, links to evidence
    |
Layer 3: Reference (verify) — full research, methodology, sources
    |
Layer 4: Bibliography (deep dive) — primary sources
```

Each layer is complete for its audience. Nobody feels they missed something — they just didn't need more depth.

| Audience | Stops at | Gets |
|----------|----------|------|
| Decision-maker | Layer 1 | The number, the risk, the action |
| Practitioner | Layer 2 | The concepts, how to apply |
| Evaluator | Layer 3 | The evidence, methodology |
| Researcher | Layer 4 | Primary sources to verify |

## Collection-Level Diataxis

| Content type | Lives in | Not in |
|--------------|----------|--------|
| "What is X?" concepts | explanation/ | reference/ (too dry for learning) |
| Step-by-step tasks | how-to/ | explanation/ (wrong mode) |
| Research findings | reference/research/ | explanation/ (just link to it) |
| Learning journeys | tutorials/ | how-to/ (different need) |
| Citations | bibliography/ | everywhere (single source) |

## Linking Patterns

| Situation | Inline | Link |
|-----------|--------|------|
| Core to understanding this doc | Inline | |
| Supporting evidence | | Link |
| Tangential but interesting | | Link |
| Reader needs it to continue | Inline | |
| Appears in multiple docs | | Link (to single source) |

Information flows downward. Links point to deeper layers. A reader starts at entry and follows links to the depth they need.

## Organizational Patterns

| Pattern | Best for | Fails when |
|---------|----------|------------|
| By task (Diataxis) | Documentation | Users don't know the task name |
| By topic | Known subject areas | Users don't know the right word |
| By audience | Distinct audiences | Someone is multiple roles |
| Hybrid | Most real collections | Over-engineering the taxonomy |

**Default: Task-based (Diataxis) at top level, topic-based within sections.**

## Diagnosing Problems

| Symptom | Root cause | Fix |
|---------|------------|-----|
| Same info in multiple docs | Document-scoped thinking | Consolidate to single source, link |
| Readers say "I read this already" | Redundancy | Single source of truth |
| Hard to find things | Structure doesn't match mental model | Re-organize by user intent |
| Updates missed in some places | Multiple copies | Single source |
| Deep nesting nobody navigates | Over-classification | Flatten. Fewer categories, more cross-links |

## References

Load for details:
- `references/collection-architecture.md` — Layer model, linking flow, audit process
- `references/information-architecture.md` — Mental models, navigation patterns, organizational patterns
- `references/reading-patterns.md` — F-pattern, scanning behavior, entry points
