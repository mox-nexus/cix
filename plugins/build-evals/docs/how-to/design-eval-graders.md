# How to Design Eval Graders

When you build evals, choosing the right grader determines whether your results are reliable. This guide shows you how to match grader types to task requirements.

## The Core Problem

You need to grade agent outputs, but a single approach fails. Code-based graders are fast but rigid. Model-based graders handle nuance but hallucinate. Human graders are accurate but don't scale.

The solution: layer grader types so each catches what others miss.

## Start with Code-Based Graders

Deterministic checks are fast, free, and objective. Use them first.

### When Code-Based Works

| Task Type | Grader Pattern | Example |
|-----------|---------------|---------|
| Test execution | Test suite pass/fail | `pytest` exit code = 0 |
| Format validation | Regex match | JSON parses without error |
| State verification | File exists, DB state | `assert os.path.exists(path)` |
| String matching | Exact or contains | Output includes expected phrase |

### Example: Test Suite Grader

```python
def grade_code_fix(task_id: str, generated_patch: str) -> bool:
    """SWE-bench pattern: apply patch, run tests."""

    # Apply patch to isolated environment
    repo = clone_repo(task_id)
    apply_patch(repo, generated_patch)

    # Run test suite
    result = subprocess.run(
        ["pytest", "tests/"],
        cwd=repo,
        capture_output=True,
        timeout=300
    )

    # Pass = all tests pass
    return result.returncode == 0
```

**Why this works:** Tests are the ground truth. If tests pass, the fix is correct. No interpretation needed.

### Example: State Verification

```python
def grade_file_creation(task: str, trace: dict) -> dict:
    """Grade by checking expected side effects."""

    checks = {
        "file_created": os.path.exists("/tmp/output.txt"),
        "correct_content": open("/tmp/output.txt").read() == expected,
        "no_errors": "error" not in trace["final_message"].lower()
    }

    # All must pass
    return {
        "passed": all(checks.values()),
        "details": checks
    }
```

**Anthropic's advice:** "Prefer code-based grading; fall back to model-based when necessary."

## When to Use Model-Based Graders

Open-ended outputs where deterministic checks fail.

### The Threshold Question

Can you write deterministic rules that cover 80% of valid outputs?
- **Yes** → Use code-based graders
- **No** → Use model-based graders

### When Model-Based Works

| Task Type | Why Deterministic Fails | LLM-as-Judge Pattern |
|-----------|------------------------|----------------------|
| Natural language quality | Infinite valid phrasings | Rubric with quality criteria |
| Multi-component tasks | Partial credit needed | Score per component, sum |
| Reasoning chains | Correct answer via different paths | Grade outcome, not path |

### Example: Rubric Grader

```python
RUBRIC = """
Rate the agent's research summary on a scale 0-3:

3 = Exceeds: All claims cited, synthesis insightful, sources authoritative
2 = Meets: Most claims cited, synthesis clear, sources credible
1 = Partial: Some claims cited, synthesis present but weak
0 = Fails: Few citations, no synthesis, or unreliable sources

Provide:
- Score (0-3)
- Reasoning (one sentence per criterion)
"""

def grade_research_output(input: str, output: str) -> dict:
    response = llm_judge(
        prompt=f"{RUBRIC}\n\nInput: {input}\n\nOutput: {output}"
    )

    # Parse structured response
    return {
        "score": extract_score(response),
        "reasoning": extract_reasoning(response)
    }
```

**Why explicit rubric matters:** Vague criteria ("Is it good?") produce unreliable scores. Specific criteria (citations, synthesis, sources) are reproducible.

### Example: Partial Credit

```python
def grade_multi_step_task(output: str) -> dict:
    """Each component scored independently."""

    components = {
        "gathered_data": llm_grade(output, "Did agent gather required data?"),
        "analyzed_correctly": llm_grade(output, "Is analysis methodology sound?"),
        "formatted_output": llm_grade(output, "Is output properly formatted?")
    }

    # Weighted sum
    weights = {"gathered_data": 0.4, "analyzed_correctly": 0.4, "formatted_output": 0.2}
    total_score = sum(components[k] * weights[k] for k in components)

    return {
        "score": total_score,
        "components": components
    }
```

**Trade-off:** Model-based graders are flexible but consume tokens. For high-volume evals (1000+ runs), cost adds up fast.

## When to Add Human Grading

Gold standard for subjective quality.

### The 10% Rule

You can't human-grade everything, but you can spot-check:

```python
# Randomly sample 10% of outputs for human review
sample_size = max(10, len(outputs) // 10)
human_review_set = random.sample(outputs, sample_size)

# Send to human reviewers
for output in human_review_set:
    output["human_score"] = request_human_review(output)
```

