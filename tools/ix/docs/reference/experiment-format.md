# Experiment Format

Experiments live on disk as a directory: one YAML config, markdown case files, and a results directory written by ix.

---

## Directory Structure

```
<lab>/
└── <experiment-name>/
    ├── experiment.yaml       # Experiment configuration
    ├── cases/                # Test cases as markdown files
    │   ├── must-001.md
    │   ├── must-002.md
    │   ├── not-001.md
    │   └── edge-001.md
    └── results/              # Output directory (created by ix on first run)
        ├── trials.jsonl                  # One verdict per line, appended each run
        ├── summary-20260218T143022Z.json # Timestamped archive
        └── summary-latest.json           # Always the most recent run
```

A lab is any directory containing at least one experiment subdirectory. `ix` auto-detects the lab by walking up from the current working directory.

---

## experiment.yaml

### Minimal

```yaml
name: skill-activation
description: Test build-eval skill activation
skill: build-eval
trials: 5
```

The `skill:` field is shorthand. ix infers the full activation evaluation pipeline from it:

- `EvalProbe` generates cases from `cases/*.md`
- `EvalRuntime` wraps `MockRuntime` or `ClaudeRuntime` and parses tool calls
- `ActivationSensor` checks whether the named skill was invoked
- Scorer computes pass/fail per case via majority vote across trials

### Full

```yaml
name: skill-activation
description: Test build-eval skill activation
sensor: activation
trials: 5

subjects:
  - name: build-eval
    description: The skill under test
    config: {}

cases:
  suite: cases/
```

### Fields

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `name` | string | yes | | Experiment identifier |
| `description` | string | no | `""` | Human-readable description |
| `skill` | string | no | | Shorthand: sets subject name and implies activation pipeline |
| `subjects` | list | no | `[]` | Explicit list of subjects under test |
| `sensor` | string | no | `"activation"` | Sensor type to use |
| `trials` | integer | no | `5` | Number of trials per case |

`skill` and `subjects` are mutually exclusive. If neither is set, ix derives the subject name from the experiment directory name.

The default trial count can be overridden at the command line with `--trials N`. The environment variable `IX_DEFAULT_TRIALS` sets a global default.

---

## Case Markdown Files

Each file in `cases/` is a test case: YAML frontmatter specifying behavior expectations, followed by the prompt text.

```markdown
---
id: must-001
expectation: must_trigger
rationale: Direct question about writing evals should always trigger the skill.
---
How do I write evals for my coding agent?
```

### Frontmatter Fields

| Field | Required | Values | Description |
|-------|----------|--------|-------------|
| `id` | yes | string | Unique identifier within the experiment |
| `expectation` | yes | see below | Expected behavior |
| `rationale` | no | string | Human documentation — ignored by ix |

If `id` is omitted, ix uses the filename stem (e.g., `must-001`).

### Naming Convention

File names follow `{expectation_prefix}-{number}.md`:

| Prefix | Expectation | Example |
|--------|-------------|---------|
| `must-` | `must_trigger` | `must-001.md` |
| `not-` | `should_not_trigger` | `not-003.md` |
| `edge-` | `acceptable` | `edge-002.md` |

Numbers are zero-padded to three digits. Gaps are allowed (`must-001`, `must-003` with no `must-002`).

### Expectations

| Value | Meaning | Scoring |
|-------|---------|---------|
| `must_trigger` | Skill MUST activate. FN if it doesn't. | Contributes to recall |
| `should_not_trigger` | Skill must NOT activate. FP if it does. | Contributes to precision |
| `acceptable` | Either outcome is valid. | Excluded from F1 entirely |

`acceptable` cases are skipped before trials run — they never reach the sensor. Use them to document ambiguous prompts without affecting metrics.

### Case Body

The markdown body is the prompt text sent verbatim to the subject under test. Plain text or markdown. No length limit, but single-turn only.

---

## Results Format

### trials.jsonl

One JSON object per line. ix appends to this file; each `run` adds `(cases × trials)` lines.

```json
{"probe_id": "must-001", "trial": 0, "expectation": "must_trigger", "observation": {"content": "...", "tool_calls": [{"name": "Skill", "input": {"skill": "build-eval"}}], "duration_ms": 1234, "tokens_input": 0, "tokens_output": 0}, "reading": {"sensor_name": "activation", "passed": true, "score": 1.0, "metrics": {}, "details": ""}}
```

Field reference:

| Field | Type | Description |
|-------|------|-------------|
| `probe_id` | string | Case ID from frontmatter |
| `trial` | integer | Trial index, 0-based |
| `expectation` | string | Expectation value from the case file |
| `observation` | object | Raw agent response (content, tool_calls, timing, tokens) |
| `reading` | object | Sensor output: `passed`, `score`, `sensor_name`, `metrics`, `details` |

### summary-latest.json

Written at the end of each run. Also archived as `summary-{timestamp}.json` where timestamp is UTC in `YYYYMMDDTHHMMSSz` format.

```json
{
  "experiment_name": "skill-activation",
  "probe_results": [
    {
      "probe_id": "must-001",
      "expectation": "must_trigger",
      "score": 0.8,
      "correct": true,
      "trials": []
    }
  ],
  "metrics": {
    "precision": 1.0,
    "recall": 0.933,
    "f1": 0.966,
    "tp": 14,
    "fp": 0,
    "fn": 1,
    "tn": 10
  },
  "interpretation": {
    "status": "excellent",
    "issues": [],
    "suggestions": []
  }
}
```

#### probe_results

One entry per case (excluding `acceptable` cases). `score` is the activation rate across trials — fraction of trials where the sensor passed. `correct` is the majority vote: `score > 0.5` must match the expectation.

| Field | Type | Description |
|-------|------|-------------|
| `probe_id` | string | Case identifier |
| `expectation` | string | `must_trigger` or `should_not_trigger` |
| `score` | float | Fraction of trials where sensor passed (0.0–1.0) |
| `correct` | bool | Whether majority vote matches expectation |

#### metrics

Standard binary classification. Only `must_trigger` and `should_not_trigger` cases contribute.

| Field | Description |
|-------|-------------|
| `precision` | TP / (TP + FP) — of cases that activated, how many should have? |
| `recall` | TP / (TP + FN) — of cases that should activate, how many did? |
| `f1` | Harmonic mean of precision and recall |
| `tp` | `must_trigger` cases where majority vote activated |
| `fp` | `should_not_trigger` cases where majority vote activated |
| `fn` | `must_trigger` cases where majority vote did not activate |
| `tn` | `should_not_trigger` cases where majority vote did not activate |

#### interpretation

| Status | Condition |
|--------|-----------|
| `excellent` | F1 >= 0.85 |
| `good` | F1 >= 0.70 |
| `needs_work` | F1 >= 0.50 |
| `poor` | F1 < 0.50 |

`issues` and `suggestions` are populated when precision < 0.8 or recall < 0.8.

---

## Lab Resolution

`ix` resolves the lab in this order:

1. `--lab <name>` flag — searches from project root (nearest `.git` or `pyproject.toml`)
2. Walk up from `cwd` — if any ancestor directory contains experiment subdirectories, use it

A directory qualifies as a lab if it contains at least one child directory with an `experiment.yaml` file.
