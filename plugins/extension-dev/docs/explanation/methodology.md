# Building Extensions: Methodology

Why these patterns exist and the research behind them.

---

## Contents

- [The Core Problem](#the-core-problem)
- [Mastery vs Performance Orientation](#mastery-vs-performance-orientation)
- [The Review Pattern](#the-review-pattern)
- [Why These Principles](#why-these-principles)
- [Collaborative Intelligence Design Patterns: The Why](#collaborative-intelligence-design-patterns-the-why)
- [Effect Sizes](#effect-sizes)
- [The Test](#the-test)
- [The Three Modes](#the-three-modes-complementary-constitutive-substitutive)
- [Study Limitations](#study-limitations)
- [The Deeper Why](#the-deeper-why)

---

## The Core Problem

AI creates a dissociation: **system performance goes up while human competence goes down**.

| What Improves | What Degrades |
|---------------|---------------|
| Output speed | Critical thinking (r = -0.75) |
| Task completion | Procedural knowledge |
| Artifact quality | Debugging intuition |

This isn't speculation. Multiple peer-reviewed studies from CHI, PNAS, and The Lancet document this pattern across domains—from legal reasoning to medical procedures to creative writing.

The implication: if we build AI tools the naive way (maximize immediate output), we create tools that make humans progressively less capable of working without them. That's dependency, not augmentation.

---

## Mastery vs Performance Orientation

Research on goal orientation shows two distinct patterns:

**Mastery orientation**: User treats AI as collaborator, questions output, maintains critical evaluation. These users maintain capability over time.

**Performance orientation**: User treats AI as oracle, accepts output, focuses on task completion. These users show skill degradation.

The extension's design determines which orientation it encourages. Speed-optimized interfaces push users toward performance orientation.

---

## The Review Pattern

Claude generates. The human reviews. The critical variable is whether the human **can** evaluate.

| Pattern | Effect |
|---------|--------|
| Output only | Human rubber-stamps (no basis for evaluation) |
| Output + reasoning | Human can evaluate logic |
| Output + alternatives + tradeoffs | Human makes informed judgment |

Extensions must provide the information needed for genuine evaluation, not just acceptance.

---

## Why These Principles

### Transparency (β = 0.415)

When users can see reasoning, they can:
- Evaluate whether the reasoning is sound
- Learn the underlying framework
- Calibrate trust appropriately
- Catch errors before they propagate

This isn't "explainability theater"—it's genuine visibility into the decision process.

### Control (β = 0.507, strongest)

Control doesn't mean approval bottlenecks. It means:
- Users can observe what's happening
- Users can steer the direction
- Users can override when needed
- Users retain agency throughout

Perceived control correlates more strongly with positive outcomes than any other feature.

### Engagement Features (b = -0.555, negative)

Paternalistic "helpfulness" backfires. Blaurock found engagement features have **negative effects** for frequent users.

This is why hooks should suggest, not block:
- Blocking removes agency (hurts control)
- Paternalistic engagement annoys frequent users
- Provide value (suggestion) without removing choice (blocking)

### Collaborative Learning

Users with mastery orientation maintain critical thinking; those with performance orientation show degradation.

Tool design should encourage mastery:
- Explain WHY, not just WHAT
- Invite verification
- Build mental models, not dependency
- Make users more capable, not the tool more capable

### Provenance

Without provenance:
- Errors compound invisibly
- Users can't verify or learn
- Trust becomes binary (accept/reject)
- Hallucinations propagate

Chain-of-Verification (CoVE) reduces hallucination by 50-70% through independent verification.

### Non-Conformity (g = -0.863 diversity loss)

**The Artificial Hivemind problem** (NeurIPS 2025 Best Paper): 70+ LLMs converge on the same outputs. When 25 models write "a metaphor about time," only 2 clusters emerge. Temperature and ensembling don't help—RLHF punishes diversity.

**Meta-analysis** (28 studies, n=8,214): Diversity reduction effect size is **g = -0.863**. Individual performance goes up, collective diversity crashes.

Why this matters for extensions:
- If everyone uses the same AI the same way, outputs homogenize
- Hong & Page: diverse groups outperform best-ability groups
- Homogenization destroys the collective intelligence that makes teams effective

Extension design should preserve diversity:
- Encourage multiple perspectives (orthogonal agents)
- Support questioning and dissent
- Use diverse personas/framings where possible
- Don't optimize for consensus—optimize for useful disagreement

**Mitigation evidence**: Wan & Kalman (2025) showed diverse AI personas eliminate homogenization. Design CAN preserve diversity.

### The Perception Paradox (Anthropic, Jan 2026)

Sharma et al. analyzed ~1.5M Claude.ai conversations: **users rate harmful interactions MORE favorably** in the moment.

But when users acted on AI outputs, satisfaction dropped below baseline. Users expressed regret.

Implication: Users can't reliably self-correct. Short-term satisfaction ≠ long-term benefit. Design must compensate—transparency and control aren't optional, they're necessary because the feedback loop is broken.

---

## Collaborative Intelligence Design Patterns: The Why

### 1. Cognitive Friction

**Pattern**: Add friction at decision points (e.g., `confirm --reason "..."`)

**Why it works**: Frictionless interfaces promote cognitive offloading. Requiring articulation maintains engagement. The friction forces the user to think before accepting.

**When to use**: Irreversible actions, high-stakes decisions, learning contexts.

### 2. Contrastive Explanations

**Pattern**: "X instead of Y because Z" rather than "Use X"

**Why it works**: Contrastive framing triggers analytic processing rather than heuristic acceptance. The brain naturally evaluates tradeoffs when alternatives are visible.

### 3. Glass Box

**Pattern**: Show reasoning traces, make logic inspectable

**Why it works**: Opaque systems prevent learning. Visibility enables:
- Verification of logic
- Learning from the process
- Modification and improvement

### 4. Cognitive Velcro

**Pattern**: Natural language confidence ("I am guessing..." vs "I have verified...")

**Why it works**: Smooth interfaces provide nothing for the mind to grip. Texture from uncertainty markers, alternatives considered, and explicit caveats creates mental hooks for evaluation.

### 5. Observable Agents

**Pattern**: Work aloud—emit observations, conclusions, uncertainty

**Why it works**: Silent agents break team situational awareness. Humans need to know what's happening to maintain context and intervene when needed.

### 6. Reflection Prompts

**Pattern**: "What is the primary risk of this operation?"

**Why it works**: Metacognitive pauses force users to engage before proceeding. If they can't answer, they're not ready—and the system knows to provide more context.

### 7. Socratic Mode

**Pattern**: Guiding questions rather than direct answers

**Why it works**: For learning contexts, building mental models through guided discovery creates more durable understanding than receiving answers.

---

## Effect Sizes

### Design Levers (Blaurock Meta-Analysis, 106 studies)

| Lever | Effect Size | Implication |
|-------|------------|-------------|
| Control (user agency) | β = 0.507 | Strongest design lever |
| Transparency | β = 0.415 | Second strongest |
| Engagement features | b = -0.555 | Paternalistic "help" backfires |

### Harm Evidence (Multiple Sources)

| Finding | Effect Size | Source |
|---------|------------|--------|
| Diversity reduction | g = -0.863 | Meta-analysis (28 studies) |
| Skill formation gap | d = 0.738 (17pp) | Anthropic RCT (2026) |
| AI ↔ critical thinking | r = -0.68 | Gerlich (2025) |
| Offloading ↔ CT | r = -0.75 | Gerlich (2025) |
| Learning harm (no guardrails) | -17% | Bastani PNAS (2025) |
| Skill degradation | -22% | Lancet colonoscopy (2025) |

---

## The Test

For every extension feature:

1. **Does this make users more capable or more dependent?**
2. **Does this preserve the generative step?** (User does the thinking)
3. **Does this encourage mastery or performance orientation?**
4. **Would users be helpless after extended use?**
5. **Does this preserve diversity or push toward homogeneity?**

Extensions that fail these questions may boost short-term productivity while eroding long-term capability and collective intelligence.

---

## The Three Modes: Complementary, Constitutive, Substitutive

The fundamental design choice:

| Mode | Definition | Outcome |
|------|------------|---------|
| **Complementary** | AI amplifies existing human capability | User more capable after use |
| **Constitutive** | Enables capability neither could achieve alone | Novel collaboration emerges |
| **Substitutive** | AI replaces human thinking | Dependency, skill atrophy |

### Complementary

AI as amplifier. The human retains the generative step—doing the thinking—while AI provides leverage.

- "Here's how to think about this" (not "here's the answer")
- Human capability compounds over time
- User could work without the tool (but chooses not to)

### Constitutive

AI enables genuinely new capability through collaboration. Neither human nor AI could do it alone.

- Human + AI together can do what neither could separately
- The collaboration itself is the capability
- Examples: real-time code review during pair programming, exploratory search through massive corpora

### Substitutive (Avoid)

AI does the work, human approves. This is the pattern that causes skill atrophy.

- "Here's the answer" (human just accepts)
- Human capability degrades over time
- User becomes helpless without the tool

**Every extension should be complementary or constitutive. Never substitutive.**

---

## The Deeper Why

An AI tool that makes humans dependent has failed, regardless of how much immediate productivity it provides.

The goal isn't to build better tools. The goal is to build tools that make better humans—more capable, more knowledgeable, more autonomous.

That's what Collaborative Intelligence means.

---

## Study Limitations

For collaborators enhancing these extensions: the research provides directional guidance, not universal laws. Each study has specific limitations that matter when applying findings.

| Study | Limitation | What It Means |
|-------|-----------|---------------|
| Budzyn (Lancet, 2025) | Medical domain (colonoscopy) | Skill atrophy rate (-22%) may not transfer directly to software |
| Gerlich (2025) | Cross-sectional, self-reported | Correlations (r = -0.68, -0.75) show association, not causation |
| Lee et al. (CHI, 2025) | Self-reported critical thinking | Perceptions may differ from actual cognitive performance |
| Blaurock (106 studies) | Service contexts (not all software) | Effect sizes (beta = 0.507, 0.415) are directional for extension design |
| Bastani (PNAS, 2025) | Education domain (Turkish math) | -17% learning harm may vary across skill types and populations |
| Mastery OR = 35.7 | Single study | Large effect size from one study needs replication |
| Sharma (Anthropic, 2026) | Claude.ai conversations only | Perception paradox may differ across AI systems |

### What This Means

The direction is consistent across studies: transparency and control help, cognitive offloading harms learning, observable processes support better collaboration. But the specific magnitudes (beta = 0.507, r = -0.75, g = -0.863) should be treated as approximate, not precise.

When enhancing extensions, use these findings to inform design decisions — but don't treat them as engineering constants. The research tells us WHAT to optimize for (control, transparency, mastery orientation). The exact numbers tell us roughly HOW MUCH each lever matters relative to others.

---

See [sources.md](sources.md) for full bibliography.
