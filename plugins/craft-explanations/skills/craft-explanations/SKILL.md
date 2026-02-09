---
name: craft-explanations
description: "Explanation craft through simultaneous encoding. Use when: writing docs, explaining concepts, teaching in conversation, creating tutorials, curating collections, making diagrams for explanation."
version: 0.1.0
---

# Craft Explanations

> Every explanation simultaneously carries principle, pattern, and practice. The receiver pulls what they need.

## The Core Insight

Explanations aren't layers to traverse top-down. They're fabric with three simultaneous dimensions:

| Dimension | What it encodes | Receiver asks |
|-----------|----------------|---------------|
| **Principle** | Why this matters, abstraction, impact over time | "What's the deeper truth?" |
| **Pattern** | How things connect, categories, relationships | "How does this relate to what I know?" |
| **Practice** | What to do now, concrete steps, implementation | "What do I actually do?" |

All three are present in every good explanation. The difference is which door the receiver enters through.

## Why This Matters

Your default failure mode: **modal lock**.

You default to principle + pattern (clean taxonomies, headers, bullet structures). When it doesn't land, you amplify the same mode — more structure, more categories, more abstraction.

The fix: **shift, don't add**. When a dimension is missing, re-encode what's already there. Don't bolt on a new section.

| Signal | Missing dimension | Shift to |
|--------|-------------------|----------|
| "I don't get why this matters" | Principle | Connect to something they care about |
| "How does this fit with X?" | Pattern | Show the relationship to what they know |
| "What do I actually do?" | Practice | Ground in a concrete example |
| "This is too abstract" | Practice | Start with the specific, derive the general |
| "This is just steps, I don't understand" | Principle | Explain WHY these steps, not others |

## Explanation Routing

Match the situation to the technique:

| Situation | Enter through | Technique | Key move |
|-----------|---------------|-----------|----------|
| Someone asks "what is X?" | Practice then Pattern | Feynman | Example first, then model |
| Writing a tutorial | Practice then Principle | Cognitive load sequencing | Do, then understand why |
| Writing reference docs | Pattern | Structured lookup | Complete, scannable, no narrative |
| Explaining a decision | Principle then Pattern | BLUF + evidence chain | Why, then framework, then specifics |
| Teaching a concept | Principle then Practice | Contrastive explanation | Why X, not Y? (Miller) |
| Code review explanation | Practice then Principle | Show impact | "This causes X because Y" |
| README / overview | All three, balanced | Progressive disclosure | 30s, 5min, verify |

## Audience Calibration

Don't guess — detect:

| Signal | Expertise | Adjust |
|--------|-----------|--------|
| Uses jargon correctly | Competent+ | Skip scaffolding |
| Asks foundational questions | Novice | More practice, less pattern |
| Points out edge cases | Expert | Engage principle, skip basics |
| "Just tell me what to do" | Any (task-focused) | Lead with practice |
| "Why?" | Any (understanding-focused) | Lead with principle |

**Expertise reversal** (Tetzlaff 2025, n=5,924): What helps novices actively harms experts. High guidance for novices (d=0.505). Low guidance for experts (d=-0.428). Detect and adapt.

## Document Types

When structuring written explanations, use Diataxis:

| Reader says | Write a | Encoding emphasis |
|-------------|---------|-------------------|
| "Teach me X" | Tutorial | Practice-heavy, principle emerges |
| "How do I do X?" | How-to | Practice-only, assume understanding |
| "Why does X work?" | Explanation | Principle through pattern |
| "What exactly is X?" | Reference | Pattern (structured lookup) |

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
| **Modal lock** | Amplifying same dimension when it doesn't land | Shift to missing dimension |
| **Sequential traversal** | "First principle, then pattern, then steps" | Encode simultaneously |
| **Adding instead of shifting** | Bolting on "practical examples" after theory | Re-encode the theory through examples |
| **Confidence theater** | Projecting certainty without evidence | State evidence level explicitly |
| **Explanation inflation** | More words when fewer would serve | Cut. Then cut more. |

## Agents

| Agent | Enters through | Best for |
|-------|----------------|----------|
| `feynman` | Practice (concrete, example-first) | Docs, tutorials, teaching |
| `sagan` | Principle (wonder, abstraction) | Concept overviews, vision docs |
| `tufte` | Pattern (visual, relational) | Data explanation, diagram decisions |
| `socrates` | Dialectical (forces traversal) | Review, deepening understanding |

## References

Load for details:
- `references/anti-patterns.md` — Modal lock, AI writing tells, explanation inflation
- `references/accuracy-integrity.md` — Why accuracy precedes technique

See also:
- `visual-communication` skill — Diagram type routing, Mermaid/D2/C4
- `information-architecture` skill — Collection-level encoding, where content lives
