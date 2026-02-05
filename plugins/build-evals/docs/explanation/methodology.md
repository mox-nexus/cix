# Eval Design: Methodology

Why these evaluation patterns exist and what they measure.

---

## The Core Problem

Single metrics mislead. Evaluation that doesn't match usage fails.

A skill with 100% activation rate sounds impressive until you realize it activates on every prompt—including when it shouldn't. A test suite that passes 95% of the time tells you nothing about the 5% of failures that corrupt production data.

**The failure mode:** Measuring what's easy instead of what matters.

This is why eval design centers on two questions:
1. What can go wrong?
2. How do we detect it before users do?

---

## Measurement Fundamentals

### The Two-Sided Test

Every capability has two failure modes:

| Failure Mode | Example | Detection |
|--------------|---------|-----------|
| **False negative** | Should trigger, doesn't | Recall metric |
| **False positive** | Shouldn't trigger, does | Precision metric |

Testing only one side creates blind spots.

**Example from skill evaluation:**

A Rust skill that activates on every coding question has perfect recall (never misses a valid case) but terrible precision (fires when writing Python, discussing architecture, writing docs).

The F1 metric forces you to balance both:
```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

You can't game it by optimizing one side.

### Why pass@k Exists

LLMs are stochastic. Single-run metrics lie about capability.

**The pattern:**
- 75% success rate per attempt
- pass@3 (any success in 3 tries): ~98%
- pass^3 (all 3 succeed): ~42%

Same model, radically different reliability depending on whether you need "works once" or "works every time."

This matters for deployment decisions:

| Use Case | Metric | Why |
|----------|--------|-----|
| Exploration | pass@k | One good solution is enough |
| Production | pass^k | Every execution must work |

---

## The Iterative Pattern (Ralph Discovery)

Traditional pass@k assumes independent trials. Real agents learn from feedback.

**The insight:** An agent with 60% first-try success might reach 95% with error feedback. That's a fundamentally different capability profile.

| Metric | Question Answered |
|--------|-------------------|
| **pass@1** | How good is the first attempt? |
| **pass@k (iterative)** | Can it recover from failures? |
| **recovery_rate** | What percentage of failures become successes? |
| **iterations_to_pass** | How fast does it learn? |

This changes deployment strategy:

```
Agent A: pass@1 = 80%, recovery_rate = 20%
→ Deploy with better prompts

Agent B: pass@1 = 60%, recovery_rate = 85%
→ Deploy with retry loop + feedback
```

Same apparent capability (both can hit 90%+), completely different implementation patterns.

---

## Multi-Agent Evaluation

Single-agent metrics miss the collaboration layer.

**The blind spot:** Each agent works perfectly in isolation, but handoffs fail. Task scores look good, but work is duplicated or dropped.

### Why Task Scores Aren't Enough

You need to measure the gaps between agents:

| Metric | Catches |
|--------|---------|
| **Handoff success** | Work dropped during transfers |
| **Communication efficiency** | Noise drowning signal |
| **Role adherence** | Agents doing each other's work |
| **Theory of Mind** | Misunderstanding collaborator state |

**Example failure mode:**

```
Agent A: Research task score = 90%
Agent B: Writing task score = 92%
Handoff success: 45%

