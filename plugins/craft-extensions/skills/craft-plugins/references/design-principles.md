# Design Principles

Five principles governing every cix extension, grounded in collaborative intelligence research.

---

## The Five Principles

| # | Principle | Rule | Research Anchor |
|---|-----------|------|-----------------|
| 1 | Complementary, Not Substitutive | AI amplifies, human remains central | Bastani -17%, mastery OR=35.7 |
| 2 | Pit of Success | Right thing is the only obvious path | Parnin (83% start with code) |
| 3 | Transparent Abstractions | Can't see through it, can't learn from it | Blaurock β=0.415 |
| 4 | Compound Value | Every change makes the next change easier | McConnell (50% annual maintenance) |
| 5 | Composable, Not Comprehensive | Small focused extensions that combine | Diversity loss g=-0.863 |

---

## 1. Complementary, Not Substitutive

The fundamental rule. Every extension must amplify human capability, never substitute for it.

Three modes of AI interaction:

| Mode | Mechanism | Outcome |
|------|-----------|---------|
| **Substitutive** | AI does the work, human approves | Capability atrophies |
| **Complementary** | AI amplifies, human remains central | Capability compounds |
| **Constitutive** | Collaboration enables what neither could alone | New capability emerges |

Every extension MUST be complementary or constitutive. Never substitutive.

### WHY > HOW

Explaining motivation produces better outcomes than prescribing method:

```
Bad:  "Always use prepared statements for SQL"
Good: "SQL injection occurs when user input is treated as code.
       Prepared statements separate data from code.
       Consider: where does untrusted input enter your query?"
```

### Protective Practices

Extensions should encourage:
- **Attempt-first** — try before consulting AI. Preserves problem-solving practice.
- **Verification workflows** — human review of all AI contributions.
- **Metacognitive prompts** — "What do you think?" before revealing AI analysis.
- **Explicit uncertainty** — evidence levels: Strong / Moderate / Weak / Speculative.

### Research

- Students who learned with AI dropped **-17%** below control once AI was removed (Bastani, PNAS 2025)
- Medical skill degradation **-20%** after AI exposure (Budzyn, Lancet 2025)
- Mastery-oriented users are **35.7x** more likely to maintain critical thinking than performance-oriented users (Pallant et al. 2025)
- Skill formation gap **d=0.738** (Anthropic RCT 2026)

---

## 2. Pit of Success

Make the right thing the only obvious path. Don't rely on documentation or willpower. Structure interfaces so mistakes are hard and correct behavior is natural.

Subsumes two related concepts:

**Defaults for most, escape hatches for few (80/20):**
- Intent-driven interface as primary (80% of users)
- Transparent abstractions as middle layer
- Raw access / SQL / flags as escape hatch (20%)

**Catch errors where they originate (mistake-proofing):**
- Validate input early
- Surface uncertainty at decision points
- Fail fast with clear diagnostics

### Two Tests

1. **Could someone unfamiliar fall into the right pattern?** If no, the default is wrong.
2. **If this goes wrong, where will we find out?** If the answer is "production," the error surface is too late.

### Research

- 83% of developers start with code, not docs (Parnin & Treude)
- Average time spent on documentation: 15 seconds (Robillard)
- Parse, don't validate — encode invariants in types, not runtime checks

---

## 3. Transparent Abstractions

If you can't see through it, you can't learn from it.

Four properties every abstraction should have:

| Property | Meaning |
|----------|---------|
| **Readable** | Plaintext, no magic |
| **Forkable** | Copy, modify, make your own |
| **Verifiable** | Claims have sources |
| **Observable** | See what the tool does |

### Show the Chain

Every extension output should make its reasoning visible:
- Observation (what was seen)
- Analysis (what it means)
- Recommendation (what to do)
- Evidence level: Strong / Moderate / Weak / Speculative

### The Transparency Paradox

Explanations that **substitute** for human evaluation increase overreliance. Explanations that **support** human evaluation reduce it. The difference: does the user still do the evaluative thinking, or does the explanation do it for them?

### Research

- Transparency effect: **β=0.415** (Blaurock 2025, n=654) — second strongest design lever
- Chain-of-Verification reduces hallucination **50-70%** (Dhuliawala et al.)
- But: AI confidence predicts less critical thinking, **r=-0.68** (Gerlich 2025)

