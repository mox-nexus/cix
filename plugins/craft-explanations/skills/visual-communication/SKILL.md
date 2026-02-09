---
name: visual-communication
description: "Diagram type selection and visual explanation. Use when: choosing diagram types, creating Mermaid/D2/C4 diagrams, explaining with visuals, debugging diagram rendering issues."
version: 0.1.0
---

# Visual Communication

> Choose the right diagram type for what you're explaining, not what's familiar.

## Why This Skill Exists

You default to the same 3-4 Mermaid types (flowchart, sequence, class). Mermaid has 15+ types. D2 and C4 exist for when Mermaid isn't enough. The gap isn't "how to write Mermaid" — it's knowing which type serves the explanation.

## Tool Selection

| Need | Tool | Why |
|------|------|-----|
| Quick docs, GitHub/GitLab native | **Mermaid** | Zero build, renders in markdown |
| Complex architecture (50+ nodes) | **D2** | Better layouts, requires build step |
| Formal C4 models | **C4-PlantUML** | Enterprise standard, sprites |

**Default: Mermaid** for 95% of cases. Upgrade only when it produces poor results.

## Diagram Type Routing

Match what you're explaining to the right diagram type:

| You're explaining... | Use | Not |
|----------------------|-----|-----|
| API call flow, message sequence | `sequenceDiagram` | flowchart (loses time ordering) |
| Process flow, decision trees | `flowchart TD/LR` | sequence (loses branching) |
| State machine, entity lifecycle | `stateDiagram-v2` | flowchart (loses state semantics) |
| Database schema, relationships | `erDiagram` | class (loses cardinality) |
| Class hierarchy, interfaces | `classDiagram` | er (loses method/property detail) |
| Project timeline, roadmap | `gantt` | flowchart (loses time axis) |
| Proportional data | `pie` | table (loses visual proportion) |
| User experience flow | `journey` | flowchart (loses satisfaction scores) |
| Git workflow | `gitGraph` | flowchart (loses branch semantics) |
| Chronological events | `timeline` | gantt (loses simplicity) |
| Concept hierarchy, brainstorm | `mindmap` | flowchart (loses radial organization) |
| 2D prioritization | `quadrantChart` | table (loses spatial positioning) |
| Flow volume, traffic sources | `sankey-beta` | flowchart (loses proportional width) |
| Service architecture | D2 or `architecture-beta` | flowchart (loses service semantics) |
| System boundary, users | `C4Context` | flowchart (loses C4 semantics) |
| Tech stack, containers | `C4Container` | class (loses deployment context) |

## Platform Reality

| Platform | Core types | Recent additions |
|----------|------------|------------------|
| GitHub | ~10.0.2 — all core types work | timeline, mindmap, architecture-beta: **may not render** |
| GitLab | 10.6.0 — most work | Some newer types available |
| Mermaid official | 11.x+ | All types available |

**Rule: Test on target platform before committing.**

## When to Upgrade from Mermaid

Upgrade to **D2** when ALL true:
- 50+ nodes or complex nesting
- Mermaid auto-layout produces spaghetti
- Build step acceptable
- Native GitHub rendering not required

Upgrade to **C4-PlantUML** when:
- Formal C4 compliance required
- Enterprise architecture documentation
- Need sprites/standardized icons

## Anti-Patterns

| Don't | Why | Do instead |
|-------|-----|------------|
| Use flowchart for everything | Loses semantic information | Match diagram type to what you're explaining |
| Use `architecture-beta` in GitHub | Non-deterministic rendering, may not render | Use D2 for architecture, or `C4Context` |
| Mega-diagram with everything | Violates coherence principle | One concept per diagram |
| Skip labels on relationships | Reader can't understand connections | Always label arrows with what happens |
| Assume latest Mermaid features | GitHub runs ~10.0.2 | Test on target platform |

## References

Load for details:
- `references/mermaid-types.md` — Full Mermaid catalog with syntax examples
- `references/diagram-gotchas.md` — Platform issues, debugging, validation checklist
- `references/d2.md` — D2 setup, syntax, layout engines, when to use
- `references/c4-architecture.md` — C4 levels, Mermaid vs PlantUML, decision matrix
