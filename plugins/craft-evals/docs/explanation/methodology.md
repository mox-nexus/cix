# Eval Methodology for LLM Agents

You have an agent that writes code, calls tools, answers questions. It works. Sometimes. You ship it, users complain, you look at the output and think "why did it do that?" You tweak the prompt, things get better in one place, worse in another. You have no systematic way to know whether the last change was an improvement or a regression.

This is the problem build-eval solves: a methodology for measuring AI systems so you make informed decisions instead of guessing.

---

## Why Agent Eval is Harder Than Software Testing

Software tests have deterministic inputs and outputs. Call a function twice, get the same result. Agent eval breaks this contract in three ways.

**Non-determinism.** The same prompt produces different outputs on different runs. An agent that succeeds 7 out of 10 times looks like it "works" on a single run and looks like it "fails" on a single run. Neither observation is meaningful. You need multiple trials to see the real distribution. (Evidence: Strong -- Anthropic 2026 agent eval guide, SWE-bench methodology)

**Multi-dimensional quality.** An agent that produces correct output in 50,000 tokens is worse than one that produces correct output in 5,000 tokens. Correctness alone doesn't capture quality -- you also care about cost, latency, tool usage efficiency, and whether the agent stays within its role. Single metrics collapse this into a number that hides the tradeoffs. (Evidence: Strong -- KDD 2025 agent eval survey)

**The judge problem.** Open-ended outputs can't always be verified by code. You need a judge. But the best judges available are also LLMs, which brings their own biases: position bias, verbosity bias, self-preference. You're using the thing you're evaluating to evaluate the thing you're evaluating. The escape hatch is layering multiple judge types and calibrating against human ground truth. (Evidence: Strong -- NeurIPS 2023, "Judging LLM-as-a-Judge")

---

## The Three Grader Types

Every eval needs a grader -- something that looks at agent output and produces a score. There are exactly three kinds, and each has a clear use case.

### Code Graders

Deterministic checks: test suites pass, expected string appears, file system state matches, regex matches output format.

**Strengths:** Fast, free, objective, reproducible. No API calls, no token cost, no judge bias.
**Weakness:** Can only verify what you can specify exactly. Rejects valid alternative solutions unless you enumerate them.

Use code graders when you can define the expected outcome precisely. This is the default -- reach for code graders first. SWE-bench uses test suites as ground truth: the generated patch either makes the tests pass or it doesn't. No judgment call required.

### Model Graders

An LLM evaluates the output against a rubric or criteria. DeepEval's GEval, Braintrust's custom scorers, and RAGAS metrics all work this way.

**Strengths:** Handle open-ended outputs (explanations, creative writing, analysis). Can apply partial credit. Flexible criteria.
**Weakness:** Expensive (each grading call costs tokens), stochastic (run the same grading call twice, sometimes get different scores), and susceptible to bias.

Use model graders when the output varies legitimately and code can't distinguish good from bad. Grade the outcome, not the path -- if five different solutions are correct, the grader must accept all five.

### Human Graders

Expert review of agent outputs against a rubric.

**Strengths:** Ground truth. Catches things code and models miss. Builds intuition about failure modes.
**Weakness:** Slow, expensive, doesn't scale.

Use human graders for calibration (spot-checking 10% of outputs), for discovering new failure modes, and as the gold standard when establishing ground truth for model grader training. Not for every run.

### The Routing Decision

| Agent Type | Primary Grader | Why |
|------------|----------------|-----|
| Coding agents | Code (test suites) | Tests are deterministic ground truth |
| Tool-using agents | Code (tool call matching) | Expected tools and args are specifiable |
| Conversational agents | Model (rubric) + Code (state checks) | Response quality is subjective; resolution state is verifiable |
| Research agents | Model (groundedness, coverage) | Claim quality requires judgment |
| Skills | Code (activation F1) + Model (methodology adherence) | Trigger is binary; behavior quality is graded |

The principle: use the most deterministic grader that captures the dimension you care about. Escalate to model graders only for dimensions code can't reach. (Source: Anthropic 2026, "prefer deterministic graders")

---

## Non-Determinism: pass@k and pass^k

A single run tells you what happened once. It doesn't tell you what the agent can do.

**pass@k** answers: "If I give the agent k independent tries, does it succeed at least once?" This measures capability ceiling. An agent with 75% per-trial success has pass@3 of approximately 98%. It can almost certainly solve the problem -- it just might need a couple of attempts.

