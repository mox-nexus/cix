# What is ix?

## An experiment, running

You have an agent that picks which tool subcommand to call based on a natural language request. Six subcommands, overlapping semantics. You changed the documentation in the system prompt from terse `--help` text to structured skill-format guidance. Did it help?

Here is what that question looks like as an ix experiment:

```
ci-lab/cep-003-skills-vs-references/
├── experiment.yaml          # 4 subjects, tool-usage sensor, 25 trials
├── tasks/
│   ├── el-001.md            # "I think the artifact ID was something like auth-decision..."
│   ├── lt-001.md            # "Starting from artifact api-design-v1, what followed?"
│   └── ...                  # 25 probes targeting 5 ambiguous command boundaries
└── subjects/
    ├── skill-rich.md        # Structured "when to use" guidance
    ├── skill-minimal.md     # Skill structure, stripped of decision heuristics
    ├── reference-rich.md    # CLI help format, with decision heuristics added
    └── reference-minimal.md # Standard --help output
```

```bash
ix run cep-003-skills-vs-references --lab ci-lab
```

ix sends each of the 25 probes to each of the 4 subjects, 25 times each. That is 2,500 agent invocations. For every invocation, a sensor checks whether the agent called the right subcommand with reasonable arguments. After all trials complete, ix aggregates: per-probe accuracy, per-boundary accuracy, factorial contrasts, credible intervals.

The output is numbers you can compare, reproduce, and act on. Not "it seemed to work better."

That is what ix does. The rest of this document explains why it is built the way it is.

---

## Why ad-hoc evaluation fails for agents

Three properties of agent systems break informal testing:

**Non-determinism.** The same prompt produces different outputs on different runs. Ask an agent to pick `locate` versus `trace` five times and you might get 3/5, then 4/5, then 2/5. A single run tells you almost nothing. You need repeated trials and aggregation to distinguish signal from stochasticity. (Evidence level: Strong -- this is a well-established property of LLM sampling.)

**Multi-dimensional quality.** An agent can get the right tool but wrong arguments. It can get the right answer for the wrong reason. A binary pass/fail misses the structure. You need grading that decomposes quality into the dimensions you actually care about -- command selection accuracy separate from argument quality, activation precision separate from recall.

**Compositional complexity.** Real agent behavior depends on system prompt, model choice, available tools, and temperature interacting simultaneously. Changing one variable and eyeballing the output confounds everything. You need controlled comparison: same probes, same trials, different subjects. A 2x2 factorial design that can separate format effects from content effects, because the interaction might be what matters.

ix provides the structure to handle all three. Repeated trials with aggregation. Multi-dimensional sensors. Controlled multi-subject comparison.

---

## The four primitives

Everything in ix is built from four types. They live in `ix.domain.types` and carry no eval-specific assumptions -- they express any experiment.

**Probe** -- the stimulus. An id, a prompt, and a metadata dict.

```python
class Probe(BaseModel, frozen=True):
    id: str
    prompt: str
    metadata: dict = {}
```

The probe does not carry an "expectation" field. Ground truth goes in metadata, and the sensor decides how to interpret it. A probe for skill-activation puts `expectation: must_trigger` in metadata. A probe for code generation puts `test_cases` and `function_name`. A probe for tool-usage puts `expected_command` and `expected_args`. The probe is the stimulus; the sensor owns the judgment.

This separation matters. The same probe can mean different things to different sensors. An `ActivationSensor` checks whether a skill fired. A `FunctionTestSensor` extracts code and runs test cases. A `DeepEvalSensor` measures answer relevancy. They all receive the same Trial object -- they just read different keys from the metadata they were configured with at construction.

**Subject** -- the thing being tested. A name and a config dict.

```python
class Subject(BaseModel, frozen=True):
    name: str
    description: str = ""
    config: dict = {}
```

A subject is pure identity. It holds a system prompt, runtime configuration (which model, how many turns, what tools are available), and any other properties that define one variant. In a 2x2 experiment, you have four subjects. In an A/B test, two. The subject does not know how to run itself -- it is data, not behavior.

**Trial** -- one execution of a probe against a subject.

```python
class Trial(BaseModel, frozen=True):
    probe_id: str
    trial_index: int
    response: Any = None
    error: str | None = None
```

