# craft-explanations

Explanation craft through simultaneous encoding. Part of the [cix](../../) marketplace.

## What This Plugin Does

Helps Claude write explanations that carry principle, pattern, and practice simultaneously — so the receiver pulls what they need rather than being forced through a prescribed sequence.

## Skills

| Skill | Purpose |
|-------|---------|
| **craft-explanations** | Core encoding principle, audience calibration, explanation routing |
| **visual-communication** | Diagram type selection (Mermaid, D2, C4), visual explanation design |
| **information-architecture** | Collection-level structure, single source of truth, layer model |

## Agents

| Agent | Entry Door | Best For |
|-------|-----------|----------|
| **feynman** | Practice (concrete, example-first) | Docs, tutorials, teaching |
| **sagan** | Principle (wonder, abstraction) | Vision docs, concept overviews |
| **tufte** | Pattern (visual, relational) | Diagram decisions, data explanation |
| **socrates** | Dialectical (forces traversal) | Reviewing explanations, deepening understanding |

## Design Philosophy

See `docs/explanation/methodology.md` for the full rationale. Key points:

- **Simultaneous encoding** over sequential disclosure
- **Route, don't teach** — Claude already knows CLT, Diataxis, Feynman
- **Shift, don't add** — when an explanation dimension is missing, re-encode rather than bolt on
- **Modal lock** awareness — Claude's default failure mode is more structure when grounding is needed
