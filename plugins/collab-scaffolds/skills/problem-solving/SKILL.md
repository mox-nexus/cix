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
- [Problem → Technique Routing](#problem--technique-routing)
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

### Step 3: Route to the Right Technique

Use the [Problem → Technique Routing](#problem--technique-routing) table. Classify → route → apply. Don't prescribe yourself verbose steps — activate the right reasoning mode.

### Step 4: One Thing at a Time

Pick the smallest verifiable piece. Do that. Confirm it works. Then the next piece.

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

## Problem → Technique Routing

You already know these techniques. This table tells you **when** to reach for each one and **what to watch for**. Frame the WHY, not the HOW — explicit procedures on frontier models degrade performance (arXiv 2510.22251).

| Problem Type | Why This Technique | Caution | Verify |
|---|---|---|---|
| **Something's broken** | Hypothesize from evidence. Smallest reproducing input. Test one variable. | Don't fix before understanding — speculative fixes take 66% longer (SO 2025) | Does the fix address root cause or just symptoms? |
| **Complex structure** | DAC: Decompose into independent parts, Abstract the pattern across parts, Compose the solution. Abstraction is the highest-value step (RLAD 2025: +27%). | Premature abstraction before decomposition is complete | Can each part be verified independently? |
| **Root cause unknown** | Five Whys: Ask "why?" recursively until you hit the systemic cause, not the symptom | Stopping at the first plausible cause — keep asking | Would fixing this prevent recurrence, not just this instance? |
| **Decision with tradeoffs** | Frame constraints first, eliminate violators, compare what remains. Show what you chose, rejected, and why. | Anchoring on first option considered | What would change your mind about this choice? |
| **Evolving situation** | Observe-Orient-Decide-Act. Don't wait for perfect information. | Analysis paralysis — act on good-enough information, reorient | Did the action produce the expected observation? |
| **Exploration needed** | Diverge (quantity, no judgment) then Converge (against constraints, pick simplest) | Converging too early; judging during divergence | Did you explore at least 3 genuinely different approaches? |
| **Going in circles** | You're solving the wrong problem. What assumption is common to all attempts? | Sunk cost of previous attempts anchoring you | If you started fresh, would you approach it the same way? |

**The principle:** Activate the right reasoning mode for the problem type. Don't prescribe steps — your internalized patterns are better than explicit procedures (TMK: WHY framing 31.5% → 97.3% on reasoning tasks).

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

## Iteration Awareness

After 3 failed attempts at the same problem, stop and self-assess.

**Research:** Shukla et al. found a 37.6% increase in security vulnerabilities after 5 conversational iterations. Each iteration without convergence increases the chance of introducing new problems.

### The 3-Iteration Check

After 3 attempts that haven't converged:

1. **Am I solving the right problem?** — Restate the actual goal
2. **Am I repeating the same approach?** — If yes, the approach is wrong, not the execution
3. **Is my context still fresh?** — After many iterations, assumptions accumulate silently

### Context Health

| Signal | Meaning | Action |
|--------|---------|--------|
| Referencing things from 50+ messages ago | Context may be stale | Re-read the relevant files |
| Making contradictory suggestions | Context degraded | Suggest `/clear` or subagent |
| Trying the same approach differently | Not learning from failures | Wolf Protocol |
| Solution complexity growing each attempt | Solving symptoms, not cause | Step back, reframe |

See [iteration-limits.md](references/iteration-limits.md) for the research and counter-patterns.

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
| Iteration limits and context health | [iteration-limits.md](references/iteration-limits.md) |
