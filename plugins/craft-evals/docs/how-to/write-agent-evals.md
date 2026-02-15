# How to Write Evals for an AI Agent

You built an agent. Does it work? A single pass rate tells you nothing about failure modes. This guide shows you how to write evals that measure what matters.

## The Core Problem

Activation rate is not an eval:

```python
activation_rate = 100%  # Activates on every prompt
```

This number is useless. It fires on everything, meaning it adds no signal.

Single metrics lie. An agent with 90% pass rate could be:
- Solving 90% of tasks correctly, or
- Firing on every input, getting 10% false positives you'll never see

You need to measure both failure modes: misses (recall) and noise (precision).

## Step 1: Identify Your Agent Type

Different agent types need different eval approaches.

| Agent Type | Primary Grader | Key Metrics | Example |
|------------|----------------|-------------|---------|
| **Coding** | Test suites | Tests pass, no regressions | "Add factorial function" → tests pass |
| **Conversational** | Multi-grader (state + rubric) | Resolution, tone, turn count | "Book a flight" → booking confirmed |
| **Research** | Model-based | Source quality, claim support | "Why did revenue drop?" → cited evidence |
| **Computer Use** | State inspection | GUI state, file system | "Archive emails" → folder exists, count correct |

Match your agent to the pattern. Coding agents get test suites. Conversational agents need state verification plus transcript rubrics.

## Step 2: Select Your Primary Grader

Three types, in order of preference:

### Code-Based (Preferred)

Deterministic checks: string matching, test suites, state inspection.

```python
# Coding agent: Run tests
def grade_coding_task(output):
    result = subprocess.run(["pytest"], capture_output=True)
    return result.returncode == 0

# Computer use: Check file system
def grade_file_task(expected_path):
    return os.path.exists(expected_path)
```

**When to use:** Anytime you can check the outcome deterministically. Fast, free, objective.

### Model-Based

LLM judges alignment between task and outcome.

```python
from deepeval.metrics import TaskCompletionMetric

metric = TaskCompletionMetric(threshold=0.7)
# LLM scores: "Did the agent achieve the goal?"
```

**When to use:** Open-ended tasks where outcomes vary (writing, research, conversation). Flexible but costs tokens per eval.

### Human

Expert review, crowdsourced judgment, spot-checks.

**When to use:** Gold standard for subjective quality. Expensive and slow, so use for validation, not continuous evals.

**Rule:** Start code-based. Upgrade to model-based only when deterministic checks can't capture success. Use human for spot validation.

## Step 3: Choose Metrics

Match metrics to what you're measuring.

| What You Need to Know | Metric | Formula |
|-----------------------|--------|---------|
| Does it work? | Accuracy | Correct / Total |
| Does it fire correctly? | Precision | True Positives / (TP + False Positives) |
| Does it catch everything? | Recall | True Positives / (TP + False Negatives) |
| Balance of both? | F1 | 2 × (Precision × Recall) / (P + R) |
| Can it use tools? | Tool Correctness | Expected tools called correctly |

### When to Use F1

Use F1 when you have two failure modes:

```
Agent fires → Is it relevant?  (Precision)
Should fire → Does it fire?    (Recall)
```

Example: A Rust skill should fire on Rust questions (recall) and NOT fire on Python questions (precision).

### When to Use Accuracy

Use accuracy when there's a clear right/wrong answer:

```
Task: "Add factorial function"
Success: Tests pass
Accuracy = Tasks completed / Total tasks
```

## Step 4: Build Labeled Test Cases

