# Running an Experiment

Set up and run an ix experiment from scratch.

---

## 1. Create a Lab

A lab is a directory that holds experiments.

```bash
ix lab init ci-lab
```

## 2. Scaffold an Experiment

```bash
ix experiment init skill-activation --lab ci-lab
```

This creates:

```
ci-lab/
└── skill-activation/
    ├── experiment.yaml
    └── cases/              # empty, you'll add cases here
```

## 3. Configure the Experiment

Edit `experiment.yaml`:

```yaml
name: skill-activation
description: Test build-eval skill activation
skill: build-eval
trials: 5
```

`skill:` is shorthand — ix infers the subject, sensor, and evaluation pipeline from it. For full control:

```yaml
name: skill-activation
description: Test build-eval skill activation
sensor: activation
trials: 5

subjects:
  - name: build-eval
    description: The skill under test
```

## 4. Write Cases

Each case is a markdown file in `cases/` — YAML frontmatter with the expectation, body is the prompt.

**Must trigger** — skill should activate:

```markdown
---
id: must-001
expectation: must_trigger
rationale: Direct question about writing evals.
---
How do I write evals for my coding agent?
```

**Should not trigger** — skill must stay quiet:

```markdown
---
id: not-001
expectation: should_not_trigger
rationale: General coding question, no eval intent.
---
How do I sort a list in Python?
```

**Acceptable** — either outcome is fine (excluded from metrics):

```markdown
---
id: edge-001
expectation: acceptable
rationale: Ambiguous — mentions testing but not evals specifically.
---
How do I test my AI assistant?
```

File naming convention: `must-001.md`, `not-001.md`, `edge-001.md`.

## 5. Validate

```bash
ix experiment validate skill-activation --lab ci-lab
# Valid: skill-activation (28 cases)
```

## 6. Run (Mock)

Mock mode uses a local runtime that simulates tool calls. No API keys needed.

```bash
ix run skill-activation --lab ci-lab --mock
```

Add `--seed 42` for deterministic results across runs.

## 7. Run (Live)

Live mode sends prompts to Claude and observes actual behavior.

```bash
export ANTHROPIC_API_KEY=sk-...
ix run skill-activation --lab ci-lab --live
```

Override trial count from the command line:

```bash
ix run skill-activation --lab ci-lab --mock --trials 3
```

## 8. Read Results

```bash
ix results skill-activation --lab ci-lab
```

```
────────────── Results ──────────────
  Precision    100.0%
  Recall        93.3%
  F1            96.6%

Confusion Matrix:
  TP=14  FP=0
  FN=1   TN=10

Status: EXCELLENT
```

JSON output:

```bash
ix results skill-activation --lab ci-lab --format json
```

Results live in `ci-lab/skill-activation/results/`:

| File | Contents |
|------|----------|
| `trials.jsonl` | One verdict per trial, appended each run |
| `summary-latest.json` | Aggregate metrics from the most recent run |
| `summary-{timestamp}.json` | Archived snapshots |

See [Experiment Format](../reference/experiment-format.md) for the complete schema.

---

## Interpreting Results

| Metric | What It Tells You |
|--------|-------------------|
| **Precision** | Of cases that activated, how many *should* have? Low = false positives. |
| **Recall** | Of cases that *should* activate, how many did? Low = false negatives. |
| **F1** | Harmonic mean of precision and recall. The single number to watch. |

| Status | F1 Threshold |
|--------|-------------|
| Excellent | >= 0.85 |
| Good | >= 0.70 |
| Needs work | >= 0.50 |
| Poor | < 0.50 |

**Low precision?** The skill activates when it shouldn't. Tighten the skill description or add negative keywords.

**Low recall?** The skill doesn't activate when it should. Broaden the skill description or add trigger patterns.
