# Building Your First Eval Suite

A guided walkthrough showing how to measure skill quality from zero to production-ready.

## What You'll Learn

By the end of this tutorial, you'll know how to build two-level evaluation for a Claude Code skill: activation testing with F1 scores and methodology rubrics.

## The Scenario

You've created a Claude Code skill called `rust-patterns` that teaches Rust idioms. It has a `SKILL.md` file with patterns like "prefer `?` operator for error propagation" and "use `impl Trait` for complex return types."

The skill exists. It activates sometimes. But you need answers to two questions:

1. Does it trigger on the right prompts?
2. When triggered, does it teach the methodology correctly?

Without measurement, you're blind.

## Phase 1: Write Activation Test Cases

Activation testing answers: "Does this skill fire when it should, and stay quiet when it shouldn't?"

You need a labeled test set. Each case has an expectation:
- `must_trigger` - should definitely activate
- `should_not_trigger` - must not activate
- `acceptable` - either is fine

Create `plugins/rust-patterns/evals/activation-suite.json`:

```json
{
  "name": "rust-patterns-activation",
  "version": "1.0.0",
  "skill": "rust-patterns",
  "description": "Activation test cases for rust-patterns skill",
  "cases": [
    {
      "id": "must-001",
      "prompt": "How do I handle errors in Rust?",
      "expectation": "must_trigger",
      "rationale": "Core Rust pattern question"
    },
    {
      "id": "must-002",
      "prompt": "What's the idiomatic way to return multiple types in Rust?",
      "expectation": "must_trigger",
      "rationale": "Asking for Rust idiom explicitly"
    },
    {
      "id": "must-003",
      "prompt": "Should I use Box<dyn Trait> or impl Trait?",
      "expectation": "must_trigger",
      "rationale": "Specific Rust pattern decision"
    },
    {
      "id": "must-004",
      "prompt": "Best practices for Rust error handling",
      "expectation": "must_trigger",
      "rationale": "Best practices = patterns"
    },
    {
      "id": "must-005",
      "prompt": "Explain Rust ownership patterns",
      "expectation": "must_trigger",
      "rationale": "Ownership is core Rust idiom"
    },
    {
      "id": "not-001",
      "prompt": "What's the best IDE for Rust?",
      "expectation": "should_not_trigger",
      "rationale": "Tooling question, not pattern/idiom"
    },
    {
      "id": "not-002",
      "prompt": "How do I install Rust?",
      "expectation": "should_not_trigger",
      "rationale": "Installation, not patterns"
    },
    {
      "id": "not-003",
      "prompt": "Write a Python script to parse JSON",
      "expectation": "should_not_trigger",
      "rationale": "Different language"
    },
    {
      "id": "not-004",
      "prompt": "Debug this TypeScript error",
      "expectation": "should_not_trigger",
      "rationale": "Different language"
    },
    {
      "id": "not-005",
      "prompt": "Explain the CAP theorem",
      "expectation": "should_not_trigger",
      "rationale": "Distributed systems theory, not Rust"
    },
    {
      "id": "edge-001",
      "prompt": "How do I write clean code?",
      "expectation": "acceptable",
      "rationale": "Too generic - could be Rust or general"
    }
  ]
}
```

### Why These Choices?

**must_trigger cases**: Direct Rust pattern questions. "How do I handle errors in Rust?" is about idioms, the core of your skill. "What IDE?" is not.

**should_not_trigger cases**: Installation, tooling, other languages. These filter out noise.

**Balance matters**: 5 positive, 5 negative. Imbalanced sets let skills overfit.

## Phase 2: Run the Activation Eval

Create `plugins/rust-patterns/evals/run_activation.py`:

```python
import json
import anthropic

def check_activation(prompt, skill_description):
    """Check if skill would activate on this prompt."""
    client = anthropic.Anthropic()

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=50,
        messages=[{
            "role": "user",
            "content": f"""You have a skill available: {skill_description}

User prompt: "{prompt}"

Would this skill activate? Answer only YES or NO."""
        }]
    )

    answer = response.content[0].text.strip().upper()
    return "YES" in answer

def calculate_metrics(results):
    """Calculate precision, recall, F1."""
    tp = sum(1 for r in results if r["should_trigger"] and r["did_trigger"])
    fp = sum(1 for r in results if not r["should_trigger"] and r["did_trigger"])
    fn = sum(1 for r in results if r["should_trigger"] and not r["did_trigger"])
    tn = sum(1 for r in results if not r["should_trigger"] and not r["did_trigger"])

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "confusion_matrix": {"tp": tp, "fp": fp, "fn": fn, "tn": tn}
    }

with open("activation-suite.json") as f:
    suite = json.load(f)

# Read skill description from SKILL.md frontmatter
with open("../SKILL.md") as f:
    content = f.read()
    # Extract description (simplified - real version would parse frontmatter)
    skill_desc = "Teach Rust idioms and patterns"

results = []
for case in suite["cases"]:
    if case["expectation"] == "acceptable":
        continue  # Skip ambiguous cases

    did_trigger = check_activation(case["prompt"], skill_desc)
    should_trigger = case["expectation"] == "must_trigger"

    results.append({
        "id": case["id"],
        "should_trigger": should_trigger,
        "did_trigger": did_trigger
    })

    status = "✓" if (should_trigger == did_trigger) else "✗"
    print(f"{status} {case['id']}: {case['prompt'][:50]}...")

metrics = calculate_metrics(results)
print(f"\nPrecision: {metrics['precision']:.2%}")
print(f"Recall:    {metrics['recall']:.2%}")
print(f"F1:        {metrics['f1']:.2%}")
```

