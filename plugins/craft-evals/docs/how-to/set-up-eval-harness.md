# How to Set Up and Run the Eval Harness

When you build an LLM skill or agent, you need empirical measurement of whether it works. This guide shows you how to run the craft-evals self-evaluation harness.

## The Core Problem

You've built the craft-evals plugin. Now you want to verify it actually works before shipping. The harness tests two questions:

1. **Activation:** Does the skill trigger on eval-related questions?
2. **Methodology:** When triggered, does Claude follow the methodology?

## Prerequisites

You need Python 3.10+ and the Anthropic SDK.

```bash
# Check Python version
python --version  # Should be 3.10+

# Install dependencies (using uv)
uv pip install anthropic

# Set API key
export ANTHROPIC_API_KEY=your-key-here
```

If you don't have `uv`, standard pip works: `pip install anthropic`

## Run the Activation Suite

This tests whether the skill triggers on the right prompts.

```bash
cd plugins/craft-evals/evals
python run_eval.py activation
```

You'll see output like:

```
Running activation eval (24 cases, 5 trials)...
  must-001: OK (rate=100%)
  must-002: OK (rate=100%)
  should-not-003: FAIL (rate=60%)  # Triggered when it shouldn't
  ...

============================================================
  ACTIVATION EVALUATION RESULTS
============================================================

Precision: 85%
Recall:    90%
F1:        87%

Confusion Matrix:
  TP=9 FP=2
  FN=1 TN=10

Status: GOOD
```

### Options

Control trials and behavior:

```bash
# More trials for stability (default: 5)
python run_eval.py activation --trials 10

# Test without API calls (mock results)
python run_eval.py activation --dry-run
```

More trials reduce variance from LLM stochasticity but cost more API calls.

## Run the Methodology Suite

This tests whether Claude follows the craft-evals methodology when activated.

```bash
python run_eval.py methodology
```

Output shows per-criterion scoring:

```
Running methodology eval (8 cases)...
  method-001: PASS (score=82%)
  method-002: FAIL (score=65%)
  ...

============================================================
  METHODOLOGY EVALUATION RESULTS
============================================================

Average Score: 78%
Pass Rate:     75%

Criterion Averages (0-3 scale):
  metric_selection: 2.5 [OK]
  failure_modes: 1.8 [WEAK]      # Needs attention
  non_determinism: 2.2 [OK]
  framework_guidance: 2.0 [OK]
  pitfall_awareness: 1.9 [WEAK]
  actionability: 2.4 [OK]

Status: GOOD

Weak Areas:
  - failure_modes
  - pitfall_awareness

Suggestions:
  - Emphasize dual failure mode thinking in core sections
  - Add more entries to the common pitfalls table
```

## Run Both Suites

```bash
python run_eval.py all
```

This runs activation first, then methodology. Use this before shipping changes to the skill.

## Interpret Results

### Activation Metrics

| Metric | Meaning | Target |
|--------|---------|--------|
| **Precision** | When skill fires, is it relevant? | 85%+ |
| **Recall** | When it should fire, does it? | 85%+ |
| **F1** | Balanced score | 85%+ |

**Status thresholds:**

| F1 Score | Status | Action |
|----------|--------|--------|
| 85%+ | Excellent | No action needed |
| 70-85% | Good | Minor tuning |
| 50-70% | Needs work | Review triggers |
| Less than 50% | Poor | Significant changes needed |

### Methodology Metrics

Scores use a weighted rubric (0-3 scale per criterion):

| Criterion | Weight | What It Tests |
|-----------|--------|---------------|
| metric_selection | 25% | Recommends appropriate metrics |
| failure_modes | 20% | Addresses precision and recall |
| non_determinism | 15% | Accounts for LLM stochasticity |
| framework_guidance | 15% | Actionable framework recommendations |
| pitfall_awareness | 15% | Warns about common traps |
| actionability | 10% | Provides concrete steps or code |

**Per-criterion thresholds:**
- 2.5-3.0: Excellent
- 2.0-2.5: OK
- 1.5-2.0: Weak (needs improvement)
- Below 1.5: Poor (urgent fix)

Weighted average above 85% = excellent, 70-85% = good.

## Add Test Cases

Test cases live in JSON files in the `evals/` directory.

### Activation Cases

Edit `activation-suite.json`:

```json
{
  "id": "must-016",
  "prompt": "How do I measure if my agent is working?",
  "expectation": "must_trigger",
  "rationale": "Direct eval question using different phrasing"
}
```

**Expectation values:**
- `must_trigger`: Should always activate
- `should_not_trigger`: Should never activate
- `acceptable`: Edge case (excluded from F1 calculation)

Balance positive and negative cases roughly 50/50.

### Methodology Cases

Edit `methodology-rubric.json`:

```json
{
  "id": "method-009",
  "prompt": "I need to evaluate my coding agent's suggestions",
  "expected_criteria": {
    "metric_selection": ["precision", "recall", "false positive"],
    "failure_modes": ["over-activation", "under-activation"]
  },
  "min_score": 0.70
}
```

The harness uses LLM-as-judge to score responses against the rubric.

## Troubleshooting

### "No module named 'anthropic'"

Install the SDK:

```bash
uv pip install anthropic
# or
pip install anthropic
```

Verify with: `python -c "import anthropic; print('OK')"`

### Inconsistent Results

LLMs are stochastic. The harness runs multiple trials and takes majority vote.

If results vary wildly:

1. Increase trials: `--trials 10`
2. Check if test cases are ambiguous
3. Use `--dry-run` to test harness logic separately

### False Positives in Activation Detection

The harness uses keyword heuristics to detect skill activation. If detection seems wrong, check `run_eval.py` around line 78 for the detection logic.

For production use, consider switching to the Claude Agent SDK approach (requires `claude_agent_sdk` package).

## What Success Looks Like

Before shipping the craft-evals plugin:

```bash
python run_eval.py all
```

Target:
- Activation F1: 85%+
- Methodology average: 85%+
- No criterion below 2.0

If you hit these thresholds, the skill is calibrated for production use.
