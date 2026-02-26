---
name: figures
description: "This skill should be used when the user asks to 'make a diagram', 'create a visualization', 'design an animation', 'choose the right diagram type', or needs visual explanations using Mermaid, D2, C4, dataviz, or cinematic animation."
version: 0.1.0
---

# Visual Communication

> Choose the right visual form for what you're explaining — static diagram, rendered chart, or cinematic animation.

## Why This Skill Exists

Two gaps, not one. First: you default to the same 3-4 Mermaid types when Mermaid has 15+ types and D2/C4 exist for when Mermaid isn't enough. Second: you reach for static diagrams when the explanation needs rendered dataviz, animation, or cinematic impact. The skill covers both — knowing which visual form serves the explanation, from text-in-markdown to scroll-driven animation.

## Tool Selection

### Static Diagrams (Documentation)

| Need | Tool | Why |
|------|------|-----|
| Quick docs, GitHub/GitLab native | **Mermaid** | Zero build, renders in markdown |
| Complex architecture (50+ nodes) | **D2** | Better layouts, requires build step |
| Formal C4 models | **C4-PlantUML** | Enterprise standard, sprites |

**Default: Mermaid** for documentation diagrams. Upgrade only when it produces poor results.

### Rendered Dataviz (Charts, Animation, Cinematic)

| Need | Tool | Why |
|------|------|-----|
| Standard charts (bar, line, area) in SvelteKit | **LayerChart** | Svelte 5 native, composable, D3-powered |
| Custom layout, force graphs, geo | **D3** (math) + **Svelte** (render) | Full control, production standard |
| Declarative grammar-of-graphics | **Observable Plot** | Concise spec, good defaults |
| Cinematic animation (particles, morphing, glow) | **Hand-rolled SVG + rAF** | Zero dependencies, full control |
| Scroll-triggered appearance | **IntersectionObserver** | Vanilla, universal |
| Scroll-scrubbed animation (pinning, parallax) | **GSAP ScrollTrigger** or **CSS animation-timeline** | Battle-tested or native |

**Upgrade from static to rendered** when: the visual needs animation, interactivity, quantitative axes, or cinematic impact that text-in-markdown can't carry.

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

## When to Upgrade from Static to Rendered

The figures skill covers a spectrum. Most documentation needs static diagrams. Some explanations need more:

| Signal | Visual form | Why upgrade |
|--------|------------|-------------|
| "This needs motion to explain" | SVG + rAF animation | Process, flow, or cycle that's invisible when frozen |
| "This needs impact" | Cinematic animation (glow, particles, morph) | Ethos pages, landing visuals, conviction writing |
| "This is quantitative data" | Rendered chart (LayerChart, D3) | Needs axes, scales, interpolation |
| "Users need to explore this" | Interactive dataviz (D3 + events) | Hover, filter, zoom, brush |
| "This should reveal as you scroll" | Scroll-driven animation | Narrative pacing, progressive disclosure |

**Key principle**: the upgrade is about information structure, not aesthetics. A feedback loop with flowing particles isn't decoration — the flow IS the explanation. Particles dimming each cycle IS the data point. Motion carries meaning that static can't.

**Accessibility requirement**: every animated visual MUST handle `prefers-reduced-motion`. When animation carries meaning, add text annotations visible in the static fallback.

## Anti-Patterns

| Don't | Why | Do instead |
|-------|-----|------------|
| Use flowchart for everything | Loses semantic information | Match diagram type to what you're explaining |
| Use `architecture-beta` in GitHub | Non-deterministic rendering, may not render | Use D2 for architecture, or `C4Context` |
| Mega-diagram with everything | Violates coherence principle | One concept per diagram |
| Skip labels on relationships | Reader can't understand connections | Always label arrows with what happens |
| Assume latest Mermaid features | GitHub runs ~10.0.2 | Test on target platform |
| Use Mermaid when you need animation | Static diagrams can't carry motion-as-meaning | Use SVG + rAF for cinematic visuals |
| Animate for decoration | Animation that doesn't carry information is chartjunk | Every motion must encode data or process |
| Skip reduced-motion handling | Excludes users, violates accessibility | Always provide static fallback with annotations |
| Use D3 for a simple bar chart | Over-engineering | Use LayerChart or even a styled HTML table |

## References

Load for details:
- `references/mermaid-types.md` — Full Mermaid catalog with syntax examples
- `references/diagram-gotchas.md` — Platform issues, debugging, validation checklist
- `references/d2.md` — D2 setup, syntax, layout engines, when to use
- `references/c4-architecture.md` — C4 levels, Mermaid vs PlantUML, decision matrix
- `references/dataviz-rendering.md` — D3, LayerChart, SVG animation, rAF patterns, scroll-driven animation, GSAP, accessibility
