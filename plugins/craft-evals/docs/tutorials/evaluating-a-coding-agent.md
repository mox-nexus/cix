# Evaluating a Coding Agent

A guided walkthrough showing how to measure whether a bug-fixing agent actually works.

## What You'll Learn

By the end of this tutorial, you'll understand the full evaluation lifecycle for a coding agent: designing test cases from real failures, building deterministic graders, measuring both initial performance and recovery capability, and tracking cost.

## The Scenario

You've built a coding agent that takes a GitHub issue describing a Python bug, reads the codebase, and generates a patch. Does it work? How reliably? Can it recover when it fails?

You have 25 real bugs from production to test it against.

## Phase 1: Define Tasks from Actual Failures

Don't invent hypothetical test cases. Use real bugs that cost you time.

### Create Test Cases

Each test case needs three parts:

```json
{
  "id": "auth-001",
  "input": {
    "issue": "Token expiry check fails in production. Users with expired tokens still get 200 OK.",
    "repo_path": "/path/to/repo"
  },
  "grader": {
    "type": "test_suite",
    "command": "pytest tests/test_auth.py::test_token_expiry -v"
  }
}
```

### Why Start from Failures?

Production failures give you:
- Real complexity (not toy examples)
- Known ground truth (you fixed them manually)
- Representativeness (what users actually hit)

Your first 25 cases should be bugs you've already fixed. You know the correct fix exists because you wrote it.

### Structure Your Dataset

```python
# test_cases.json
[
  {
    "id": "auth-001",
    "description": "Token expiry validation",
    "input": {
      "issue": "Token expiry check fails...",
      "repo_path": "./repos/auth-001"
    },
    "grader": {
      "type": "test_suite",
      "command": "pytest tests/test_auth.py -v"
    }
  },
  {
    "id": "db-017",
    "description": "Connection pool leak",
    "input": {
      "issue": "Database connections not released...",
      "repo_path": "./repos/db-017"
    },
    "grader": {
      "type": "test_suite",
      "command": "pytest tests/test_db.py -v"
    }
  }
  // ... 23 more cases
]
```

Each repo is a clean checkout at the commit where the bug existed. Your agent generates a patch. The grader checks if tests pass.

## Phase 2: Design Code-Based Graders

Grade what the agent produced, not the path it took.

### Test Suite Grader

The simplest and most reliable grader for code agents: run the test suite.

```python
import subprocess
import json

def grade_code_fix(agent_output, test_case):
    """
    Grade by running the test suite after applying the patch.
    """
    repo_path = test_case["input"]["repo_path"]
    patch = agent_output["patch"]

    # Apply patch
    with open(f"{repo_path}/agent.patch", "w") as f:
        f.write(patch)

    result = subprocess.run(
        ["git", "apply", "agent.patch"],
        cwd=repo_path,
        capture_output=True
    )

    if result.returncode != 0:
        return {
            "passed": False,
            "score": 0.0,
            "reason": "Patch failed to apply",
            "details": result.stderr.decode()
        }

    # Run tests
    test_cmd = test_case["grader"]["command"]
    result = subprocess.run(
        test_cmd.split(),
        cwd=repo_path,
        capture_output=True
    )

    passed = result.returncode == 0

    return {
        "passed": passed,
        "score": 1.0 if passed else 0.0,
        "reason": "Tests passed" if passed else "Tests failed",
        "details": result.stdout.decode()
    }
```

### Why Test Suites?

Deterministic, fast, and objective. No model bias. No token cost for grading.

If the tests pass, the bug is fixed. If they fail, it's not.

## Phase 3: Run with pass@5

One trial isn't enough. LLMs are stochastic. Run 5 trials per task.

### Implementation

