# What is ix?

**ix** = Intelligent Experimentation — a QoS experimentation platform for AI agents, skills, and extensions.

---

## The Problem

You've built an AI skill. It works in demos. But does it *actually* activate on the right prompts? Does it stay quiet when it should? What happens when five skills compete for the same context? What's the variance across runs?

Traditional testing gives you binary pass/fail. But AI behavior isn't binary — it's *distributional*. You need to measure characteristics, not correctness.

> "Skills evals aren't unit tests — you're measuring behavioral characteristics, not correctness."

## What ix Does

ix runs **experiments** against AI systems. You write cases, ix runs them multiple times, and gives you F1, precision, recall.

```bash
$ ix run skill-activation --lab ci-lab --mock --seed 42
Running skill-activation in lab ci-lab (28 cases, 5 trials, mock)
  must-001: OK (score=100%)
  must-002: OK (score=80%)
  ...

────────────── Results ──────────────
  Precision    100.0%
  Recall        93.3%
  F1            96.6%

Status: EXCELLENT
```

Each experiment runs multiple **trials** per case — AI behavior is stochastic, so a single run tells you nothing. Five trials per case, majority vote per case, F1 across all cases. That's the shape.

## The Hypothesis

Every experiment starts with a question: *"Does build-eval activate on eval-related prompts?"*

That question becomes a config: 28 cases (some that must trigger, some that must not), 5 trials each, an activation sensor. ix runs it and tells you precision, recall, F1. Not "passed" or "failed" — how well.

```
"Does build-eval activate correctly?"
  → 15 must_trigger cases
  → 10 should_not_trigger cases
  → 3 acceptable cases (excluded from metrics)
  → 5 trials each → majority vote → F1
```

## What ix Is NOT

- **Not a test framework.** pytest tests correctness. ix measures quality of service.
- **Not binary.** Results are distributions, not pass/fail.
- **Not just evals.** ix also supports comparative experiments (A vs B) and benchmarks.
- **Not eval methodology.** The build-evals skill teaches *what* to eval. ix is the platform that *runs* experiments.
