---
name: eliciting
description: "This skill should be used when the user asks to 'scope a research project', 'define research questions', 'figure out what to research', 'identify sources', or needs to articulate research intent before the pipeline begins."
version: 0.1.0
---

# Eliciting

> The agent asks. The human generates. The human's generation IS the scope.

Research is thinking — not retrieval of pre-formed questions. When someone says "I want to research X" and can't specify what about X, the discourse surfaces a thinking gap. Eliciting applies this: the human is scoping when they're talking to the agent. The agent won't let hand-waving happen.

Eliciting is step 0 — the first move in every research workflow. Without it, the orchestrator writes `scope.md` from a one-line request, producing a plausible but ungrounded scope. That's the research equivalent of "the generated" — scope that looks right but wasn't thought through.

## Contents

- [Why Eliciting Comes First](#why-eliciting-comes-first)
- [The Three Movements](#the-three-movements)
- [Deepening Questions](#deepening-questions)
- [Source Identification](#source-identification)
- [Eliciting Is Complete When](#eliciting-is-complete-when)

## Why Eliciting Comes First

When the orchestrator generates scope and the human approves, the human is verifying — not thinking. When the agent asks and the human generates, the human activates their own understanding of what they need to learn. The scope emerges from the human's generation, not from their approval of an AI-generated scope.

The human has the domain knowledge. Eliciting finds the sharp questions in it — pushes until the research questions are specific, answerable, and bounded. The rest of the pipeline is methodology infrastructure. The human never needed to learn the methodology. They needed a collaborator who could force clarity on the inquiry and then handle the extraction, verification, and synthesis.

## The Three Movements

Three movements draw out everything downstream agents need.

**Movement 1 — Inquire**: What are you trying to learn?

Ask: *What is the question? What gap does it address? Why does it matter to you?*

The human articulates purpose and research intent. Not paper titles, not methodology — the inquiry itself. Listen for what they say unprompted. That's where the weight is.

**Movement 2 — Bound**: What's the context?

Ask: *What's in scope? What's out? How deep? What will you do with the findings?*

The human names boundaries, depth, constraints, and intended use. A systematic review has different bounds than a quick literature check. Understanding the container early prevents scope creep downstream.

**Movement 3 — Source**: What do you already know, and where might you look?

This movement adapts to the human's knowledge state:

| Knowledge state | Draw out |
|----------------|----------|
| Expert entering new sub-area | What they know from adjacent work, where this area differs |
| Practitioner with scattered reading | What papers they remember, what they took from each, what's hearsay |
| Beginner with a question | Why this question matters to them, what they've heard, where they'd start |

The agent does not suggest sources. The agent asks, clarifies, deepens — but the source landscape originates with the human.

## Deepening Questions

Within each movement, use Paul-Elder categories to deepen:

| Category | Purpose | Example |
|----------|---------|---------|
| **Clarification** | Surface what they mean | "What do you mean by 'cognitive offloading'?" |
| **Assumptions** | Expose what must hold | "What has to be true for that question to be answerable?" |
| **Evidence** | Ground in measurement | "What kind of evidence would answer that?" |
| **Viewpoints** | Test from other angles | "How would a skeptic frame this differently?" |
| **Implications** | Follow the thread | "If you found X, what would that change?" |
| **Meta** | Check the framing | "Why this question and not the adjacent one?" |

Don't run through all categories mechanically. Follow the human's energy.

## Source Identification

During Movement 3, co-create `sources/inventory.md`:

| Field | What to capture |
|-------|----------------|
| **Known sources** | Papers the human has read, with their take |
| **Potential sources** | Papers they've heard of, databases to search |
| **Source hierarchy** | Where to look first, second, third |
| **Excluded sources** | What to never cite and why |
| **Tier pre-classification** | Human's initial estimate (1-Gold, 2-Silver, 3-Bronze) |

This shifts source identification from "orchestrator guesses" to "human articulates with agent support."

## Eliciting Is Complete When

The agent can state back — in its own words, not the human's phrasing — the research questions, boundaries, source landscape, and success criteria. The human confirms or corrects. Iterate until confirmed.

**Output**: Two files written to the workspace:

| File | Contents |
|------|----------|
| `scope.md` | Research questions, boundaries, source hierarchy, success criteria. Immutable after discourse. |
| `sources/inventory.md` | Source list with metadata, tiers, known vs potential. |

These are the co-created input documents for the entire pipeline. Every downstream agent reads `scope.md`.

## What Eliciting Does Not Do

- Comprehend source material — that's extract (extracting skill)
- Search for papers — it identifies what sources exist, it doesn't retrieve them
- Suggest research questions — the agent asks, the human generates
- Verify claims — that's scrutiny (verifying skill)
- Write content downstream

## References

Load for detail:
- [discourse-protocol](references/discourse-protocol.md) — Three movements in detail, worked examples, failure modes