A trial pairs a probe identity with what the agent returned. If the agent raised an exception, `error` captures it and `response` stays `None`. The sensor gets the trial; it never sees the original probe directly. It looks up ground truth by `probe_id` using a registry it was given at construction time.

**Reading** -- the result of a sensor measuring a trial.

```python
class Reading(BaseModel, frozen=True):
    sensor_name: str
    probe_id: str
    trial_index: int
    passed: bool
    score: float | None = None
    metrics: dict = {}
    details: str = ""
```

A reading is what an instrument produces. `passed` is the binary judgment. `score` is the continuous signal. `metrics` holds decomposed measurements (tests_passed, tests_failed). `details` is the human-readable explanation. Every reading traces back to its trial via `probe_id` and `trial_index`, enabling joins and aggregation downstream.

These four types are frozen Pydantic models. Immutable, serializable, no behavior attached. The experiment produces a stream of readings; analysis is just grouping and counting.

---

## The inner DAG

Each probe-trial iteration runs as a four-node directed acyclic graph:

```
ProbeNode ──┐
            ├──▶ TrialNode ──▶ SensorNode
SubjectNode ┘
```

This is a DAG, not a pipeline. ProbeNode and SubjectNode have no dependency on each other -- they can run concurrently. TrialNode depends on both. SensorNode depends on TrialNode. The topology is declared through `consumes` and `produces` sets on each node:

| Node | Consumes | Produces |
|------|----------|----------|
| ProbeNode | nothing | `probe.stimulus` |
| SubjectNode | nothing | `subject.config` |
| TrialNode | `probe.stimulus`, `subject.config` | `trial.observation` |
| SensorNode | `trial.observation` | `sensor.reading` |

TrialNode is where agent execution happens. It reads the subject's runtime config, resolves an agent from a ComponentRegistry (e.g., `matrix.agent.claude` or `matrix.agent.mock`), calls `agent.run(prompt)`, and wraps the response in a Trial. If the agent fails, the Trial captures the error. Either way, SensorNode gets a Trial to measure.

SensorNode delegates to the Sensor protocol. If the trial has an error, it produces a failed reading without calling the sensor. If the sensor itself throws, it catches the exception and produces a failed reading with the error message. Failures propagate as data, not as exceptions that abort the experiment.

The DAG runs on Matrix's Orchestrator. Matrix is the Agentic Data Plane -- it provides the agent runtimes, the component registry, and the DAG execution engine. ix provides the experiment semantics: what to test, how to grade, how to aggregate. The dependency is one-way: ix depends on Matrix. Matrix knows nothing about experiments or sensors.

---

## Sensors: why "sensor" and not "grader"

A sensor is an instrument that measures a trial and produces readings. The `measure()` protocol:

```python
@runtime_checkable
class Sensor(Protocol):
    @property
    def name(self) -> str: ...
    def measure(self, trial: Trial) -> list[Reading]: ...
```

The name "sensor" comes from the instrumentation metaphor. A grader implies a single correct answer and a binary judgment. A sensor implies measurement -- it can produce continuous scores, multiple metrics, partial credit. The `ToolUsageSensor` gives 1.0 for right command and right args, 0.5 for right command but wrong args, 0.0 for wrong command. That is measurement, not grading.

ix ships four sensors:

**ActivationSensor** -- did the agent invoke the expected tool? Expectation-aware: a `should_not_trigger` probe that correctly stays silent scores `passed=True`. Deterministic, fast, no API calls.

**FunctionTestSensor** -- extracts code from the agent's response, loads it into an isolated module, runs test cases with a timeout. Returns `score = tests_passed / tests_total`. Ground truth (function name, test cases) is injected at construction from probe metadata.

**ToolUsageSensor** -- checks subcommand selection and argument quality. Two-tier scoring. Used in the CEP-003 experiment described above.

**DeepEvalSensor** -- wraps any DeepEval metric (answer relevancy, faithfulness, hallucination, bias, toxicity, GEval) as an ix sensor. When a judge agent is provided, LLM grading calls route through Matrix's Agent protocol, making grading costs observable.

Multiple sensors compose via `CompositeSensor`, which runs N sensors and flattens the readings. One experiment, measured from multiple angles. The experiment config declares which sensors to use:

```yaml
sensors:
  - type: activation
    expected_skill: build-eval
  - type: deepeval
    metric: answer_relevancy
    threshold: 0.7
```

