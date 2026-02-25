---
name: discovering
description: "Inventio — discourse to draw out human ground truth, then comprehension transform on source material. Use when: starting any content workflow, establishing what is true before writing, comprehending research or code."
version: 0.1.1
---

# Discovering

> The methodology for going from raw source + human discourse to genuine understanding. Content production is the OUTPUT.

## Contents

- [Discourse](#discourse)
- [The Comprehension Transform](#the-comprehension-transform)
- [The Four-Pass Reading Protocol](#the-four-pass-reading-protocol)
- [Gap-State Tracking](#gap-state-tracking)
- [Radical Doubt as Method](#radical-doubt-as-method)
- [The Explain-Back Pattern](#the-explain-back-pattern)
- [Confidence-Gated Progression](#confidence-gated-progression)
- [Production Formats](#production-formats)

## Discourse

> The agent asks. The human generates. The human's generation IS the ground truth.

Discourse is the first move in every workflow. Three movements draw out everything downstream agents need: what the human wants to communicate, the context it lives in, and the substance itself.

**Why discourse comes first**: Without it, the agent pattern-matches source material and produces plausible content that was never grounded in human understanding. That's failure mode #4 — the generated. Discourse prevents it by making the human articulate the substance before any agent touches it.

**Why the agent asks and the human generates**: This is the interaction design principle the cix project itself is built on. When the agent generates and the human evaluates, the human is verifying — not thinking. When the agent asks and the human generates, the human activates their own understanding. The ground truth emerges from the human's generation, not from their approval of the agent's generation.

### The Three Movements

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

### Deepening Questions

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

### Discourse Is Complete When

The agent can state back — in its own words, not the human's phrasing — what the human wants to communicate, the setup, and the substance. The human confirms or corrects. Iterate until the human says: "yes, that's what I mean."

**Output**: Ground truth written to `ground-truth.md` in the workspace. The format adapts to the project — what matters is that the human's communicate, setup, and substance are captured faithfully. This is the only human-authored input document for the entire pipeline.

This output feeds the comprehension transform. The agent now has human-generated ground truth to check its comprehension against — not just source material.

---

## The Comprehension Transform

Before explaining, the agent must verify its understanding. Pattern-matching a source and producing a plausible explanation is failure mode #4 — the generated. The comprehension transform prevents this by making shallow engagement fail visibly.

LLMs are "often not context-faithful, answering while considering their parametric knowledge rather than relying exclusively on the text" (Park et al. 2024). When an agent reads source material, it may "understand" by blending what the source says with what it already "knows" — producing plausible but unfaithful interpretation.

**The foundational constraint**: LLMs cannot reliably self-correct reasoning without external feedback (Huang et al. ICLR 2024). Metacognition must be architecturally designed, not hoped for. The techniques below introduce structural independence between generation and verification.

## The Four-Pass Reading Protocol

Adapted from SSR++ (Han et al. 2025) and academic reading strategies:

**Pass 1 — Literal**: What does this say?
- Extract claims, structure, terminology
- Identify what's stated explicitly
- Map the argument's skeleton

**Pass 2 — Interpretive**: What does this mean?
- Connect claims to each other
- Identify the reasoning chain (A therefore B therefore C)
- Spot gaps in the reasoning (where does the chain jump?)

**Pass 3 — Critical**: What does this assume?
- What must be true for the argument to hold?
- What's the weakest link?
- What contradicts this elsewhere?

**Pass 4 — Reconstructive** (the Feynman pass): Can I rebuild this?
- Close the source. Reconstruct the argument from memory.
- Where reconstruction fails? Those are comprehension gaps.
- Return to source specifically for the gaps.

## Gap-State Tracking

Maintain an explicit state throughout discovery (adapted from MemR3, arXiv:2512.20237):

    ESTABLISHED:
    - Claim X is supported by evidence Y (source: section)
    - Mechanism Z works because of A

    GAPS:
    - I don't understand how B leads to C
    - The paper claims D but doesn't explain the mechanism
    - E contradicts F and I haven't resolved the contradiction

    ASSUMPTIONS:
    - I'm assuming G, which isn't stated in the source
    - The paper assumes H, which may not hold in our context

Making gaps explicit prevents the agent from papering over them with fluent prose. Gaps don't disappear — they get resolved or flagged.

## Radical Doubt as Method

After forming understanding, apply Descartes' method operationalized (Zavala et al. MDPI AI 2025):

- "Could I be wrong about what the author means by X?"
- "Could I be wrong about the relationship between A and B?"
- "What would someone who disagrees with my interpretation say?"
- "Am I following the source or my own prior beliefs?"

### Five Whys for Comprehension

Each "why" peels an assumption layer (Ohno/Toyota). If the agent can't answer the third why, understanding is insufficient:

    Claim: "Cognitive offloading reduces critical thinking"
    Why? When AI handles cognitive work, humans practice it less.
    Why? Skills require deliberate practice to maintain.
    Why? Neural pathways weaken without activation.
    Why? The brain prioritizes efficiency — unused circuits get pruned.
    Why? Biological resources are finite and costly.
    Root: biological resource allocation, not laziness.

### Adversarial Self-Questioning (MAPS Critic)

Three types of checks from MAPS (arXiv:2503.16905):
1. **Existential**: Does this claim actually hold? Is this thing real?
2. **Consistency**: Does this contradict something established earlier?
3. **Boundary**: What happens at the edges? What breaks?

## The Explain-Back Pattern

The agent explains its understanding to the human BEFORE producing reader-facing content. Not an explanation for the end reader — an explanation of what the agent thinks the source material says.

**Interactive mode** (with human in the loop): The agent says "Here is what I understand" with explicit uncertainty flags. Human corrects misunderstandings. Agent updates and re-explains until human confirms comprehension. Only then does the agent write the reader-facing explanation.

**Internal mode** (agent self-checks): Agent explains the mechanism to itself, then checks against source. Where explanation diverges from source, comprehension gap exists. Weaker than interactive mode but better than no check.

**When to use interactive mode**: Novel domains, research synthesis, high-stakes content. For routine documentation, internal mode suffices.

## Confidence-Gated Progression

The agent cannot proceed to writing until its gap list is either empty or explicitly acknowledged.

**Structural confidence categories** (not verbalized confidence — that's unreliable):

| Category | Meaning | Signal |
|----------|---------|--------|
| **Solid** | Multiple verification paths converge, comprehension tests pass | Proceed |
| **Probable** | Most paths converge, minor uncertainty remains | Proceed with caveats |
| **Uncertain** | Paths diverge, comprehension tests reveal gaps | Flag in output |
| **Unknown** | Cannot verify, insufficient source material | Flag or ask human |

Never present "uncertain" as "solid." Never use verbalized confidence alone — always pair with structural checks.

### Comprehension Verification Tests

Before proceeding from discovery to writing:

1. **Rephrase test**: Can you state the key ideas without using the source's phrasing?
2. **Implication test**: What follows from this? What does this predict about situation X?
3. **Contradiction test**: What would disprove this? Strongest counterargument?
4. **Boundary test**: Where does this apply and where does it break down?
5. **Novelty test**: Can you generate an example the source doesn't include?

If any test produces incoherent or surface-level responses, the agent has not understood — it has pattern-matched.

## Production Formats

Once the comprehension transform is complete, content is produced in Diataxis formats — each encodes knowledge at a different register:

| Reader says | Write a | Door emphasis |
|-------------|---------|---------------|
| "Teach me X" | Tutorial | Door 3 heavy, Door 1 emerges |
| "How do I do X?" | How-to | Door 3 only, assume understanding |
| "Why does X work?" | Explanation | Door 1 through Door 2 |
| "What exactly is X?" | Reference | Door 2 (structured lookup) |

Don't mix types in one document.

The comprehension transform determines the Diataxis type. The Diataxis type determines the entry door. The entry door determines how all three doors are woven. This is the pipeline: understand first, then choose format, then encode.

## References

Load for detail:
- `references/metacognition.md` — Full discovery protocol, CoVe factored execution, token budgets, failure modes, effect sizes