---

## 4. Compound Value

Every change should make the next change easier.

Quick fixes, workarounds, special cases compound cost. Clean abstractions, complete implementations, single source of truth compound value.

**Before acting:** Does this make the next change easier or harder?

### Signals

- **Compounding value:** Single source of truth, clean interfaces, complete implementations
- **Compounding cost:** Scattered copies, workarounds, "just for now" hacks, dead code left "just in case"

### Research

- 50% of development effort goes to maintenance (McConnell)
- Modification time increases 2-3x with scattered dependencies (Cataldo)

---

## 5. Composable, Not Comprehensive

Small, focused extensions that combine are better than monolithic agents that handle everything opaquely.

```
Good: security-review + api-contracts + observability -> Human synthesizes
Bad:  "full-code-review-agent" that handles everything
```

### Orthogonality Lock

Agents provide ONE perspective, not comprehensive coverage. This forces human synthesis across multiple viewpoints — which is where the learning happens.

### Defense in Depth (Implementation Pattern)

Multiple complementary approaches catch what single solutions miss:
- Intent-driven interface (primary)
- Escape hatch (secondary)
- Raw access (tertiary)

If one approach doesn't work for a user's case, another catches them.

### Research

- Diverse groups outperform best-ability homogeneous groups (Hong & Page)
- AI-generated outputs show diversity reduction **g=-0.863** across 28 studies, n=8,214
- The effect persists after AI withdrawal — homogenization is structural

---

## Implementation Patterns

Concrete techniques for operationalizing the five principles. Brief descriptions here; see `../../../docs/explanation/methodology.md` for depth.

| Pattern | Mechanism | Principle |
|---------|-----------|-----------|
| **Cognitive Friction** | Add friction at decision points to prevent autopilot | Complementary |
| **Contrastive Explanations** | "X instead of Y because Z" — shows alternatives | Transparent |
| **Glass Box** | Show reasoning traces, not just outputs | Transparent |
| **Observable Agents** | Work aloud — show what the agent is doing | Transparent |
| **Socratic Mode** | Guiding questions instead of direct answers | Complementary |
| **Reflection Prompts** | "What do you think?" before revealing analysis | Complementary |

---

## Anti-Patterns

| Anti-Pattern | Signal | Alternative |
|--------------|--------|-------------|
| **Auto-fix** | Human doesn't learn why | Explain issue, offer fix, human applies |
| **Black box** | Human can't evaluate | Show reasoning at every step |
| **Scope creep** | Agent does more than asked | Strict orthogonality constraints |
| **Confidence theater** | Fake certainty | Explicit uncertainty (evidence levels) |
| **Memory hoarding** | Private agent state | Shared knowledge substrate |
| **Paternalism** | "I know better" | "Here's my perspective, you decide" |

---

## Research Coefficients

Quick-reference table. All magnitudes are approximate — treat as directional, not precise.

| Finding | Effect Size | Source | Context |
|---------|------------|--------|---------|
| Control (user agency) | β=0.507 | Blaurock 2025 (n=654) | Strongest design lever |
| Transparency | β=0.415 | Blaurock 2025 (n=654) | Second strongest |
| Engagement features | b=-0.555 | Blaurock 2025 (n=654) | Paternalistic "help" backfires |
| Mastery orientation | OR=35.7 | Pallant et al. 2025 | 35.7x more likely to maintain critical thinking |
| Diversity reduction | g=-0.863 | Meta-analysis (28 studies, n=8,214) | Persists after AI withdrawal |
| Skill formation gap | d=0.738 | Anthropic RCT 2026 | 17 percentage point gap |
| AI / critical thinking | r=-0.68 | Gerlich 2025 | Higher AI confidence = less thinking |
| Cognitive offloading / CT | r=-0.75 | Gerlich 2025 | Offloading predicts reduced CT |
| Learning harm (no guardrails) | -17% | Bastani, PNAS 2025 | Eliminated by hint-based design |
| Skill degradation | -20% | Budzyn, Lancet 2025 | Medical domain |

Full bibliography: `docs/content/library/reference/bibliography.md`
