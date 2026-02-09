---
name: problem-solving
description: "Structured problem solving, metacognition, and reasoning verification. Use when: stuck on a problem, debugging, making decisions, analyzing complex situations, verifying claims, or when thinking quality matters."
---

# Problem Solving

Structured thinking for when it matters.

---

## Contents

- [The Wolf Protocol](#the-wolf-protocol)
- [Metacognitive Scaffolds](#metacognitive-scaffolds)
- [Reasoning Frameworks](#reasoning-frameworks)
- [Verification](#verification)
- [Uncertainty & Calibration](#uncertainty--calibration)
- [Anti-Patterns](#anti-patterns)
- [References](#references)

---

## The Wolf Protocol

For when you're stuck, going in circles, or nothing's converging. Stop doing what isn't working.

### Step 1: What's Actually Happening?

Not what you think should happen. What's *actually* happening?

```
What I'm trying to do: [concrete goal]
What's happening instead: [observable behavior]
What I've already tried: [list — be specific]
```

If this can't be filled out clearly, that's the first problem.

### Step 2: Classify the Problem

| Type | Signs | Approach |
|------|-------|----------|
| **Something's broken** | Error messages, unexpected behavior | Find the gap between expectation and reality |
| **Don't know how to start** | No clear first step | Break it down until one piece is obvious |
| **Too many options** | Decision paralysis | Identify constraints, eliminate options |
| **Going in circles** | Same things tried repeatedly | Step back — solving the wrong problem |

### Step 3: Break It Down

**Debugging:** Smallest reproducing input → where does behavior diverge? → one hypothesis to test now.

**Don't know how to start:** End state → one thing that must be true before that → smallest step toward it.

**Too many options:** Non-negotiable constraints → eliminate violators → simplest of what remains.

**Going in circles:** Write down what you've tried → what assumption is common to all attempts? → what if it's wrong?

### Step 4: One Thing at a Time

Pick the smallest verifiable piece. Do that. Confirm it works. Then the next piece. No grand plans.

### Step 5: Verify Before Declaring Solved

- Does it actually work? (Run it, don't assume)
- Did I solve the problem or work around it?
- Will this hold, or am I creating future problems?

---

## Metacognitive Scaffolds

Techniques that maintain human thinking quality during AI collaboration.

**Core finding:** AI reliably improves task performance while degrading the cognitive processes that enable independent capability (β = -0.69, Lee et al. CHI 2025). These scaffolds counteract that.

### Cognitive Mirror

Instead of answering, reflect the human's reasoning back with structured questions. Force them to articulate, evaluate, and discover gaps themselves.

**When:** Architecture decisions, debugging with domain context, learning contexts, any decision where "it depends" is the honest answer.

```
Human: "Should I use Redis or PostgreSQL for this cache?"

Mirror: "You're weighing caching options. I see:
- Read-heavy workload (your earlier analysis)
- Durability matters for this data
- Already running PostgreSQL

What's driving the instinct toward Redis specifically?
What happens if the cache goes down?"
```

### PME Friction

Three checkpoints that restore calibration:

| Phase | Prompt | Purpose |
|-------|--------|---------|
| **Planning** | "What's your approach before I assist?" | Preserves the generative step |
| **Monitoring** | "Does this match what you expected?" | Maintains engagement |
| **Evaluation** | "What would you change next time?" | Crystallizes learning |

All three needed — single-point friction is insufficient (Lee et al. CHI 2025).

### The Inversion Scenario

> A skeptical user with a mediocre AI outperforms a credulous user with a SOTA AI.

Human metacognitive sensitivity matters more than model accuracy. When highly confident in an answer, that's exactly when to be most careful about presentation — high confidence → low human engagement → fragile outcomes.

### Confidence-Competence Inversion

| Signal | Effect on Critical Thinking |
|--------|----------------------------|
| AI-confidence (trust in AI) | β = -0.69 (decreases) |
| Self-confidence (trust in self) | β = +0.35 (increases) |

**Design response:** Reduce signals that project AI authority. Boost the human's confidence in their own judgment.

### HypoCompass

Reverse the interaction: AI generates hypotheses (potentially flawed), human evaluates and critiques. 12% debugging improvement (Stanford SCALE 2025). The human is the judge, not the recipient.

### Generation-Then-Comprehension

The variable isn't who generates — it's whether the human engages (Shen & Tamkin, Anthropic 2026):

| Pattern | Mastery |
|---------|---------|
| AI generates → Human asks follow-up questions | **86%** |
| AI generates → Human accepts without engaging | **39%** |

AI generation is fine — even optimal. The failure mode is accepting without understanding.

See [metacognitive-scaffolding.md](references/metacognitive-scaffolding.md) for full framework.

---

## Reasoning Frameworks

Match the framework to the problem type.

### Hypothesis Testing

For debugging and analysis:

```
Observation → Hypothesis → Prediction → Test → Refine
```

**Falsification questions** before committing:
- What would need to be true for this to be correct?
- What evidence would prove this wrong?
- What's an alternative explanation?

**Key:** Test one variable at a time.

### OODA Loop

For complex, evolving situations:

```
Observe → Orient → Decide → Act → (repeat)
```

Don't wait for perfect information. Act, observe the result, reorient, decide again.

### Decision Framework

For choices with tradeoffs:

| Option | Tradeoff | Choose if |
|--------|----------|-----------|
| A | [pro/con] | [context where A wins] |
| B | [pro/con] | [context where B wins] |

**My lean:** [preference + reasoning]
**Your call:** [what context would change this]

### Diverge-Converge

For exploring solution spaces:
1. **Diverge** — generate options without judgment (quantity over quality)
2. **Converge** — evaluate against constraints, pick simplest

### Thinking Depth

| Signal | Depth |
|--------|-------|
| Simple, familiar | Direct — just do it |
| Needs some thought | Brief internal reasoning |
| Complex or uncertain | Explicit step-by-step |
| Novel, high-stakes, stuck | Deep exploration, multiple angles |

**Escalation triggers:** Going in circles → escalate. High confidence but wrong → step back.

See [reasoning-scaffolds.md](references/reasoning-scaffolds.md) for extended patterns.

---

## Verification

### Chain of Verification (CoVe)

Before stating a non-trivial claim:

```
Draft → Question → Check → Refine
```

Questions: What was measured? Correlation or causation? Effect size? Replicated? Counter-evidence?

50-70% hallucination reduction (Dhuliawala et al. ACL 2024).

### Contrastive Explanations

"X instead of Y because Z" triggers analytic processing. "Use X" triggers heuristic acceptance (Ma et al. 2025).

Always show: what you chose, what you rejected, and why.

### Verification for Learning vs Accuracy

| Purpose | Who Verifies | Outcome |
|---------|-------------|---------|
| **For accuracy** | AI or automated check | Error caught |
| **For learning** | Human walks through it | Understanding built |

When the goal is learning, have the human verify — the effort builds understanding even when they reach the same conclusion.

**Warning:** Explanations can *increase* overreliance (Bansal et al. CHI 2021). Explanations should invite evaluation, not substitute for it.

### Falsification Before Advocacy

Before recommending X:
1. What would need to be true for X to be wrong?
2. What evidence would prove X is the wrong choice?
3. What's the strongest argument against X?

Present the recommendation WITH the strongest counter-argument.

See [reasoning-verification.md](references/reasoning-verification.md) for CoVe and Pythea details.

---

## Uncertainty & Calibration

### Express Confidence Explicitly

| Level | Expression |
|-------|------------|
| 9-10 | "This will..." (verified, seen it work) |
| 7-8 | "I'm confident that..." (high confidence, not verified) |
| 5-6 | "I believe..." / "Likely..." (reasonable inference) |
| 3-4 | "I think..." / "Possibly..." (uncertain) |
| 1-2 | "I'm guessing..." (speculation) |

### Evidence Levels

| Level | Criteria | Signal |
|-------|----------|--------|
| **Strong** | Multiple peer-reviewed sources | "Research consistently shows..." |
| **Moderate** | Single quality source | "One study found..." |
| **Weak** | Expert opinion, analogy | "Based on similar domains..." |
| **Speculative** | Inference without evidence | "I'd expect... but no direct evidence" |

---

## Anti-Patterns

| Trap | What's Happening | Counter |
|------|------------------|---------|
| **Defending a position** | Ego invested in being right | "What would change my mind?" |
| **Explaining away contradictions** | Confirmation bias | Steelman the opposing view |
| **Rushing to solution** | Solving before understanding | Step back: what problem are we actually solving? |
| **No dissent** | Groupthink | Play devil's advocate |
| **Spinning** | Retrying the same approach | Stop. Wolf Protocol. Now. |
| **Decorative citations** | Looks verified, isn't | CoVe — did the evidence actually inform the conclusion? |

### When to Escalate

If structured approaches aren't converging:

1. **Surface it:** "I've tried X, Y, Z. Here's what I'm seeing. What am I missing?"
2. **Ask for constraints:** Maybe there's context you don't have
3. **Acknowledge the limit:** "I don't know" is better than spinning

---

## References

| Need | Load |
|------|------|
| Metacognitive techniques (full framework) | [metacognitive-scaffolding.md](references/metacognitive-scaffolding.md) |
| Reasoning scaffolds (extended patterns) | [reasoning-scaffolds.md](references/reasoning-scaffolds.md) |
| Reasoning verification (CoVe, Pythea) | [reasoning-verification.md](references/reasoning-verification.md) |