**pass^k** answers: "If I run the agent k times, does it succeed every time?" This measures production reliability. That same 75%-per-trial agent has pass^3 of approximately 42%. Fewer than half of deployments would see three consecutive successes.

Same agent, same task. One metric says 98%, the other says 42%. Neither is wrong -- they measure different things.

| Context | Use | Reasoning |
|---------|-----|-----------|
| Exploring what's possible | pass@k | One good solution is enough |
| Production deployment | pass^k | Every execution must succeed |
| Comparing models | Both | Capability AND reliability matter |

**The trap of mean accuracy.** Reporting "75% accuracy" from a single run of 100 tasks conflates capability with reliability. Run 5+ trials per task. Report the distribution, not just the mean. (Source: Anthropic 2026 eval guide, "run 5+ trials"; Anthropic statistical approach to model evals)

---

## The Iterative Pattern

Standard pass@k treats each trial as independent -- the agent doesn't see its previous failures. Real-world agents often work differently: they try, fail, get error output, and try again. The Ralph pattern measures this feedback loop.

**The question it answers:** Is 60% pass@1 the agent's ceiling, or just its first-try performance?

Consider a code agent that fixes bugs. Traditional eval: 60% success rate. But if you feed the test failures back to the agent and let it retry:

```
pass@1:          60%   (baseline)
pass@3 iterative: 91%  (with feedback from failures)
recovery_rate:    78%  (78% of first-try failures became successes)
```

This changes the deployment decision completely. You don't need a better prompt -- you need a retry loop with error feedback.

Contrast with an agent where feedback doesn't help:

```
pass@1:          60%
pass@3 iterative: 64%  (plateau)
recovery_rate:    10%
```

Same baseline performance, completely different architecture recommendation. The first agent needs a feedback loop. The second needs a better model or approach.

### Key Iterative Metrics

| Metric | Formula | What It Tells You |
|--------|---------|-------------------|
| **recovery_rate** | (pass@k - pass@1) / (1 - pass@1) | Fraction of failures that become successes with feedback |
| **iterations_to_pass** | Number of retries until success | How fast the agent learns from feedback |
| **feedback_sensitivity** | Score change per iteration | Whether guidance produces measurable improvement |
| **ceiling_score** | Max score across all iterations | Best the agent can achieve with unlimited retries |

A recovery_rate above 50% means feedback loops are worth building. Below 25% means the failures are structural -- the agent doesn't have the capability, and retrying won't create it.

(Source: Ralph pattern, ghuntley.com/ralph; Anthropic 2026 building effective agents)

---

## Cost as a First-Class Metric

A grader that costs more than the thing it's grading is broken.

Model-based graders consume tokens on every evaluation call. If you run 100 test cases across 5 trials each with an LLM judge, that's 500 grading calls. At Sonnet pricing ($3/M input, $15/M output), a verbose rubric grader can easily cost more per run than the agent outputs it's evaluating.

### What to Track

| Metric | Why |
|--------|-----|
| Cost per eval run | Budget planning -- know what a suite costs before scaling |
| Cost per success | Efficiency -- cheap failures are fine, expensive failures aren't |
| Grader cost vs agent cost | Sanity check -- grading shouldn't dominate the budget |
| Context utilization | How much of the model's context window each eval consumes |

### The Economics of Grader Selection

Code graders cost nothing to run. Model graders cost tokens per call. The routing decision from the grader section has a cost dimension: use code graders wherever possible, and reserve model graders for dimensions that genuinely require judgment.

For high-volume eval suites, consider using a cheaper model as judge (Haiku instead of Sonnet) and calibrating its scores against a small human-labeled sample. The accuracy tradeoff is usually worth the 10-20x cost reduction.

Set budget guardrails. A per-case limit ($0.50) and a per-suite limit ($50) prevent runaway costs during development. (Source: tokencost library, Anthropic pricing)

---

## Two-Sided Testing

Every capability has two ways to fail. Measuring only one side creates blind spots.

A skill that activates on every prompt has perfect recall -- it never misses a valid trigger. It also has terrible precision -- it fires on irrelevant prompts, generates noise, and trains users to ignore it.

A skill that activates only on exact keyword matches has perfect precision -- when it fires, it's always relevant. It also has terrible recall -- it misses paraphrases, synonyms, and natural-language variations of valid triggers.

F1 forces both sides into one score:

```
Precision = correct activations / total activations     ("when it fires, is it right?")
Recall    = correct activations / should-have-fired     ("when it should fire, does it?")
F1        = 2 * (Precision * Recall) / (Precision + Recall)
```