Ground truth is injected into each sensor at construction time by the composition layer, not discovered from the probe at measurement time. The sensor receives a registry of `probe_id -> ground_truth` and looks up what it needs when `measure()` is called. This keeps the Sensor protocol clean: `measure(trial) -> list[Reading]`, nothing else.

---

## The experiment loop

The `Experiment` class ties it together. It receives infrastructure (registry, sensor, store) at construction and executes the full matrix when `run()` is called:

```
for probe in config.probes:
    for trial_index in range(config.trials):
        readings += run_trial(probe, subject, sensor, registry, trial_index)
```

This is the outer loop. Each `run_trial` invocation builds and runs the inner DAG described above. The cross-product of probes and trials produces the complete observation matrix.

After the loop, two pure functions aggregate:

1. **`aggregate_readings`** -- groups readings by `probe_id`, computes pass rate per probe, produces a `ProbeResult` for each. A probe passes if more than half its trials passed (majority vote).

2. **`compute_metrics`** -- takes the list of `ProbeResult`s, computes `pass_rate` (fraction of probes that passed), `mean_score` (mean of continuous per-probe scores), `min_score`, `max_score`.

The final `ExperimentResults` carries provenance: a hash of the config, the run timestamp, and the ix version. Status is a `@computed_field` derived from pass_rate -- not a separate interpretation layer. The numbers speak: >= 1.0 is "excellent", >= 0.85 is "good", >= 0.50 is "needs_work", below is "poor".

---

## What ix is not

**ix is not a test framework.** pytest asserts deterministic expectations. Agent outputs are stochastic. ix runs N trials and aggregates, because a single assertion on a non-deterministic system is noise.

**ix is not a benchmark suite.** Benchmarks provide standardized tasks and leaderboards. ix provides the experiment structure -- you bring your own probes, your own subjects, your own sensors. ix does not rank models against each other on a canonical task set. It helps you answer YOUR questions about YOUR agents.

**ix is not a CI pipeline.** It can feed a CI pipeline (the exit code reflects pass/fail), but the core value is the experiment: controlled comparison, repeated trials, multi-dimensional measurement. CI is one consumer of experiment results. Research is another. Debugging is a third.

ix is an experimentation platform. The distinction matters because it shapes the design: probes are not assertions, sensors are not test fixtures, subjects are not mocks. They are the vocabulary of structured experimentation applied to agent systems.

---

## What you write

An experiment is a directory with three parts:

1. **`experiment.yaml`** -- name, sensors, trial count, subject references
2. **`tasks/*.md`** -- one probe per file, YAML frontmatter for id and metadata, prompt as body
3. **`subjects/*.md`** -- one subject per file, YAML frontmatter for name and runtime config, system prompt as body

No Python required to define an experiment. The file format is the interface. Version-control your experiments, diff them, review them. Start with `--mock` to validate structure before spending API budget.

```bash
ix run my-experiment --lab ci-lab --mock    # Dry run, no API calls
ix run my-experiment --lab ci-lab           # Real run
ix results my-experiment --lab ci-lab       # View results
```

---

## The composition root

One question the architecture must answer: who wires concrete implementations together? The composition root (`ix.composition`) does this once, at startup. It builds a unified `ComponentRegistry` that resolves both agent runtimes (`matrix.agent.claude`, `matrix.agent.mock`) and sensors (`ix.sensor.activation`, `ix.sensor.function-test`) through the same `type_url -> factory` pattern.

The `Experiment` class never imports a concrete node class or agent implementation. It receives a `run_trial` callable from the composition root -- a closure that knows how to build the inner DAG from concrete components. This inversion means the experiment loop is testable in isolation, mock mode works by swapping one registry entry, and new agent runtimes or sensor types plug in without touching the experiment code.

---

## Status: alpha

ix 0.0.1-alpha means the core loop works and real experiments have run (CEP-002, CEP-003). The sensor protocol, the file format, and the CLI commands are stable. Internal model field names may change.

Known gaps: no built-in statistical significance testing (Bayesian methods are documented in experiment proposals but not automated), no pass@k metric, no load-testing sensor. The architecture supports all three -- the Sensor protocol generalizes -- but they do not exist yet.

If you are evaluating ix: run an experiment in `ci-lab/`. The structure there is what the file format looks like. If it fits your use case, ix is worth trying.