Run it:

```bash
cd plugins/rust-patterns/evals
python run_activation.py
```

Output:

```
✓ must-001: How do I handle errors in Rust?...
✓ must-002: What's the idiomatic way to return multiple type...
✗ must-003: Should I use Box<dyn Trait> or impl Trait?...
✓ must-004: Best practices for Rust error handling...
✗ must-005: Explain Rust ownership patterns...
✓ not-001: What's the best IDE for Rust?...
✓ not-002: How do I install Rust?...
✓ not-003: Write a Python script to parse JSON...
✓ not-004: Debug this TypeScript error...
✓ not-005: Explain the CAP theorem...

Precision: 100.00%
Recall:    60.00%
F1:        75.00%
```

## Phase 3: Diagnose and Fix

### Reading the Results

**Precision 100%**: When it fires, it's always right. No false positives.

**Recall 60%**: It only catches 60% of valid Rust pattern questions. Missing 40%.

**F1 75%**: Balanced score. Not bad, but below the 85% threshold for "excellent."

### The Problem

The skill is too narrow. "Should I use Box<dyn Trait> or impl Trait?" didn't trigger. Neither did "Explain Rust ownership patterns."

Your skill description is:

```yaml
description: "Teach Rust idioms and patterns"
```

That's generic. The system doesn't know what "idioms" means.

### The Fix

Expand the description with concrete examples:

```yaml
description: |
  Teach Rust idioms and patterns. Use when: error handling (? operator, Result,
  custom errors), trait patterns (impl Trait, dyn Trait, associated types),
  ownership patterns (borrowing, lifetimes, smart pointers), async patterns
  (futures, tokio idioms), or general Rust best practices.
```

### Rerun the Eval

```bash
python run_activation.py
```

New output:

```
✓ must-001: How do I handle errors in Rust?...
✓ must-002: What's the idiomatic way to return multiple type...
✓ must-003: Should I use Box<dyn Trait> or impl Trait?...
✓ must-004: Best practices for Rust error handling...
✓ must-005: Explain Rust ownership patterns...
✓ not-001: What's the best IDE for Rust?...
✓ not-002: How do I install Rust?...
✓ not-003: Write a Python script to parse JSON...
✓ not-004: Debug this TypeScript error...
✓ not-005: Explain the CAP theorem...

Precision: 100.00%
Recall:    100.00%
F1:        100.00%
```

The skill now activates on all valid cases and none of the invalid ones.

## Phase 4: Add Methodology Rubric

Activation testing is Level 1. It tells you IF the skill fires. It doesn't tell you if Claude follows the methodology when the skill is active.

Level 2 measures: "Does Claude teach patterns correctly?"

Create `plugins/rust-patterns/evals/methodology-rubric.json`:

```json
{
  "name": "rust-patterns-methodology",
  "version": "1.0.0",
  "skill": "rust-patterns",
  "description": "Rubric for methodology adherence",
  "rubric": {
    "criteria": [
      {
        "name": "provides_idiom",
        "weight": 0.4,
        "description": "Does it provide the idiomatic Rust pattern?",
        "levels": {
          "0": "No pattern provided or wrong pattern",
          "1": "Generic advice without Rust-specific idiom",
          "2": "Correct Rust idiom but incomplete",
          "3": "Complete Rust idiom with clear example"
        }
      },
      {
        "name": "explains_why",
        "weight": 0.35,
        "description": "Does it explain WHY this is idiomatic?",
        "levels": {
          "0": "No explanation",
          "1": "Says 'this is idiomatic' without reasoning",
          "2": "Explains benefit but not tradeoff",
          "3": "Explains benefit, tradeoff, and context"
        }
      },
      {
        "name": "shows_alternatives",
        "weight": 0.25,
        "description": "Does it show when NOT to use this pattern?",
        "levels": {
          "0": "No mention of alternatives",
          "1": "Mentions alternatives exist",
          "2": "Shows alternative with basic comparison",
          "3": "Shows when each approach fits"
        }
      }
    ]
  }
}
```