You can't game F1 by optimizing one side. High F1 requires both high precision and high recall.

This applies beyond skill activation. Any binary decision the agent makes -- call this tool or don't, flag this issue or don't, trigger this workflow or don't -- has the same two-failure-mode structure.

### Reading the Pattern

| Observation | Diagnosis | Action |
|-------------|-----------|--------|
| High recall, low precision | Fires on everything | Tighten trigger criteria, add exclusions |
| High precision, low recall | Barely fires | Broaden trigger, add intent variations |
| Both low | Fundamentally miscalibrated | Rethink the activation logic |
| Both high (F1 > 0.85) | Working well | Monitor for regression |

---

## Saturation: When Evals Stop Teaching You Things

A 100% pass rate means the eval only catches regressions. You've stopped measuring improvement because the test set is too easy.

Anthropic's guidance: target 60-80% pass rates during active development. This provides headroom to detect improvements and enough failures to analyze.

When a suite saturates:
1. Add harder tasks drawn from real production failures
2. Expand into edge cases the current suite doesn't cover
3. Increase task complexity (single-step to multi-step to long-horizon)

Evals are living artifacts. They grow with the system's capability. The moment you stop adding to them, they start decaying into regression tests. That's useful but incomplete. (Source: Anthropic 2026, "monitor saturation")

---

## Defense in Depth

No single evaluation method catches everything.

| Layer | Speed | What It Catches |
|-------|-------|-----------------|
| Automated evals (CI) | Minutes | Regressions, known failure modes |
| Production monitoring | Real-time | Unexpected behavior in the wild |
| A/B testing | Days-weeks | Statistical outcome differences |
| Transcript review | Hours | Reasoning failures, grader bugs |
| Human studies | Weeks | Subjective quality, user experience |

Each layer has holes. Automated evals miss novel failure modes. Production monitoring misses subtle quality degradation. Transcript review doesn't scale. The Swiss Cheese model: safety comes from the holes rarely aligning across layers.

A practical layering:
- **Pre-deploy:** Automated eval suite (regression gate)
- **Post-deploy:** A/B test against previous version (outcome validation)
- **Weekly:** Review 20 transcripts from lowest-scoring cases (failure pattern discovery)
- **Monthly:** Refresh test set with new production failures (suite growth)

---

## Connection to ix

build-eval teaches the methodology: what to measure, which grader to use, which metrics matter for which agent type, how to handle non-determinism and iteration.

ix is the experimentation platform that runs it.

| build-eval decides | ix handles |
|-------------------|------------|
| Which grader type (code, model, human) | Sensor protocol -- sensors implement grading logic |
| What to measure (pass@k, recovery_rate, F1) | Analysis pipeline -- aggregate_readings, compute_metrics |
| How many trials | Experiment config -- trials per probe, statistical rigor |
| Test case design | Probe definition -- stimulus + ground truth |
| What agent configurations to compare | Subject definition -- agent config as independent variable |

The skill informs the design decisions. The platform handles execution: running probes across subjects, managing trials for statistical validity, computing metrics with appropriate rigor (Bayesian for small-N, not CLT), and persisting results for comparison.

You can use the build-eval methodology without ix -- the concepts work with any eval framework. But ix operationalizes it: repeatable experiments, controlled comparisons, phased execution, persistent results.

---

## Sources

- Anthropic (2026). [Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents). Agent evaluation guide.
- Anthropic (2026). [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents). Agent design and feedback loops.
- Anthropic (2025). [Statistical Approach to Model Evals](https://www.anthropic.com/research/statistical-approach-to-model-evals). Clustering, paired differences.
- Anthropic (2025). [Bloom: Automated Behavioral Evaluations](https://alignment.anthropic.com/2025/bloom-auto-evals/). Behavioral eval framework.
- KDD 2025. [LLM Agent Evaluation Survey](https://arxiv.org/abs/2507.21504). Comprehensive taxonomy.
- NeurIPS 2023. [Judging LLM-as-a-Judge](https://arxiv.org/abs/2310.05470). Judge bias analysis.
- Ralph pattern. [ghuntley.com/ralph](https://ghuntley.com/ralph/). Iterative eval loop.
- MCPGauge (2025). [arxiv:2506.07540](https://arxiv.org/abs/2506.07540). MCP server evaluation.
- Scott Spence. [Skill activation study](https://scottspence.com/posts/how-to-make-claude-code-skills-activate-reliably). 200+ test methodology.