```python
import asyncio
import json

async def run_pass_at_k(agent, test_cases, k=5):
    """
    Run k independent trials per test case.
    """
    results = []

    for case in test_cases:
        print(f"Evaluating {case['id']}...")

        trials = []
        for trial_num in range(k):
            # Clean environment for each trial
            reset_repo(case["input"]["repo_path"])

            # Run agent
            output = await agent.run(
                issue=case["input"]["issue"],
                repo_path=case["input"]["repo_path"]
            )

            # Grade
            grade = grade_code_fix(output, case)

            trials.append({
                "trial": trial_num + 1,
                "passed": grade["passed"],
                "score": grade["score"],
                "details": grade["details"]
            })

            print(f"  Trial {trial_num + 1}: {'PASS' if grade['passed'] else 'FAIL'}")

        # Calculate metrics
        successes = sum(1 for t in trials if t["passed"])
        pass_at_1 = trials[0]["passed"]
        pass_at_k = successes >= 1  # At least one success

        results.append({
            "case_id": case["id"],
            "trials": trials,
            "pass@1": pass_at_1,
            "pass@5": pass_at_k,
            "success_count": successes
        })

    return aggregate_results(results)

def aggregate_results(results):
    """Calculate overall metrics."""
    n = len(results)
    pass_1_count = sum(1 for r in results if r["pass@1"])
    pass_k_count = sum(1 for r in results if r["pass@5"])

    return {
        "total_cases": n,
        "pass@1": pass_1_count / n,
        "pass@5": pass_k_count / n,
        "results": results
    }
```

### Example Output

```
Evaluating auth-001...
  Trial 1: FAIL
  Trial 2: PASS
  Trial 3: PASS
  Trial 4: FAIL
  Trial 5: PASS

Evaluating db-017...
  Trial 1: PASS
  Trial 2: PASS
  Trial 3: PASS
  Trial 4: PASS
  Trial 5: PASS

... (23 more)

Overall Results:
├── pass@1: 60%  (15/25 cases)
├── pass@5: 92%  (23/25 cases)
└── Interpretation: Good exploration ceiling. Worth deploying with retry.
```

### What This Tells You

Pass@1 of 60% means baseline capability. Pass@5 of 92% means the agent can solve almost all bugs if you give it multiple attempts.

The gap between pass@1 and pass@5 tells you whether retry logic helps.

## Phase 4: Add Iterative Evaluation

Traditional pass@5 runs independent trials. Iterative evaluation uses failure feedback.

### Why Iterative?

If the agent gets 60% pass@1, two questions:
1. Is 60% its ceiling?
2. Can it recover if you show it the test failures?

Iterative eval answers both.

### Implementation

```python
async def iterative_eval(agent, test_case, max_iterations=3):
    """
    Run with retry and feedback.
    """
    attempts = []
    feedback = ""

    for iteration in range(max_iterations):
        # Build prompt with accumulated feedback
        prompt = f"Fix: {test_case['input']['issue']}"
        if feedback:
            prompt += f"\n\nPrevious attempt failed. Test output:\n{feedback}"

        # Run agent
        output = await agent.run(
            issue=prompt,
            repo_path=test_case["input"]["repo_path"]
        )

        # Grade
        grade = grade_code_fix(output, test_case)

        attempts.append({
            "iteration": iteration + 1,
            "passed": grade["passed"],
            "details": grade["details"]
        })

        if grade["passed"]:
            break

        # Generate feedback for next iteration
        feedback = grade["details"]

    # Calculate metrics
    passed_at = next((i+1 for i, a in enumerate(attempts) if a["passed"]), None)

    return {
        "case_id": test_case["id"],
        "pass@1": attempts[0]["passed"],
        "passed": attempts[-1]["passed"],
        "iterations_to_pass": passed_at,
        "iterations_run": len(attempts),
        "attempts": attempts
    }
```

### Run Full Iterative Eval

```python
async def full_iterative_eval(agent, test_cases, max_iterations=3):
    results = []

    for case in test_cases:
        print(f"Iterative eval: {case['id']}")
        reset_repo(case["input"]["repo_path"])

        result = await iterative_eval(agent, case, max_iterations)
        results.append(result)

        status = "PASS" if result["passed"] else "FAIL"
        iters = result["iterations_to_pass"] or "MAX"
        print(f"  {status} (iterations: {iters})")

    return aggregate_iterative(results)

def aggregate_iterative(results):
    n = len(results)

    pass_1 = sum(1 for r in results if r["pass@1"]) / n
    pass_k = sum(1 for r in results if r["passed"]) / n

    iterations = [r["iterations_to_pass"] for r in results if r["iterations_to_pass"]]
    avg_iterations = sum(iterations) / len(iterations) if iterations else None

    recovery_rate = (pass_k - pass_1) / (1 - pass_1) if pass_1 < 1 else 1.0

    return {
        "pass@1": pass_1,
        "pass@k_iterative": pass_k,
        "recovery_rate": recovery_rate,
        "avg_iterations_to_pass": avg_iterations
    }
```