Start with 20-50 cases from actual failures (Anthropic's "Step 0").

### Structure

```json
{
  "id": "001",
  "input": "Fix authentication bug in auth.py",
  "expected": {
    "type": "patch",
    "file": "auth.py",
    "tests_pass": true
  },
  "labels": ["must_succeed"],
  "metadata": {
    "difficulty": "medium",
    "source": "production bug #4521"
  }
}
```

### Balance Positive and Negative

Don't just test success cases. Include both:

| Label | Tests | Measures |
|-------|-------|----------|
| `must_succeed` | Agent should complete this | Recall (misses) |
| `should_fail` | Agent should recognize this is impossible/invalid | Precision (noise) |

Example for a coding agent:

```json
[
  {"input": "Add tests for login", "label": "must_succeed"},
  {"input": "Make this faster without changing behavior", "label": "must_succeed"},
  {"input": "Fix the bug (no bug description)", "label": "should_fail"}
]
```

One-sided test sets let agents overfit. The agent that fires on everything gets 100% recall, 0% precision.

### Source from Real Usage

Don't invent hypothetical cases. Pull from:
- Production bugs that slipped through
- Support tickets
- Failed runs from development
- Edge cases discovered in code review

Real failures are higher signal than imagined ones.

## Step 5: Handle Non-Determinism

LLMs are stochastic. One run tells you nothing.

### Run Multiple Trials

Minimum 5 runs per test case. Track both:

| Metric | Formula | Question |
|--------|---------|----------|
| **pass@k** | P(at least 1 success in k trials) | One success is enough? |
| **pass^k** | P(all k trials succeed) | Needs to be reliable? |

Example: Agent has 75% per-trial success rate.

```
pass@3 = 1 - (1 - 0.75)^3 = 98%   # Exploration mode
pass^3 = 0.75^3 = 42%              # Production reliability
```

**When to use each:**
- **pass@k**: Rapid prototyping, research, one-off tasks
- **pass^k**: Production systems, customer-facing agents

### Example Implementation

```python
def eval_agent(agent, test_case, trials=5):
    results = []
    for _ in range(trials):
        output = agent.run(test_case["input"])
        success = grade(output, test_case["expected"])
        results.append(success)

    pass_at_k = any(results)
    pass_all_k = all(results)

    return {
        "pass@k": pass_at_k,
        "pass^k": pass_all_k,
        "success_rate": sum(results) / len(results)
    }
```

## Step 6: Interpret Results

Look at both failure modes.

### The Two-by-Two

```
                    ACTUAL
                    Fire    Don't Fire
              +-----------+-----------+
SHOULD   Fire |    TP     |    FN     |
             |  Correct  |  Missed   |
             +-----------+-----------+
  Don't Fire |    FP     |    TN     |
             |   Noise   |  Correct  |
             +-----------+-----------+

Precision = TP / (TP + FP)   "When it fires, is it right?"
Recall    = TP / (TP + FN)   "When it should fire, does it?"
```

### What Each Pattern Means

| Precision | Recall | Problem | Fix |
|-----------|--------|---------|-----|
| High | High | Working well | Expand dataset difficulty |
| High | Low | Too conservative | Broaden activation triggers |
| Low | High | Too aggressive | Tighten activation logic |
| Low | Low | Fundamentally broken | Redesign |

Example:

```
Rust skill results:
- Precision: 95% (fires on Rust → usually correct)
- Recall: 60% (should fire on Rust → often misses)

Diagnosis: Too conservative. Fires correctly but misses valid cases.
Action: Add more trigger examples to training data.
```

### Look at Specific Failures

Don't just look at aggregate scores. Read failed cases:

```python
for case in failed_cases:
    print(f"Input: {case['input']}")
    print(f"Expected: {case['expected']}")
    print(f"Actual: {case['actual']}")
    print(f"Why failed: {case['reason']}\n")
```

Patterns emerge: "Always fails on multi-file changes" or "Misses error handling requirements."

## Complete Example

Evaluating a coding agent:

```python
from deepeval.metrics import TaskCompletionMetric
from deepeval.test_case import LLMTestCase
import subprocess

# Test cases from production bugs
test_cases = [
    {
        "input": "Add input validation to user signup",
        "context": {"repo": "auth-service", "file": "signup.py"},
        "expected": "tests pass",
        "label": "must_succeed"
    },
    {
        "input": "Make this faster",  # Vague request
        "context": {"repo": "auth-service"},
        "expected": "clarification requested",
        "label": "should_fail"
    }
]

# Code-based grader (primary)
def grade_with_tests(output):
    result = subprocess.run(["pytest"], capture_output=True)
    return result.returncode == 0

# Model-based grader (secondary)
metric = TaskCompletionMetric(threshold=0.7)

# Run eval with 5 trials per case
results = []
for case in test_cases:
    trial_results = []
    for _ in range(5):
        output = agent.run(case["input"], case["context"])
        success = grade_with_tests(output)
        trial_results.append(success)

    results.append({
        "case": case["input"],
        "pass@5": any(trial_results),
        "pass^5": all(trial_results),
        "rate": sum(trial_results) / 5
    })

# Aggregate
total_pass_at_5 = sum(r["pass@5"] for r in results) / len(results)
total_pass_all_5 = sum(r["pass^5"] for r in results) / len(results)

print(f"Pass@5: {total_pass_at_5:.1%}")
print(f"Pass^5: {total_pass_all_5:.1%}")
```

## Summary Checklist

Before running evals:

- [ ] Agent type identified (coding, conversational, research, computer use)
- [ ] Primary grader selected (code-based preferred, model-based for flexibility)
- [ ] Metrics chosen (F1 for binary, accuracy for tasks, tool correctness)
- [ ] 20-50 test cases from actual failures
- [ ] Test set balanced (positive AND negative cases)
- [ ] Multiple trials per case (minimum 5)
- [ ] Both pass@k and pass^k tracked (if non-deterministic)
- [ ] Precision AND recall measured (not just one)
- [ ] Failed cases reviewed individually (not just aggregate score)

If any box is unchecked, your eval will miss critical failure modes.
