# Eval-First Design

Why measurement comes before shipping, not after.

---

## Contents

- [The Problem](#the-problem)
- [Eval-First Philosophy](#eval-first-philosophy)
- [What to Evaluate](#what-to-evaluate)
- [The Dual Failure Modes](#the-dual-failure-modes)
- [Why Single Metrics Lie](#why-single-metrics-lie)
- [Connection to build-evals](#connection-to-build-evals)

---

## The Problem

Extensions are invisible. Unlike a UI component (where you can see if it's broken), an extension's failure modes are subtle:

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

## Connection to build-evals

This document covers the philosophy. For operational eval frameworks — choosing tools, building test suites, measuring agent effectiveness — see the **build-evals** plugin.

| Need | Where |
|------|-------|
| Why eval-first matters | This document |
| How to build evals | `build-evals` plugin |
| Quality gates for extensions | `extension-dev` evaluator agent |

The evaluator agent in `extension-dev` checks 7 quality gates (content, transparency, control, observability, activation, expert value, content efficiency). The `build-evals` plugin provides the broader framework for building automated test suites.

---

See [sources.md](sources.md) for full bibliography.
