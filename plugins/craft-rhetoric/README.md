# craft-rhetoric

Understanding that propagates, not persuasion. A compiler pipeline for meaning — organized by the Five Canons of Classical Rhetoric plus Discourse and Critique.

## The Thesis

Impact shouldn't be gated behind skills that aren't the point. The person who has a breakthrough insight shouldn't need a literature degree to get that insight into the world. The insight is the spark. Writing craft is the delivery vehicle.

Discourse finds the spark — pushes until the thinking is sharp. The rest of the pipeline is delivery infrastructure. The human does the hard part (thinking clearly about their domain). The AI does the skilled part (writing craft, structure, visual design). Both are necessary. Neither replaces the other.

## When to Use

- Writing docs that need to teach multiple audiences
- Content that only resonates with one type of reader
- Diagrams that need the right visual form for what they're explaining
- Restructuring documentation collections
- Designing staged reveal experiences
- Reviewing content for completeness, accuracy, and human authorship

## The Pipeline

An evaluator-optimizer loop. Multiple optimizers transform content. Orwell gates voice after every prose step. Ebert makes the final ship/return call.

```
socrates (discourse) → ground-truth.md + voice.md
  → magellan (cartography) → map/
  ─── per deliverable ───
  → feynman (inventio) → orwell (voice check)
  → sagan (memoria) → orwell (voice check)
  → vyasa (dispositio)
  → tufte (figures) / jobs (staging) → orwell (voice check after jobs)
  → ebert (critique — ship or return)
```

## Skills

| Skill | Canon | Version | Use When |
|-------|-------|---------|----------|
| `rhetoric` | Hub | 0.3.0 | Five canons, Three Doors, weaving, pipeline — the routing center |
| `discourse` | Skill 0 | 0.1.0 | Draw out human ground truth, co-create voice anchor |
| `discovering` | Inventio | 0.2.0 | Comprehension transform, four-pass reading, gap-state tracking |
| `mapping` | Cartography | 0.1.0 | Source survey, quote-anchored synthesis, map of contents |
| `arranging` | Dispositio | 0.1.0 | Collection architecture, layer model, reading paths, single source of truth |
| `voicing` | Elocutio | 0.3.0 | Voice preservation, anti-LLM-speak, voice drift detection, regression testing |
| `figures` | Actio (visual) | 0.1.0 | Diagrams (Mermaid, D2, C4), dataviz (D3, LayerChart), cinematic animation |
| `staging` | Actio (experience) | 0.1.0 | Medium selection, beat structure, progressive disclosure |
| `evaluating` | Critique | 0.1.0 | Propagation test, structural confidence, evidence verification |

## Agents

| Agent | Role | Posture |
|-------|------|---------|
| **socrates** | Discourse — draw out ground truth | Generous: deepening, not judging |
| **magellan** | Cartography — survey source landscape | Scoped by ground truth |
| **feynman** | Inventio — comprehend sources, draft content | Comprehend before producing |
| **sagan** | Memoria — weave, make understanding stick | Additive threading, never weakening |
| **vyasa** | Dispositio — arrange collection | Structure, not prose |
| **orwell** | Elocutio — voice preservation (after every prose step) | Preservation by default |
| **tufte** | Actio — visual artifacts | Information structure drives form |
| **jobs** | Actio — experience design | Medium selection, pacing |
| **ebert** | Critique — ship or return | "Does it work?" not "I'd do it differently" |

## Core Constraint: Voice Preservation

A multi-agent pipeline will destroy the original voice through cumulative drift unless voice preservation is architecturally enforced. Orwell runs after every prose-transforming step — not as a late-stage filter but as a continuous guardian. Every agent in the pipeline preserves voice by default. Changes require justification against the agent's specific scope.

See `docs/explanation/voice-preservation.md` for the research and design reasoning.

## Design Documentation

- `docs/explanation/methodology.md` — Why the Three Doors, modal lock, dimensional shift
- `docs/explanation/voice-preservation.md` — Why voice is a first-class constraint, the research behind it
- `docs/explanation/sources.md` — Full bibliography

## License

MIT
