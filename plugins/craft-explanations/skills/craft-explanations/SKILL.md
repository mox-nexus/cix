---
name: craft-explanations
description: "Explanation craft through simultaneous encoding. Use when: writing docs, explaining concepts, teaching in conversation, creating tutorials, curating collections, making diagrams for explanation."
version: 0.2.0
---

# Craft Explanations

> Every explanation simultaneously carries principle, concretion, and ground. The receiver pulls what they need.

## The Three Doors

Explanations aren't layers to traverse top-down. They're fabric with three simultaneous dimensions — coordinate axes, not a ladder.

| Door | Explanation | Engineering | Philosophy | The receiver asks |
|------|-------------|-------------|------------|-------------------|
| **1** | Principle | Abstraction | Universal | "Why does this hold together?" |
| **2** | Concretions | Planning | Constituency | "Who is this for, and why this, not that?" |
| **3** | Ground | Execution | Self | "What do I carry away?" |

All three are present in every good explanation. The difference is which door the receiver enters through.

The doors narrow: **Universal → Constituency → Self.** Door 1 is true everywhere. Door 2 is true for these people, in this situation. Door 3 is true for me, right now, in my hands. Constituency is the bridge — the universal becomes concrete *for someone*. Skip it and Door 3 is just generic steps anyone could follow and no one does.

## Modal Lock

Your default failure mode. You default to Door 1 — Abstraction | Universal. Clean taxonomies, complete frameworks, universal truths beautifully organized. When it doesn't land, you amplify: more structure, more categories, more abstraction. The explanation gets taller without getting wider.

What's missing isn't "practice" generically. It's **Constituency** — Door 2. The question you almost never ask: *who is standing at this door right now, and what do they specifically need?*

### Directional Diagnosis

Modal lock shifts through the next door, not a skip. 1→2→3. The bridge isn't optional.

| Lock | Symptom | What's missing | Shift to |
|------|---------|----------------|----------|
| Stuck in Door 1 | Beautiful framework, nobody moves | Who is this *for*? | Door 2: concretize for a constituency |
| Stuck in Door 2 | Endless options, trade-offs, analysis | What do *I* do right now? | Door 3: enable self-execution |
| Stuck in Door 3 | Shipped but nobody knows why | Why does this *matter*? | Door 1: connect to the universal |

### Signal Table

| Signal | Missing door | Shift to |
|--------|-------------|----------|
| "I don't get why this matters" | Door 1 | Connect to something they care about |
| "Who is this for?" | Door 2 | Concretize for a specific audience |
| "How does this fit with X?" | Door 2 | Show the relationship to what they know |
| "What do I actually do?" | Door 3 | Ground in what they carry away |
| "This is too abstract" | Door 3 | Start with the specific, derive the general |
| "This is just steps, I don't understand" | Door 1 | Explain WHY these steps, not others |

## Wider, Not Louder

When explanation fails, the instinct is more of the same — more docs, more slides, more energy. This deepens the lock.

The fix: **encode all three doors simultaneously** so the signal survives lossy compression. Each receiver — each organizational layer — compresses through whatever dimensions it can perceive. If you encode wide, enough survives in whatever door the receiver can pass.

**Weave, don't sequence.** "A why section, then a how section, then a what section" is three one-dimensional presentations in a trench coat. Every passage should carry all three threads. The reader pulls theirs.

If a door is missing, don't add a section. Shift the weave of what's already there.

## Dimensional Shift

The most powerful explanation moments happen at intersections between doors — not within one.

| Shift | Experience | Design move |
|-------|-----------|-------------|
| Door 1 → Door 3 | "I understood it, then suddenly I *felt* it" | Principle becomes embodied |
| Door 2 → Door 3 | "I iterated, then it settled into my hands" | Contrast becomes ground |
| Door 3 → Door 2 | "It was automatic, then I had to choose again" | Ground becomes deliberate |

Design for dimensional shift, not dimensional purity. The moment an idea crosses from one door to another is when it stops being information and starts being knowledge.

## Instrumental Boundaries

When you explain something, you're doing interpretability work — making internal representations cross a boundary between instruments. "This isn't landing" doesn't mean "I need better words." It means the channel can't carry all the dimensions.

Build explanations that survive the crossing. Encode wide enough that dimensional compression at the boundary doesn't strip what matters.

## The Missing Ground

Professional communication is almost entirely Door 1 + Door 2: docs, diagrams, logic, demos, energy. Door 3 — weight, inevitability, ground — remains elusive.

The closest analog: show the thing already working. Not a prototype. Not a mockup. The thing itself, undeniable. A deck explains and contrasts. It doesn't *weigh*.

When you can: ground in the real artifact. When you can't: use language that carries weight — specific numbers, direct statements, things that don't argue for themselves because they don't need to.

## Explanation Routing

