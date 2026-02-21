# Domain Models

ix has a two-layer type system. Core types (`ix.domain`) are domain-agnostic — they express any experiment. Eval types (`ix.eval`) are eval-specific vocabulary that flows through the core as `Any`.

All models are frozen Pydantic `BaseModel` unless otherwise noted. Protocols use `typing.Protocol` with `@runtime_checkable`.

---

## Core Types

**Import path**: `ix.domain.types`

### `Subject`

A Subject Under Test — one variant being compared.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | `str` | required | Identifier for this subject |
| `description` | `str` | `""` | Human-readable description |
| `config` | `dict` | `{}` | Adapter-specific configuration |

### `Interaction`

One stimulus–response pair. The Probe generates a stimulus, the ExperimentRuntime executes it against the Subject, and the result lands here.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `stimulus` | `Any` | required | The input sent to the SUT (eval: `EvalCase`) |
| `trial_index` | `int` | required | Which trial this belongs to (0-indexed) |
| `observation` | `Any \| None` | `None` | What the SUT returned (eval: `EvalObservation`) |
| `error` | `str \| None` | `None` | Error message if invocation failed |

### `Reading`

Result of a sensor evaluating a single interaction. Sensors produce readings like instruments.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `sensor_name` | `str` | required | Name of the sensor that produced this reading |
| `passed` | `bool` | required | Whether this interaction passed the sensor's criteria |
| `score` | `float \| None` | `None` | Numeric score (sensor-defined semantics) |
| `metrics` | `dict` | `{}` | Additional numeric measurements |
| `details` | `str` | `""` | Human-readable explanation |

---

## Core Protocols

**Import path**: `ix.domain.ports`

All protocols are `@runtime_checkable`. Implement the methods — no base classes, no inheritance.

### `Probe`

Generates stimuli for an experiment.

| Method | Signature | Description |
|--------|-----------|-------------|
| `generate` | `() -> Iterable[Any]` | Yields stimuli (eval: `EvalCase`; benchmark: load parameters) |

### `ExperimentRuntime`

Executes a stimulus against a Subject.

| Method | Signature | Description |
|--------|-----------|-------------|
| `invoke` | `async (subject: Subject, stimulus: Any) -> Any` | Runs the stimulus, returns an observation |

### `Sensor`

Evaluates an interaction and produces readings.

| Member | Signature | Description |
|--------|-----------|-------------|
| `name` | `@property -> str` | Sensor identifier (appears in `Reading.sensor_name`) |
| `sense` | `(interaction: Interaction) -> list[Reading]` | Evaluates one interaction |

---

## Eval Models

**Import path**: `ix.eval.models`

All eval-specific types live in one file. Stimulus types (`EvalCase`, `EvalObservation`) and result types (`Verdict`, `ProbeResult`, `ExperimentResults`) are grouped together.

### `ToolCall`

A tool invocation observed in an agent response.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | `str` | required | Tool name (e.g., `"Skill"`) |
| `input` | `dict` | `{}` | Tool input arguments |

### `EvalCase`

A single eval case — the stimulus in eval vocabulary.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `id` | `str` | required | Unique identifier (e.g., `must-001`) |
| `prompt` | `str` | required | Text sent to the SUT |
| `expectation` | `str` | required | `"must_trigger"`, `"should_not_trigger"`, or `"acceptable"` |
| `rationale` | `str` | `""` | Human documentation — ignored by ix |

### `EvalObservation`

What the agent did in response to an `EvalCase` prompt.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `content` | `str` | `""` | Text response from the agent |
| `tool_calls` | `tuple[ToolCall, ...]` | `()` | Tool invocations made |
| `duration_ms` | `int` | `0` | Response time in milliseconds |
| `tokens_input` | `int` | `0` | Input token count |
| `tokens_output` | `int` | `0` | Output token count |

### `Experiment`

An eval experiment definition. Loaded from `experiment.yaml` + `cases/*.md`.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | `str` | required | Experiment identifier |
| `description` | `str` | `""` | Human-readable description |
| `subjects` | `tuple[Subject, ...]` | `()` | SUTs being compared |
| `sensor` | `str` | `"activation"` | Sensor kind to use |
| `trials` | `int` | `5` | Number of trials per case |
| `cases` | `tuple[EvalCase, ...]` | `()` | Test cases (loaded from markdown files) |

### `Verdict`

One trial of one probe: observation + sensor reading.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `probe_id` | `str` | required | Which `EvalCase.id` this trial belongs to |
| `trial` | `int` | required | Trial index (0-indexed) |
| `expectation` | `str` | required | `EvalCase.expectation` at time of run |
| `observation` | `Any` | `None` | The raw `EvalObservation` |
| `reading` | `Reading \| None` | `None` | Sensor output for this trial |

### `ProbeResult`

Aggregated result across all trials for one probe.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `probe_id` | `str` | required | Which `EvalCase.id` |
| `expectation` | `str` | required | `"must_trigger"` or `"should_not_trigger"` |
| `score` | `float` | required | Activation rate: fraction of trials that passed |
| `correct` | `bool` | required | Majority vote matches expectation |
| `trials` | `tuple[Verdict, ...]` | `()` | Individual trial verdicts |

### `ExperimentResults`

Complete results for one experiment run. Metrics and interpretation are flat fields — no nested sub-models.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `experiment_name` | `str` | required | Which experiment was run |
| `probe_results` | `tuple[ProbeResult, ...]` | `()` | Per-probe aggregated results |
| `precision` | `float` | `0.0` | TP / (TP + FP) |
| `recall` | `float` | `0.0` | TP / (TP + FN) |
| `f1` | `float` | `0.0` | Harmonic mean of precision and recall |
| `tp` | `int` | `0` | True positives |
| `fp` | `int` | `0` | False positives |
| `fn` | `int` | `0` | False negatives |
| `tn` | `int` | `0` | True negatives |
| `status` | `str` | `"pending"` | `"excellent"` (F1 >= 0.85), `"good"` (>= 0.70), `"needs_work"` (>= 0.50), `"poor"` |
| `issues` | `tuple[str, ...]` | `()` | What's wrong (e.g., `"Low recall"`) |
| `suggestions` | `tuple[str, ...]` | `()` | How to fix it |

`acceptable` cases are excluded from all counts.

---

## Eval Protocols

### `Storage`

**Import path**: `ix.eval.service`

Persistence boundary for experiments and eval results.

| Method | Signature | Description |
|--------|-----------|-------------|
| `load_experiment` | `(path: Path) -> Experiment` | Load experiment definition from directory |
| `list_experiments` | `(base: Path) -> list[Path]` | Enumerate experiment directories |
| `append_result` | `(experiment_name: str, result: Verdict) -> None` | Append one trial verdict to JSONL |
| `save_summary` | `(experiment_name: str, results: ExperimentResults) -> Path` | Write aggregate summary, return path |

---

## Type Flow

```
Probe.generate()          -> stimulus: Any (eval: EvalCase)
ExperimentRuntime.invoke() -> observation: Any (eval: EvalObservation)

Interaction(stimulus, trial_index, observation, error)
    |
Sensor.sense(interaction)  -> list[Reading]

Reading(sensor_name, passed, score, metrics, details)
    | aggregate_readings()
ProbeResult(probe_id, expectation, score, correct, trials)
    | compute_metrics() -> dict
    | interpret() -> dict
ExperimentResults(experiment_name, probe_results, precision, recall, f1, ..., status, issues, suggestions)
```