### Example Output

```
Iterative eval: auth-001
  PASS (iterations: 2)
Iterative eval: db-017
  PASS (iterations: 1)
... (23 more)

Iterative Results:
├── pass@1: 60%             (baseline)
├── pass@k: 91%             (with retry + feedback)
├── recovery_rate: 78%      (78% of failures recovered)
└── avg_iterations: 1.6

Interpretation: Agent can fix 91% of bugs when given test feedback.
                Deploy with retry loop, not better prompts.
```

### Contrast: When Feedback Doesn't Help

```
Iterative Results:
├── pass@1: 60%
├── pass@k: 63%             (minimal improvement)
├── recovery_rate: 8%
└── avg_iterations: 2.9

Interpretation: Agent at capability ceiling. Retry won't help.
                Need better model or different approach.
```

This tells you retry logic won't save you. The agent needs fundamental improvements.

## Phase 5: Track Cost

Evaluation costs money. Track it.

### Token Counting

```python
import tokencost

def run_with_cost_tracking(agent, test_cases):
    results = []
    total_cost = 0.0

    for case in test_cases:
        # Count input tokens
        input_cost = tokencost.calculate_prompt_cost(
            prompt=case["input"]["issue"],
            model="claude-3-5-sonnet-20241022"
        )

        # Run agent
        output = await agent.run(case["input"]["issue"])

        # Count output tokens
        output_cost = tokencost.calculate_completion_cost(
            completion=output["patch"],
            model="claude-3-5-sonnet-20241022"
        )

        case_cost = input_cost + output_cost
        total_cost += case_cost

        results.append({
            "case_id": case["id"],
            "cost": case_cost,
            "output": output
        })

        print(f"{case['id']}: ${case_cost:.4f}")

    return {
        "results": results,
        "total_cost": total_cost,
        "avg_cost_per_case": total_cost / len(test_cases)
    }
```

### Budget for pass@k

Multiple trials multiply cost.

```python
# For pass@5
cost_per_trial = 0.08  # Average from initial run
trials = 5
cases = 25

total_cost = cost_per_trial * trials * cases
# = 0.08 * 5 * 25
# = $10.00

print(f"Budget for pass@5 eval: ${total_cost:.2f}")
```

### Set Guardrails

```python
MAX_COST_PER_CASE = 0.50  # $0.50 max per case
MAX_TOTAL_BUDGET = 15.00  # $15 total

running_cost = 0.0

for case in test_cases:
    if running_cost >= MAX_TOTAL_BUDGET:
        print(f"Budget exceeded at ${running_cost:.2f}")
        break

    case_cost = run_case_with_tracking(case)

    if case_cost > MAX_COST_PER_CASE:
        print(f"Warning: {case['id']} cost ${case_cost:.4f} > limit")

    running_cost += case_cost
```

## What's Next

You've run the full eval lifecycle:
1. Built 25 test cases from real bugs
2. Created deterministic graders
3. Measured pass@5 (exploration ceiling)
4. Measured iterative capability (recovery with feedback)
5. Tracked cost per run

### Expand the Eval Suite

Add more test cases. The SWE-bench pattern uses 500 human-validated bugs. Start with 25. Scale to 100.

### Add Model-Based Graders

Test suites measure correctness. Add graders for code quality:

```python
from deepeval.metrics import GEval

code_quality = GEval(
    name="Code Quality",
    criteria="Clean, readable, maintainable. No obvious bugs.",
    evaluation_steps=[
        "Check variable naming",
        "Check function length",
        "Check code duplication",
        "Assess readability"
    ]
)
```

### Set Up Continuous Evaluation

Run evals on every commit. Track regressions.

```yaml
# .github/workflows/eval.yml
name: Agent Eval

on: [push, pull_request]

jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run eval suite
        run: python eval/run_evals.py
      - name: Check regression
        run: python eval/check_regression.py
```

### Measure What Changed

After improvements, re-run the eval. Did pass@1 improve? Did recovery rate change? Did cost go up?

The eval suite tells you whether changes made the agent better or worse.