Match the situation to the technique:

| Situation | Enter through | Technique | Key move |
|-----------|---------------|-----------|----------|
| Someone asks "what is X?" | Door 3 then Door 2 | Feynman | Example first, then model |
| Writing a tutorial | Door 3 then Door 1 | Cognitive load sequencing | Do, then understand why |
| Writing reference docs | Door 2 | Structured lookup | Complete, scannable, no narrative |
| Explaining a decision | Door 1 then Door 2 | BLUF + evidence chain | Why, then framework, then specifics |
| Teaching a concept | Door 1 then Door 3 | Contrastive explanation | Why X, not Y? (Miller) |
| Code review explanation | Door 3 then Door 1 | Show impact | "This causes X because Y" |
| README / overview | All three, woven | Progressive disclosure | 30s, 5min, verify |

## Audience Calibration

Don't guess — detect:

| Signal | Expertise | Adjust |
|--------|-----------|--------|
| Uses jargon correctly | Competent+ | Skip scaffolding |
| Asks foundational questions | Novice | More Door 3, less Door 2 |
| Points out edge cases | Expert | Engage Door 1, skip basics |
| "Just tell me what to do" | Any (task-focused) | Lead with Door 3 |
| "Why?" | Any (understanding-focused) | Lead with Door 1 |

**Expertise reversal** (Tetzlaff 2025, n=5,924): What helps novices actively harms experts. High guidance for novices (d=0.505). Low guidance for experts (d=-0.428). Detect and adapt.

## Document Types

When structuring written explanations, use Diataxis:

| Reader says | Write a | Door emphasis |
|-------------|---------|---------------|
| "Teach me X" | Tutorial | Door 3 heavy, Door 1 emerges |
| "How do I do X?" | How-to | Door 3 only, assume understanding |
| "Why does X work?" | Explanation | Door 1 through Door 2 |
| "What exactly is X?" | Reference | Door 2 (structured lookup) |

Don't mix types in one document.

## Writing Craft

**Coherence principle** (d=0.86, 23/23 tests): Extraneous material must be excluded. If it doesn't serve the encoding, cut it.

**Scanning patterns**: People read in F-pattern. Front-load keywords in headings. Headers as signposts. Bullets and bold for scannability.

**AI tell-tale audit**: Avoid — delve, leverage, utilize, robust, tapestry. Uniform paragraph lengths. Rule-of-three in every list. Excessive bold. Generic openings.

See: `references/anti-patterns.md`

## Accuracy

Teaching wrong things effectively is worse than not teaching at all. Verification precedes craft.

- State what was measured, not what you infer
- Label evidence levels: Strong / Moderate / Weak / Speculative
- Separate findings from interpretation
- Acknowledge contradictory evidence

See: `references/accuracy-integrity.md`

## Anti-Patterns

| Anti-pattern | What's happening | Fix |
|--------------|------------------|-----|
| **Modal lock** | Amplifying same door when it doesn't land | Shift to next door (1→2→3) |
| **Skipping Door 2** | Jumping from universal to execution | Concretize for a constituency first |
| **Sequential traversal** | "First principle, then pattern, then steps" | Weave simultaneously |
| **Adding instead of shifting** | Bolting on "practical examples" after theory | Re-encode the theory through Door 3 |
| **Door 1 in costume** | Generic example pretending to be Door 3 | Real constituency, real context, real weight |
| **Confidence theater** | Projecting certainty without evidence | State evidence level explicitly |
| **Explanation inflation** | More words when fewer would serve | Cut. Then cut more. |

## Before Shipping

1. Does this trust the learner?
2. Will they discover something themselves?
3. Can the ground-seeker find their door at every point?
4. Can the constituency-seeker feel the contrast in the reasoning?
5. Can the principle-seeker pull their thread from any passage?
6. Is the weave woven, not sequenced?
7. Does a dimensional shift happen — does the explanation cross doors?
8. Have I trusted what I cannot see?

## Agents

| Agent | Enters through | Best for |
|-------|----------------|----------|
| `feynman` | Door 3 (Ground · Execution · Self) | Docs, tutorials, teaching |
| `sagan` | Door 1 (Principle · Abstraction · Universal) | Concept overviews, vision docs |
| `tufte` | Door 2 (Concretions · Planning · Constituency) | Data explanation, diagram decisions |
| `socrates` | Forces traversal across all doors | Review, deepening understanding |

## References

Load for details:
- `references/anti-patterns.md` — Modal lock, AI writing tells, explanation inflation
- `references/accuracy-integrity.md` — Why accuracy precedes technique

See also:
- `weaving` skill — Re-weave modal-locked content across doors (diagnose → anchor → thread → shift → verify)
- `visual-communication` skill — Diagram type routing, Mermaid/D2/C4
- `information-architecture` skill — Collection-level encoding, where content lives
