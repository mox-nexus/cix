---
name: discourse
description: "This skill should be used when the user asks to 'start a content project', 'figure out what I want to say', 'establish ground truth', 'create a voice anchor', or needs to articulate claims before writing begins."
version: 0.1.0
---

# Discourse

> The agent asks. The human generates. The human's generation IS the ground truth.

Writing is thinking — not documentation of thinking. When someone writes "this experiment tests whether..." and can't finish the sentence, the writing surfaced a thinking gap. Discourse applies this: the human is writing when they're talking to the agent. The agent won't let hand-waving happen.

Discourse is skill 0 — the first move in every workflow. Without it, agents pattern-match source material and produce plausible content that was never grounded in human understanding. That's the generated. Discourse prevents it.

## Contents

- [Why Discourse Comes First](#why-discourse-comes-first)
- [The Three Movements](#the-three-movements)
- [Deepening Questions](#deepening-questions)
- [Voice Anchor](#voice-anchor)
- [Discourse Is Complete When](#discourse-is-complete-when)

## Why Discourse Comes First

When the agent generates and the human evaluates, the human is verifying — not thinking. When the agent asks and the human generates, the human activates their own understanding. The ground truth emerges from the human's generation, not from their approval of the agent's generation.

The human has the spark. Discourse finds it — pushes until the thinking is sharp. The rest of the pipeline is delivery infrastructure. The human never needed to learn the delivery. They needed a collaborator who could force clarity on the thinking and then handle the craft.

## The Three Movements

Three movements draw out everything downstream agents need.

**Movement 1 — Communicate**: What are you trying to communicate?

Ask: *What is this about? What's the core thing? Why does it matter?*

The human articulates purpose and thesis. Not features, not structure — the thing itself. Listen for what they say unprompted. That's where the weight is.

**Movement 2 — Setup**: What's the context?

Ask: *Who is this for? Where does it live? What medium? What constraints?*

The human names audience, presentation context, and boundaries. A library article has different setup than an experience page or a one-time presentation. Understanding the container early informs every downstream decision.

**Movement 3 — Substance**: What do you know about it?

This movement adapts to the project type. The agent follows the human's energy:

| Project type | Draw out |
|-------------|----------|
| Research synthesis | Claims with evidence levels, what studies establish, where evidence conflicts, tensions, bets |
| Experience page | Story arc, emotional journey, what the reader should feel, key moments |
| Project docs | Architecture, audience entry points, what users need to do, what's tricky |
| Presentation | Key takeaways, narrative structure, what needs to land, what's surprising |

The agent does not suggest substance. The agent asks, clarifies, deepens — but the substance originates with the human.

## Deepening Questions

Within each movement, use the Paul-Elder categories to deepen:

| Category | Purpose | Example |
|----------|---------|---------|
| **Clarification** | Surface what they mean | "What do you mean by X?" |
| **Assumptions** | Expose what must be true | "What has to hold for that claim?" |
| **Evidence** | Ground in measurement | "What was actually measured? By whom?" |
| **Viewpoints** | Test from other angles | "How would a skeptic see this?" |
| **Implications** | Follow the thread forward | "If that's true, what else follows?" |
| **Meta** | Check the framing itself | "Why this question and not another?" |

Don't run through all categories mechanically. Follow the human's energy. When they say something with weight, go deeper there. When they're vague, clarify. When they're certain, probe assumptions.

## Voice Anchor

During discourse, co-create `voice.md` with the human. This document defines the author's voice and is injected into every downstream agent's context.

The voice anchor distinguishes:
- **Voice features** (protect): sentence rhythm, cross-domain connections, characteristic phrasing, strategic inefficiencies, humor, authority posture
- **Voice habits** (correct): patterns the author explicitly flags as unintentional

Only habits the author flags are correctable. Everything else is preserved by default.

Listen for voice signal in how the human talks during discourse — their natural phrasing, rhythm, rough edges. These carry voice. Note them in `voice.md`.

## Discourse Is Complete When

The agent can state back — in its own words, not the human's phrasing — what the human wants to communicate, the setup, and the substance. The human confirms or corrects. Iterate until the human says: "yes, that's what I mean."

**Output**: Two files written to the workspace:

| File | Contents |
|------|----------|
| `ground-truth.md` | The human's communicate, setup, and substance — faithfully captured. Immutable from this point. |
| `voice.md` | Voice features to protect, habits to correct. Co-created with the author. |

These are the only human-authored input documents for the entire pipeline. Every downstream agent reads them.

## What Discourse Does Not Do

- Comprehend source material — that's feynman (discovering skill)
- Survey sources — that's magellan (mapping skill)
- Suggest substance — the agent asks, the human generates
- Write content — downstream agents handle delivery