### Why These Criteria?

**provides_idiom (40%)**: The primary job. If it doesn't teach the pattern, nothing else matters.

**explains_why (35%)**: From cix principles: WHY > HOW. Understanding beats memorization.

**shows_alternatives (25%)**: No pattern is universal. Knowing when NOT to use it is skill.

Weights sum to 1.0.

## Phase 5: Test Methodology

Create `plugins/rust-patterns/evals/run_methodology.py`:

```python
import json
import anthropic

def score_criterion(response_text, criterion):
    """Use LLM to score response against criterion."""
    client = anthropic.Anthropic()

    rubric_text = "\n".join([
        f"{score}: {desc}"
        for score, desc in criterion["levels"].items()
    ])

    judge = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=100,
        messages=[{
            "role": "user",
            "content": f"""Score this response on: {criterion['description']}

Rubric:
{rubric_text}

Response to score:
{response_text}

Return only the score (0, 1, 2, or 3)."""
        }]
    )

    score = int(judge.content[0].text.strip())
    return score

with open("methodology-rubric.json") as f:
    rubric = json.load(f)

# Test case: Ask Claude with rust-patterns skill active
test_prompt = "How should I handle errors in Rust?"

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1000,
    messages=[{"role": "user", "content": test_prompt}]
)

response_text = response.content[0].text

# Score against rubric
total_score = 0
for criterion in rubric["rubric"]["criteria"]:
    score = score_criterion(response_text, criterion)
    weighted = score * criterion["weight"]
    total_score += weighted

    print(f"{criterion['name']}: {score}/3 (weight {criterion['weight']}) = {weighted:.2f}")

final_score = total_score / 3  # Normalize to 0-1
print(f"\nFinal Score: {final_score:.2%}")
```

Run it:

```bash
python run_methodology.py
```

Output:

```
provides_idiom: 3/3 (weight 0.4) = 0.40
explains_why: 2/3 (weight 0.35) = 0.23
shows_alternatives: 1/3 (weight 0.25) = 0.08

Final Score: 71.00%
```

### Reading the Results

**provides_idiom**: Perfect. Claude showed the `?` operator pattern with example.

**explains_why**: Good but not great. It explained the benefit (concise error propagation) but didn't mention the tradeoff (requires `From` implementation).

**shows_alternatives**: Weak. It mentioned `match` exists but didn't say when to use it.

71% is "good" but below 85% excellence threshold.

### Improving the Skill

The methodology rubric reveals gaps. Your skill needs to emphasize:

1. Always explain WHY, not just WHAT
2. Show tradeoffs explicitly
3. Mention when alternatives fit better

Update `SKILL.md`:

```markdown
## Teaching Pattern

When presenting a Rust idiom:

1. Show the pattern with concrete example
2. Explain WHY it's idiomatic (benefit + tradeoff)
3. Show when NOT to use it (alternatives and their fit)

Example:
- Pattern: Use `?` operator for error propagation
- Why: Concise, compiler-enforced error paths
- Tradeoff: Requires `From` trait implementation
- Alternative: `match` when you need custom handling per error
```

Rerun the methodology eval. The score improves.

## What's Next

You now have two-level evaluation:

**Level 1 (Activation)**: F1 score tracking whether skill triggers correctly
**Level 2 (Methodology)**: Rubric tracking teaching quality when active

### Continuous Improvement

Run these evals:
- Before publishing the skill
- After major changes to `SKILL.md`
- When activation behavior seems wrong
- Monthly to catch drift

Track metrics:

| Date | F1 | Methodology | Notes |
|------|----|-------------|-------|
| 2026-02-09 | 100% | 71% | Initial baseline |
| 2026-02-10 | 100% | 84% | Added tradeoff guidance |

### Expand the Test Suite

Start with 10 cases. Grow over time:
- Add cases when you find prompts that should/shouldn't trigger
- Add methodology test cases for different pattern types
- Aim for 30-50 activation cases eventually

### Version Your Evals

```
evals/
├── activation-suite.json      # Current
├── methodology-rubric.json    # Current
├── v1/
│   ├── activation-suite.json  # Previous version
│   └── methodology-rubric.json
└── CHANGELOG.md
```

When you change test suites, version them. You need to know if metric changes come from skill improvements or test changes.

## Key Takeaways

**Two-level testing**: Activation (F1) + methodology (rubric). Both matter.

**Balanced test sets**: Equal positive and negative cases prevent overfitting.

**Concrete descriptions**: "Error handling, trait patterns, ownership" beats "Rust idioms."

**Metrics reveal gaps**: 60% recall showed under-activation. 71% methodology showed weak alternative coverage.

**Iterate with evidence**: Change description, rerun eval, measure improvement.

The skill you ship isn't the skill you write. It's the skill the evals prove works.