Overall system: Task completion = 41%
```

Each component looks good. The system fails.

---

## Why Grader Types Matter

### Code-Based Graders (Preferred)

Deterministic, fast, objective.

```python
# ✅ Unambiguous
assert result.status == "success"
assert result.files_modified == ["config.yaml"]
```

**Use when:** You can specify exact expected state.

### Model-Based Graders (When Necessary)

LLM judges for open-ended tasks.

**The trap:** LLMs can't reliably grade their own outputs without bias.

**The solution:** Multi-judge agreement or human spot-checks.

**Use when:**
- Output varies legitimately (creative writing, explanations)
- Outcome matters more than path
- Applying partial credit for multi-component tasks

### The Grading Principle

> "Grade what the agent produced, not the path it took."

If 5 different correct solutions exist, your grader must accept all 5. Path-dependent grading creates false failures.

---

## Real-World Benchmark Patterns

Production benchmarks reveal design principles:

| Benchmark | Domain | Key Insight |
|-----------|--------|-------------|
| **SWE-bench Verified** | Code agents | Test suites are ground truth; 500 tasks >> 2294 unverified |
| **τ2-Bench** | Conversation | Multi-turn state tracking; turn limits prevent rambling |
| **WebArena** | Web agents | Screenshot + state inspection; must verify GUI changes |
| **OSWorld** | Computer use | File system state is proof of work |

The pattern: Verify actual state changes, not LLM claims about state changes.

---

## The Saturation Problem

> "100% pass rate means the eval only catches regressions."

**Why it matters:** You've stopped measuring improvement. The test set is too easy.

**Anthropic guidance:** Target 60-80% pass rates for active development. This leaves headroom to measure progress.

**The fix when saturated:**
1. Add harder tasks from recent failures
2. Expand to edge cases
3. Increase complexity (multi-step → long-horizon)

Evals are living artifacts. They must grow with capability.

---

## Defense in Depth

No single eval catches everything.

| Layer | Speed | Coverage | Catches |
|-------|-------|----------|---------|
| **Automated regression tests** | Fast | Narrow | Breaking changes |
| **Production monitoring** | Real-time | Broad | Unexpected real-world behavior |
| **A/B testing** | Days | Statistical | Outcome differences |
| **Transcript review** | Slow | Deep | Reasoning failures |
| **Human studies** | Very slow | Gold standard | Subjective quality |

The Swiss Cheese model: Each layer has holes. Safety comes from holes rarely aligning.

**Example composite strategy:**
```
Pre-deploy: Automated evals (regression prevention)
Post-deploy: A/B test (outcome validation)
Weekly: Transcript review (failure pattern discovery)
Quarterly: Human study (subjective quality check)
```

---

## Why These Principles

### Start Early (Step 0)

Building evals after the agent is like writing tests after shipping.

**The pattern:** 20-50 tasks from actual failures becomes your foundation. Real problems, not hypothetical ones.

### Unambiguous Tasks (Step 1)

> "If an expert would debate whether the agent succeeded, the task is poorly specified."

Vague goals create grader arguments. Evals measure grader quality, not agent quality.

### Balanced Datasets (Step 2)

Positive-only test sets let agents overfit to "always yes."

**The fix:** Include negative examples (should_not_trigger cases) to measure precision.

### Environment Isolation (Step 3)

Shared state between test runs creates hidden dependencies.

**The failure:** Test 5 passes because Test 3 created a file. Reordering breaks everything.

**The fix:** Clean environment per trial.

### Read Transcripts (Step 5)

Metrics tell you where. Transcripts tell you why.

Patterns emerge: "The agent always fails when X and Y both happen." That becomes your next test case.

### Maintain as Artifact (Step 7)

Evals decay without ownership. Tests bitrot. Benchmarks saturate.

**The fix:** Dedicated ownership. Someone responsible for keeping evals relevant.

---

## Effect Sizes That Matter

From Anthropic's production deployment research:

| Change | Impact |
|--------|--------|
| Adding behavioral evals (Bloom) | Caught alignment issues automated tests missed |
| Transcript review | Identified grader bugs in 15% of evals |
| Pass@5 vs pass@1 | 98% vs 75% apparent reliability (same model) |

The pattern: Multiple measurement modes, multiple angles, continuous refinement.

---

## The Test

For every eval you write:

1. **Does it test both failure modes?** (false positive AND false negative)
2. **Is the task unambiguous?** (would experts agree on success?)
3. **Does it measure outcome, not path?** (accepts all valid solutions)
4. **Can you explain what it catches?** (if not, it's not testing anything meaningful)
5. **Will it survive model improvements?** (or saturate immediately)

Evals that fail these questions waste time or create false confidence.

---

## The Deeper Why

Evaluation isn't about proving the agent works. It's about understanding where it doesn't—before users find out.

The goal is compounding insight: each test reveals a failure mode, each failure mode becomes a test, the suite becomes a map of how the system can go wrong.

That map is how you ship with confidence.

---

See [sources.md](sources.md) for research citations and framework documentation.