### Use Human Grading To

1. **Calibrate model-based graders**
   ```python
   # Compare human vs LLM-as-judge
   correlation = pearsonr(human_scores, llm_scores)

   # If correlation < 0.7, revise LLM rubric
   ```

2. **Catch edge cases deterministic graders miss**
   ```python
   # Code-based grader passed, but human caught subtle issue
   if human_score < 3 and code_grader_passed:
       add_to_failure_dataset(output)
   ```

3. **Validate controversial decisions**
   ```python
   # When LLM-as-judge scores vary widely (σ > 0.5), request human review
   if stdev(llm_scores) > 0.5:
       request_human_review(output)
   ```

**Cost vs value:** Human grading is expensive but catches what automated graders miss. Use it strategically, not universally.

## Combining Approaches

Best practice: layer graders in sequence.

### The Filter-Judge-Verify Pattern

```
1. Rules filter     → Fast elimination (format errors, forbidden content)
2. Model judge      → Quality assessment (nuanced criteria)
3. Human spot-check → Calibration (10% sample)
```

### Example: Layered Grading

```python
def grade_agent_output(output: str) -> dict:
    # Layer 1: Code-based filters
    if not passes_format_checks(output):
        return {"score": 0, "reason": "Format invalid"}

    if contains_forbidden_content(output):
        return {"score": 0, "reason": "Policy violation"}

    # Layer 2: LLM-as-judge for quality
    llm_score = llm_grade_quality(output)

    # Layer 3: Human review (10% sample)
    if random.random() < 0.1:
        human_score = request_human_review(output)
        log_human_vs_llm(human_score, llm_score)

    return {"score": llm_score, "grader": "llm"}
```

**Why this works:** Each layer catches different failure modes. Rules catch format errors. LLM catches quality issues. Humans catch subtle failures both miss.

## Grade the Outcome, Not the Path

Agents solve tasks differently than humans expect. Don't penalize valid alternative approaches.

### The Anti-Pattern

```python
# BAD: Requires specific tool sequence
expected_tools = ["search_flights", "compare_prices", "book_flight"]
actual_tools = ["aggregate_search", "book_flight"]  # Skipped comparison, used better tool

# This fails even though task succeeded
assert actual_tools == expected_tools  # ❌ Too rigid
```

### The Fix

```python
# GOOD: Grade outcome state
def grade_flight_booking(task: str, trace: dict) -> bool:
    # Check: was flight booked?
    booking_confirmed = "confirmation_number" in trace["final_output"]

    # Check: was it cheapest available?
    booked_price = extract_price(trace)
    cheapest_price = query_actual_cheapest(task)
    price_acceptable = booked_price <= cheapest_price * 1.1  # 10% tolerance

    return booking_confirmed and price_acceptable
```

**Anthropic's principle:** "Grade what the agent produced, not the path it took." An agent that skips expected steps but achieves the goal has succeeded.

## Validate Your Graders

Graders have bugs. Find them before they corrupt your eval results.

### Read Transcripts

Anthropic reports 15% of evals have grader bugs discovered by reading agent transcripts.

```python
# For each failed test, manually inspect:
# 1. Did grader correctly identify failure?
# 2. Or did agent actually succeed but grader failed?

for test_case in failed_cases[:20]:  # Review first 20 failures
    print(f"Task: {test_case.input}")
    print(f"Output: {test_case.output}")
    print(f"Grader reason: {test_case.grade_reasoning}")
    input("Does grader decision look correct? [Enter to continue]")
```

### Check for False Passes

More dangerous than false failures: grader passes a bad output.

```python
# Inject known-bad outputs
bad_outputs = [
    {"input": "Book flight", "output": "Error: API failed", "should_fail": True},
    {"input": "Summarize", "output": "...", "should_fail": True}  # Incomplete
]

for test in bad_outputs:
    score = grader(test["input"], test["output"])
    assert score == 0, f"Grader passed a known-bad output: {test}"
```

**If grader passes known-bad outputs, your eval results are unreliable.** Fix the grader before running full eval suite.

## Summary Checklist

Before finalizing your grader design:

- [ ] Started with code-based graders (deterministic, fast, free)
- [ ] Used model-based only where deterministic fails (open-ended quality)
- [ ] Defined explicit rubric with 0-3 scale and clear criteria
- [ ] Planned human spot-check for 10% of outputs
- [ ] Grading outcome state, not tool call sequence
- [ ] Validated grader with known-good and known-bad cases
- [ ] Read transcripts to catch grader bugs

If any box is unchecked, revisit that aspect before running evals at scale.
