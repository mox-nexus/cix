# Craft Explanations: Design Methodology

This document explains WHY the craft-explanations plugin is designed the way it is.

## The Core Insight: The Three Doors

Explanations aren't sequential layers (principle → pattern → practice). They're fabric with three simultaneous dimensions — a coordinate system, not a ladder.

Three dimensions of perception, not a hierarchy:

- **Coherence** — the unifying principle, why this holds together
- **Contrast** — the alternatives weighed, why this and not that
- **Ground** — the weight that doesn't argue for itself, what is right now

### The Facet-Set Model

Each door isn't a single concept. It's a facet set — the same dimension viewed from different domains:

| Door | Explanation | Engineering | Philosophy |
|------|-------------|-------------|------------|
| **1** | Principle | Abstraction | Universal |
| **2** | Concretions | Planning | Constituency |
| **3** | Ground | Execution | Self |

The vertical alignment is the same dimension through different lenses. The horizontal flow narrows: Universal → Constituency → Self.

- Door 1 is true everywhere, no context needed
- Door 2 is true for these people, in this situation — it requires knowing who's in the room
- Door 3 is true for me, right now, in my hands — it requires the body

**Constituency is the bridge.** The abstract becomes concrete *for someone*. Skip Door 2 and Door 3 becomes generic steps. You can't jump from Universal to Self without passing through Constituency.

### Evolution from v0.1

The original skill used Principle / Pattern / Practice as the three labels. This was replaced in v0.2 because:

- **"Pattern"** was the weakest name. It doesn't communicate that Door 2 is about *who this is for* — the constituency, the concretion for a specific audience. "Pattern" sounds like taxonomy. "Concretions" says the universal truth has been shaped for someone particular.
- **"Practice"** was too generic. "Just add a practical example" can still be abstract — a hypothetical scenario, a generic code sample. That's Door 1 wearing Door 3's clothes. "Ground" conveys weight, embodiment, the thing that doesn't argue for itself because it doesn't need to.
- **The facet sets** reveal that the three doors aren't explanation-specific. They map onto engineering (Abstraction → Planning → Execution), philosophy (Universal → Constituency → Self), and architecture (Domain model → Application layer → Infrastructure). The framework is a coordinate system that applies across domains.

## Why Directional Modal Lock

v0.1 diagnosed modal lock as "you're stuck in one dimension, shift to another." v0.2 adds directionality: shifts go through the next door (1→2→3), not a skip.

This matters because:
- Jumping from Door 1 (beautiful framework) directly to Door 3 (steps) without Door 2 (who is this for?) produces generic instructions that look practical but aren't grounded in anyone's reality
- Door 2 is the bridge that gets skipped most often — especially by Claude, whose default lock is Abstraction | Universal
- The directional diagnosis tells you *which* shift to make, not just that one is needed

## Why Dimensional Shift

The most powerful learning moments happen at intersections between doors — when understanding crosses from one dimension to another. "I understood it, then suddenly I *felt* it" (Door 1 → Door 3). "I iterated, then it settled into my hands" (Door 2 → Door 3).

This goes beyond "all three doors should be present" to: **design the transitions between them**. The moment of crossing is where information becomes knowledge.

## Why "Wider, Not Louder"

When explanation fails, the instinct is to amplify: more docs, more slides, more energy. This deepens modal lock.

The reframe: explanation failure is dimensional compression across instrumental boundaries. Each receiver — each organizational layer — compresses through whatever dimensions it can perceive. The fix isn't louder signal. It's wider encoding — all three doors woven so that enough survives in whatever dimension the receiver can pass.

This connects to the interpretability insight: the meeting problem (human → human) and the interpretability problem (model → human) may be the same dimensional compression problem viewed from opposite directions.

## Why Four Agents with Different Entry Doors

Initial design mapped agents 1:1 to dimensions. This was rejected because it decomposes simultaneous encoding back into sequential traversal.

Instead, each agent enters through a different door but carries ALL three:

- **Feynman** enters through Door 3 (Ground · Execution · Self) — example-first, surfaces why it works
- **Sagan** enters through Door 1 (Principle · Abstraction · Universal) — wonder-first, grounds in the tangible
- **Tufte** enters through Door 2 (Concretions · Planning · Constituency) — who needs to see this, what makes it concrete for them
- **Socrates** is meta — forces traversal across all doors and checks for dimensional shift

The Tufte reframe was the most significant: from "pattern/visual structure" to "constituency/concretion." This changes the agent's first question from "what's the right diagram type?" to "who needs to see this?"

## Why "Modal Lock" Is the Key Anti-Pattern

Modal lock is Claude's specific failure mode: defaulting to Door 1 (clean taxonomies, headers, structure) and amplifying when it doesn't land.

With the facet-set model, the diagnosis is more precise:
- What's over-represented: Abstraction | Universal
- What's missing: Constituency — the question "who is standing at this door?"
- What looks like a fix but isn't: generic examples (Door 1 in Door 3's clothes)

## The Missing Ground

Professional communication is almost entirely Door 1 + Door 2: docs, diagrams, logic, demos, energy. Door 3 — weight, inevitability, ground — is nearly absent from professional contexts.

The closest analog: showing the thing already working. Not a prototype. The thing itself. This is an open question in the framework — ground-level transmission may require a fundamentally different instrument than the deck or the document.

## Research Base

Key findings informing the design:

| Finding | Source | Design Implication |
|---------|--------|-------------------|
| Coherence principle d=0.86 | Mayer, 23/23 tests | Cut extraneous material ruthlessly |
| Expertise reversal d=0.505/-0.428 | Tetzlaff 2025, n=5,924 | Detect expertise, adapt guidance level |
| WHY framing 31.5% -> 97.3% | Prompting Inversion, arXiv | Route and explain why, don't prescribe how |
| CoVe +23% accuracy | Dhuliawala et al. 2024 | Independent verification prevents hallucination |
| Feynman Bot 1.8x learning | Demszky et al. 2025 | Example-first teaching works |
| Contrastive explanations | Miller 2019 | "Why X, not Y?" is more effective than "Why X?" |

## Sources

- Bastani et al. (2025). Generative AI without guardrails can harm learning. PNAS.
- Dhuliawala et al. (2024). Chain-of-Verification Reduces Hallucination. ACL.
- Miller, T. (2019). Explanation in Artificial Intelligence: Insights from the Social Sciences. AI Journal.
- Tetzlaff et al. (2025). Expertise Reversal Effect meta-analysis. n=5,924.
- arXiv:2510.22251. Prompting Inversion for frontier models.
- Mayer, R. (2009). Multimedia Learning. Cambridge University Press.
- Nielsen Norman Group. F-pattern, scanning, information architecture research.
- "The Three Doors: A Framework for Resonant Transmission" — origin essay for the facet-set model.
