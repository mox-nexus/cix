# Statistical Rigor for Architectural Decisions

When measuring whether an architectural decision worked, naive statistics will mislead you.

## The CLT Trap

The Central Limit Theorem assumes large, independent, identically distributed samples. Architectural measurements rarely satisfy any of these:

- **Small N**: You run 5-50 trials, not 10,000
- **Not independent**: Trials sharing infrastructure, prompts, or time windows are correlated
- **Not identically distributed**: LLM outputs are multimodal and skewed, not Gaussian

**Rule**: Never use Z-tests, t-tests, or naive standard errors ($\sqrt{p(1-p)/n}$) for small-N evaluations. They underestimate uncertainty by 2-3x.

**Use instead**: Bayesian credible intervals (posterior distributions). They work correctly at any sample size and make uncertainty explicit.

Source: "Don't Use the CLT for Evaluating LLMs" (ICML 2025 Spotlight)

## Clustered Standard Errors

Trials that share a prompt template, a subject, or a time window are correlated. Treating them as independent inflates your confidence.

**Rule**: Error bars must be clustered by the grouping variable (e.g., `subject_id`, `prompt_id`).

**Effect size**: Clustered SEs are typically 3x larger than naive SEs. A "significant" result often isn't once you cluster correctly.

Source: "Adding Error Bars to Evals" (Anthropic 2024)

## pass@k

For stochastic tasks (code generation, reasoning), a single trial tells you little. The right question is: "If we try k times, what's the probability of at least one success?"

**Definition**: The unbiased estimator from Chen et al. for "probability of at least 1 correct in k attempts."

**When to use**: Any evaluation where the subject's output is non-deterministic and you care about capability (not just average performance).

## Signal-to-Noise Ratio

Before trusting a benchmark, measure the benchmark itself:

- **Signal**: Variance explained by the model differences you're trying to measure
- **Noise**: Variance from infrastructure, prompt phrasing, run-to-run randomness

If noise > signal, your benchmark cannot distinguish the thing you're trying to measure. Increasing N won't fix a noisy benchmark — you need to reduce noise or increase effect size.

Source: "Signal and Noise in AI Benchmarks" (Allen AI, NeurIPS 2025)

## The Split: Row Scores vs Aggregate Metrics

| Level | What | Example | When |
|-------|------|---------|------|
| **Row score** | Per-trial pass/fail | "Did this response satisfy the rubric?" | During execution (enables fast-fail) |
| **Aggregate metric** | Distribution-level statistic | F1, pass@k, Bayesian CI, clustered SE | After all trials complete (needs full population) |

**Rule**: Never compute aggregate metrics incrementally during execution. Collect raw row scores first, persist them, then compute aggregates on the full dataset. This prevents:
- Premature conclusions from partial data
- p-hacking (recomputing aggregates with different parameters)
- Super-Sink dependencies in execution pipelines

## Ixian's Checklist

When defining validation criteria for any architectural decision:

1. **Falsifiable hypothesis** — What specific claim are we testing? What would disprove it?
2. **Noise floor** — What's the infrastructure variance? (Measure before comparing)
3. **Sample size** — Power analysis: how many trials to detect the expected effect?
4. **Clustering** — What grouping variables create correlation?
5. **Metric choice** — Row-level (fast feedback) vs aggregate (statistical rigor)
6. **Rollback criteria** — What number triggers reversal?
