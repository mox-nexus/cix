# Eval-First Design

Why measurement comes before shipping, not after.

---

## Contents

- [The Problem](#the-problem)
- [Eval-First Philosophy](#eval-first-philosophy)
- [Eval-First in Practice](#eval-first-in-practice)
- [What to Evaluate](#what-to-evaluate)
- [The Dual Failure Modes](#the-dual-failure-modes)
- [Why Single Metrics Lie](#why-single-metrics-lie)
- [The TDD Parallel](#the-tdd-parallel)
- [Connection to craft-evals](#connection-to-craft-evals)

---

## The Problem

Extensions are invisible. A broken button is obvious. A skill that silently ignores 80% of the prompts it should handle — that's invisible failure. Unlike a UI component (where you can see if it's broken), an extension's failure modes are subtle:

- A skill with vague triggers activates on the wrong prompts — or never activates at all
- An agent that sounds confident but gives generic advice passes casual review
- A hook that blocks too aggressively gets disabled rather than fixed

Without measurement, you discover these problems through user frustration, not systematic detection.

---

## Eval-First Philosophy

**Measure before you ship, not after.**

The principle: define what "good" looks like before building, then verify the extension meets that bar. This is the same discipline as test-driven development, applied to AI extensions.

| Without Evals | With Evals |
|---------------|------------|
| "Seems good" | Activation F1 = 0.85 |
| "Users like it" | Methodology adherence = 78% |
| "It works for me" | Content efficiency: 0 lines of tutorial |

The eval-first approach catches problems during development when they're cheap to fix, not in production when they've already eroded user trust.

---

## Eval-First in Practice

Here's the cycle applied to a real skill:

**1. Define "good"** — The `data-store` skill should activate when users ask about databases, search, embeddings, or RAG. It should NOT activate for general coding questions, deployment, or authentication.

**2. Measure** — Run activation eval against 20 test prompts (10 should-activate, 10 should-not):

```
Results:
  True Positives:  8/10  (activated correctly)
  False Positives: 3/10  (activated incorrectly)
  Precision: 0.73  |  Recall: 0.80  |  F1: 0.76
```

**3. Diagnose** — Precision is low (0.73): the skill fires on "How do I store user sessions?" (authentication, not data-store). Recall gap: misses "What embedding model should I use?" (no "database" keyword in prompt).

**4. Fix** — Update the skill description:
- Add: "embedding models, vector search, RAG pipelines"
- Add exclusion: "Not for: authentication, session management, caching strategies"

**5. Re-measure** — F1 improves from 0.76 to 0.88. Ship it.

Without eval-first, the precision problem (firing on auth questions) would surface as user complaints weeks later. The recall problem (missing embedding queries) might never surface — users just wouldn't know the capability existed.

---

## What to Evaluate

### Activation Quality

Does the extension activate on the right prompts and stay quiet on the wrong ones?

| Metric | What It Measures |
|--------|-----------------|
| **Precision** | Of activations, how many were correct? (Signal vs noise) |
| **Recall** | Of relevant situations, how many activated? (Coverage) |
| **F1** | Harmonic mean of precision and recall |

### Methodology Adherence

Does the extension follow its own stated methodology?

- LLM-as-judge evaluation against skill principles
- Spot-check outputs for transparency, control, reasoning quality
- Verify sources are cited, alternatives shown, uncertainty acknowledged

### Content Efficiency

Does every line justify its token cost?

- Zero tutorial content (Claude already knows basics)
- Decisions with recommendations, not option lists
- References that change behavior, not explain concepts

---

## The Dual Failure Modes

Extensions fail in two opposite directions:

### Over-Activation (noise)

The extension fires on prompts it shouldn't handle. Users see irrelevant guidance, learn to ignore the extension, and eventually disable it.

**Signal:** High recall, low precision. "It activates on everything."

### Under-Activation (missed value)

The extension stays silent when it should help. Users don't know the capability exists. The extension provides zero value for the use cases it was designed for.

**Signal:** High precision, low recall. "It never activates."

Both failures are invisible without measurement. A skill with 95% precision but 20% recall looks great when it fires — but misses 80% of the situations where it should help.

---

## Why Single Metrics Lie

Optimizing for one metric hides problems in the other:

| Optimize For | What Happens | What You Miss |
|-------------|--------------|---------------|
| Precision only | Narrow triggers, few false positives | Misses most relevant cases |
| Recall only | Broad triggers, catches everything | Floods user with noise |
| Accuracy only | Looks great on balanced data | Fails on real-world distributions |

You need **both** precision and recall (or their composite, F1) to understand activation quality. The same principle applies across all eval dimensions — a single number rarely tells the full story.

---

## The TDD Parallel

If you know test-driven development, eval-first follows the same discipline:

| TDD | Eval-First |
|-----|------------|
| Red: Write a failing test | Define: Write test prompts that should/shouldn't activate |
| Green: Make it pass | Measure: Run eval, see the score |
| Refactor: Improve without breaking | Fix: Tighten triggers, re-measure |

The difference: TDD tests binary correctness (pass/fail). Eval-first tests dimensional quality (precision, recall, methodology adherence). Both catch problems before users do.

---

## Connection to craft-evals

This document covers the philosophy. For operational eval frameworks — choosing tools, building test suites, measuring agent effectiveness — see the **craft-evals** plugin.

| Need | Where |
|------|-------|
| Why eval-first matters | This document |
| How to build evals | `craft-evals` plugin |
| Quality gates for extensions | `craft-extensions` evaluator agent |

The evaluator agent in `craft-extensions` checks 7 quality gates (content, transparency, control, observability, activation, expert value, content efficiency). The `craft-evals` plugin provides the broader framework for building automated test suites.

---

See [sources.md](sources.md) for full bibliography.
