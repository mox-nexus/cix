# craft-rhetoric

Understanding that propagates, not persuasion. Organized by the Five Canons of Classical Rhetoric — Invention, Arrangement, Style, Memory, Delivery — plus Dialectic.

## Orienting Principle

The test isn't "is this well-crafted?" It's **does understanding propagate?** Can the reader explain it to someone else? Does it survive forwarding?

## When to Use

- Writing docs that need to teach multiple audiences
- Content that only resonates with one type of reader
- Diagrams that need the right visual form for what they're explaining
- Restructuring documentation collections
- Designing staged reveal experiences
- Reviewing content for completeness, accuracy, and human authorship

## The Semantic Stack

Source material enters and understanding exits. Each canon transforms it:

```
Source → Discourse → Discovering → Encoding → Arranging → Voicing → Figures/Staging → Evaluating → Target
```

## Skills (Hub and Spoke)

| Skill | Canon | Version | Use When |
|-------|-------|---------|----------|
| `rhetoric` | Hub | 0.2.0 | Five canons, Three Doors, weaving, pipeline — the routing center |
| `discovering` | Inventio | 0.1.0 | Comprehension transform, four-pass reading, gap-state tracking |
| `mapping` | Cartography | 0.1.0 | Source survey, quote-anchored synthesis, map of contents |
| `arranging` | Dispositio | 0.1.0 | Collection architecture, layer model, reading paths, single source of truth |
| `voicing` | Elocutio | 0.1.0 | Anti-LLM-speak, four-pass voice review, writing craft |
| `figures` | Actio (visual) | 0.1.0 | Diagrams (Mermaid, D2, C4), dataviz (D3, LayerChart), cinematic animation |
| `staging` | Actio (experience) | 0.1.0 | Medium selection, beat structure, progressive disclosure |
| `evaluating` | Dialectic | 0.1.0 | Propagation test, structural confidence, evidence verification |

## Agents

| Agent | Canon | Function |
|-------|-------|----------|
| **magellan** | Cartography | Survey source landscape, produce map (MOC + cluster files) |
| **planner** | Planning | Break project into deliverables with agents, dependencies, sequence |
| **feynman** | Inventio | Comprehend sources, discover what to say, draft through Three Doors |
| **sagan** | Memoria | Weave content across audiences, dimensional shifts, universal thread |
| **vyasa** | Dispositio | Collection architecture — where content lives, how readers navigate |
| **orwell** | Elocutio | Voice — anti-LLM-speak, precision, rhythm, authenticity |
| **tufte** | Actio (visual) | Visual medium selection, design, build, verify |
| **jobs** | Actio (experience) | Experience design — medium selection, pacing, staged reveals |
| **socrates** | Dialectic | Content evaluation — propagation test, Three Doors traversal |

## Pipeline

```
setup → discourse → magellan (cartography) → planner (tasks)
  ─── per deliverable ───
  → feynman (inventio — discover + draft)
  → sagan (memoria — weave + stick)
  → vyasa (dispositio — arrange) — if collection
  → orwell (elocutio — voice)
  → tufte/jobs (actio) — if applicable
  → socrates (evaluate)
```

## License

MIT
