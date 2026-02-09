# How to Tune Skill Activation

When your skill fires on every prompt or misses the ones that matter, you need to tune its activation behavior. This guide shows you how to measure the problem and fix it.

## The Core Problem

Your skill has two failure modes:

- **False Positive (Noise)**: Activates when it shouldn't, wasting context and diluting relevance
- **False Negative (Miss)**: Doesn't activate when it should, leaving users without help

You can't see this without measurement. Raw activation rate tells you nothing.

## Step 1: Run the Activation Eval

```bash
cd plugins/build-evals/evals
python run_eval.py activation
```

This produces:

```
Precision: 75%    # When it fires, it's right 75% of time
Recall:    60%    # It catches 60% of relevant prompts
F1:        67%    # Balanced score

Status: NEEDS WORK
```

### What These Numbers Mean

| Metric | Formula | Question |
|--------|---------|----------|
| **Precision** | TP / (TP + FP) | When skill activates, is it relevant? |
| **Recall** | TP / (TP + FN) | When skill should activate, does it? |
| **F1** | 2×(P×R)/(P+R) | Balanced score |

### The Confusion Matrix

```
                    ACTUALLY TRIGGERED
                      Yes         No
                  +-----------+-----------+
SHOULD      Yes   |    TP     |    FN     |
TRIGGER           |  Correct  |  Missed   |
                  +-----------+-----------+
            No    |    FP     |    TN     |
                  |   Noise   |  Correct  |
                  +-----------+-----------+
```

## Step 2: Diagnose the Issue

Look at precision and recall together:

| Pattern | Problem | Root Cause |
|---------|---------|------------|
| High recall, low precision | Over-activating (FP > 0) | Description too broad |
| Low recall, high precision | Under-activating (FN > 0) | Description too narrow |
| Both low | Fundamental mismatch | Description unrelated to actual use |

### Example Diagnosis

```
Precision: 60%    # 40% of activations are noise
Recall:    90%    # Only missing 10% of valid cases
F1:        72%

Problem: Skill triggers too much - tighten description
```

## Step 3: Fix the Description

### For Low Precision (Over-Activation)

**Before:**
```yaml
description: "Help with testing and metrics"
```

**Problem:** This triggers on unit tests, performance benchmarks, business analytics. All noise.

**After:**
```yaml
description: "Write evals for LLM agents and AI systems. Use when: building test suites for agents, measuring agent effectiveness, evaluating multi-agent coordination. NOT for: unit tests, integration tests, performance benchmarks, business metrics."
```

**Changes:**
- Added explicit scope ("LLM agents and AI systems")
- Added exclusions to prevent false positives
- Used "Use when:" pattern for clarity

### For Low Recall (Under-Activation)

**Before:**
```yaml
description: "Write evals for LLM agents"
```

**Problem:** Misses "test suite", "metrics", "measure performance", "choose eval framework".

**After:**
```yaml
description: "Write evals for LLM agents, multi-agent systems, skills, MCP servers. Use when: building test suites, measuring effectiveness, evaluating coordination, choosing eval frameworks. Covers: DeepEval, Braintrust, RAGAS, precision, recall, F1, pass@k."
```

**Changes:**
- Broadened scope (agents, skills, MCP servers)
- Added user intent triggers ("Use when:")
- Added keyword coverage (framework names, metric terms)

### Intent-Driven, Not Tool-Centric

Wrong approach:
```yaml
# Triggers only when tool names are mentioned
description: "Use when: DeepEval, Braintrust, RAGAS"
```

Right approach:
```yaml
# Triggers on user goals
description: "Use when: building test suites, measuring agent effectiveness, choosing eval frameworks"
```

Users think in goals ("I need to test my agent"), not tools ("I need DeepEval").

## Step 4: Rebalance Test Cases

Your test suite should be 50/50 positive and negative cases.

### Check Current Balance

```bash
# Count test cases
grep "must_trigger" activation-suite.json | wc -l
grep "should_not_trigger" activation-suite.json | wc -l
```

### Add Missing Cases

If you have 20 positive, 5 negative:

```json
{
  "id": "neg-006",
  "prompt": "Run unit tests for my Python function",
  "expectation": "should_not_trigger",
  "rationale": "Unit test, not agent eval"
}
```

### Mark Ambiguous Cases

For borderline prompts:

```json
{
  "id": "edge-001",
  "prompt": "Explain F1 score",
  "expectation": "acceptable",
  "rationale": "Could be educational or eval-related"
}
```

Marking as `acceptable` excludes them from F1 calculation.

## Step 5: Iterate

After making changes, re-run the eval:

```bash
# Before changes
python run_eval.py activation > before.txt

# Edit description in SKILL.md

# After changes
python run_eval.py activation > after.txt

# Compare
diff before.txt after.txt
```

Track progress over time:

| Date | Precision | Recall | F1 | Change |
|------|-----------|--------|-----|--------|
| 2026-02-01 | 60% | 90% | 72% | Initial |
| 2026-02-05 | 85% | 88% | 86% | Tightened description |
| 2026-02-09 | 90% | 85% | 87% | Added exclusions |

## Thresholds

| F1 Score | Interpretation | Action |
|----------|----------------|--------|
| 85%+ | Excellent | No action needed |
| 70-85% | Good | Minor tuning |
| 50-70% | Needs work | Review triggers |
| <50% | Poor | Significant changes needed |

## What Good Looks Like

**Before tuning:**
```
Description: "Write evals"

Precision: 55%
Recall:    95%
F1:        70%

Problem: Triggers on "write tests", "measure performance", "unit test coverage"
```

**After tuning:**
```
Description: "Write evals for LLM agents, multi-agent systems, skills. Use when: building test suites, measuring agent effectiveness, evaluating coordination. NOT for: unit tests, integration tests, business metrics."

Precision: 90%
Recall:    88%
F1:        89%

Improvement: Eliminated unit test noise, still catches eval questions
```

## When to Stop Tuning

Stop when one of these is true:

1. F1 score is 85% or higher
2. Improvement is less than 2% per iteration
3. Changes start hurting one metric to help the other

Perfect is the enemy of good. At 85% F1, your effort is better spent elsewhere.

