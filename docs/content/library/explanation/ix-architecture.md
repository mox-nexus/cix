# ix + Matrix Architecture

How intelligent experimentation works: ix as a multi-agent system running on the Matrix platform.

---

## The Two Layers

**Matrix** is the platform — the agentic data plane. It owns agent execution, DAG orchestration, storage, configuration, and dependency injection.

**ix** is an experimentation tool — a multi-agent system that runs inside Matrix. It defines experiment models, components, and lifecycle. Matrix handles the rest.

```
              ix defines                      Matrix executes
    ┌─────────────────────────┐    ┌─────────────────────────────┐
    │  Experiment config      │    │  AgentRuntimePort            │
    │  Subject definitions    │───>│  DAG orchestration           │
    │  Probes (prompts)       │    │  Construct (artifact ledger) │
    │  Grader specs           │    │  Container (DI wiring)       │
    │  State machine          │    │  Config loading              │
    └─────────────────────────┘    └─────────────────────────────┘
```

---

## Matrix: The Platform

### AgentRuntimePort

The universal interface for running agents on any LLM backend:

```python
@runtime_checkable
class AgentRuntimePort(Protocol):
    async def invoke(self, system: str, messages: list[dict]) -> str: ...
```

Every component that needs an LLM gets this injected. The adapter handles the backend:

| Adapter | Backend | Maps to |
|---------|---------|---------|
| `ClaudeAdapter` | Claude SDK | `query(prompt, ClaudeAgentOptions)` |
| `GoogleADKAdapter` | Google ADK | `Runner(LlmAgent).run_async()` |
| `OllamaAdapter` | Local models | HTTP API |

Swap backends in config. Nobody else knows.

### The Agent Definition Problem

Claude SDK and Google ADK both define agents, but with different shapes:

| Concept | Claude SDK | Google ADK |
|---------|-----------|------------|
| System prompt | `system_prompt` | `instruction` |
| Model | `model: str` | `model: str` |
| Tools | `allowed_tools: list[str]` | `tools: list[ToolUnion]` |
| Sub-agents | `agents: dict` | `sub_agents: list` |
| Max turns | `max_turns: int` | `RunConfig.max_llm_calls` |
| Output format | `output_format` (JSON Schema) | `output_schema` (Pydantic) |
| Skills | `setting_sources + Skill tool` | N/A |
| Plugins | `plugins: [{type, path}]` | N/A |
| MCP servers | `mcp_servers: dict` | N/A |
| Working dir | `cwd: str` | N/A |
| Permissions | `permission_mode` | N/A |

The 8 common fields: **name, description, instruction, model, tools, sub_agents, max_turns, output_schema**.

Claude-specific but important: **skills, plugins, MCP servers**. These inject domain knowledge into the agent — critical for ix, where the Subject agent needs specific skills loaded to test activation.

### The Common Abstraction

```python
@dataclass(frozen=True)
class AgentSpec:
    """Runtime-agnostic agent definition."""
    name: str
    instruction: str = ''
    model: str = ''
    tools: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    plugins: list[str] = field(default_factory=list)
    mcp_servers: dict = field(default_factory=dict)
    cwd: str | None = None
    max_turns: int | None = None
    output_schema: dict | None = None
    runtime_config: dict = field(default_factory=dict)
```

Each adapter maps `AgentSpec` to its native API. The Claude adapter maps `instruction` to `system_prompt`, `skills` to `setting_sources` + `Skill` in `allowed_tools`. The Google ADK adapter maps `instruction` to `instruction`, ignores `skills` (or bakes them into the instruction).

### Construct and Artifacts

Matrix's data plane is the **Construct** — an append-only ledger of immutable **Artifacts**:

```python
class Artifact(BaseModel, frozen=True):
    kind: str           # "subject.response", "grader.evaluation", "scorer.row_scores"
    producer: str       # component name
    data: Any           # the actual payload
    id: str             # unique ID
    timestamp: datetime

class Construct(BaseModel, frozen=True):
    subject: str
    artifacts: tuple[Artifact, ...] = ()

    def append(self, artifact: Artifact) -> Construct:
        """Returns NEW instance with artifact added."""
        return self.model_copy(update={"artifacts": self.artifacts + (artifact,)})

    def last(self, kind: str) -> Any:
        """Get data from most recent artifact of given kind."""
        for a in reversed(self.artifacts):
            if a.kind == kind:
                return a.data
        raise KeyError(f"No artifact of kind '{kind}'")
```

Components produce data. Matrix wraps it in Artifacts. The Construct carries everything.

### Container and DI

Matrix's Container wires adapters into components:

```python
class Container:
    def __init__(self, config: MatrixConfig):
        self.runtime = ClaudeAdapter(...)  # or GoogleADKAdapter, etc.
        self.storage = DuckDBStorage(...)

    def build_component(self, name: str) -> Component:
        cls = ComponentRegistry.get(name)
        return cls(runtime=self.runtime)  # inject runtime
```

Any component that needs an LLM gets the runtime injected. The component doesn't know which backend is behind it.

---

## ix: The Experimentation MAS

### Domain Models

ix uses Pydantic v2 discriminated unions for type-safe experiment configuration:

```python
class AgentSubject(BaseModel, frozen=True):
    kind: Literal["agent"] = "agent"
    name: str
    agent_ref: str
    model: str = "claude-sonnet-4-5-20250929"
    system_prompt: str | None = None
    tools: list[str] = []
    skills: list[str] = []        # skills to load
    plugins: list[str] = []       # plugins to load

class ServiceSubject(BaseModel, frozen=True):
    kind: Literal["service"] = "service"
    name: str
    image: str
    env: dict[str, str] = {}

Subject = Annotated[Union[AgentSubject, ServiceSubject], Field(discriminator="kind")]
```

Similarly for scenarios:

```python
class CognitiveScenario(BaseModel, frozen=True):
    kind: Literal["cognitive_task"] = "cognitive_task"
    task_prompt: str
    expected: dict | None = None

class LoadScenario(BaseModel, frozen=True):
    kind: Literal["load_profile"] = "load_profile"
    tool: str = "wrk"
    duration: str = "5m"

Scenario = Annotated[Union[CognitiveScenario, LoadScenario], Field(discriminator="kind")]
```

### The Probe Is Data

A probe is a prompt. A string. The stimulus fed to the subject.

```yaml
# cases/must-001.md
---
id: must-001
expectation: must_trigger
---
How do I write evals for my Claude skill?
```

The probe does NOT execute anything. It does NOT need a runtime. It gets fed TO the subject agent via the AgentRuntime.

### Components

ix defines components that implement Matrix's Component protocol. Each component decides what goes into the Construct:

**SubjectRunner** — feeds probes to the subject via AgentRuntime:

```python
class SubjectRunner:
    def __init__(self, runtime: AgentRuntimePort):
        self.runtime = runtime

    async def run(self, construct: Construct) -> list[dict]:
        subject = construct.subject
        probes = construct.last("probes")
        results = []
        for probe in probes:
            response = await self.runtime.invoke(
                system=subject.system_prompt,
                messages=[{"role": "user", "content": probe}],
            )
            results.append({"probe": probe, "response": response})
        return results
```

**Grader (LLM-as-judge)** — evaluates responses via AgentRuntime with a rubric as system prompt:

```python
class LLMJudgeGrader:
    def __init__(self, runtime: AgentRuntimePort, rubric: str):
        self.runtime = runtime
        self.rubric = rubric

    async def run(self, construct: Construct) -> list[dict]:
        responses = construct.last("subject.responses")
        grades = []
        for entry in responses:
            grade = await self.runtime.invoke(
                system=self.rubric,
                messages=[{"role": "user", "content": entry["response"]}],
            )
            grades.append({"grade": grade})
        return grades
```

**Rule-based Grader** — no runtime needed:

```python
class ActivationGrader:
    async def run(self, construct: Construct) -> list[dict]:
        responses = construct.last("subject.responses")
        return [{"passed": "Skill" in r["response"]} for r in responses]
```

Same `AgentRuntimePort.invoke()` for both SubjectRunner and LLMJudgeGrader. Different system prompt. Different input. Same mechanism.

### Experiment State Machine

ix uses pytransitions for experiment lifecycle management:

```python
from transitions import Machine

states = ['idle', 'probing', 'sensing', 'scoring', 'reporting', 'completed', 'failed']

transitions = [
    {'trigger': 'start',         'source': 'idle',      'dest': 'probing'},
    {'trigger': 'probes_done',   'source': 'probing',   'dest': 'sensing'},
    {'trigger': 'sensors_done',  'source': 'sensing',   'dest': 'probing',
     'conditions': ['has_more_trials']},
    {'trigger': 'sensors_done',  'source': 'sensing',   'dest': 'scoring',
     'unless': ['has_more_trials']},
    {'trigger': 'scores_done',   'source': 'scoring',   'dest': 'reporting'},
    {'trigger': 'report_done',   'source': 'reporting', 'dest': 'completed'},
    {'trigger': 'fail',          'source': '*',          'dest': 'failed'},
]
```

Callbacks drive the components: `on_enter_probing` triggers SubjectRunner, `on_enter_sensing` triggers the Grader, etc.

### Experiment Configuration

```yaml
name: "Skill Activation Quality"
hypothesis: "build-eval skill activates for eval-related prompts"

conditions:
  - id: "with-skill"
    subject:
      kind: "agent"
      name: "claude-with-build-eval"
      model: "claude-sonnet-4-5-20250929"
      system_prompt: "You are a helpful assistant."
      tools: ["Skill", "Read", "Write"]
      skills: ["build-eval"]

scenario:
  kind: "cognitive_task"
  task_prompt: "How do I write evals?"
  expected:
    activated: true

graders:
  - id: "activation"
    type: "activation"
    config:
      expected_skill: "build-eval"

runs_per_condition: 5
```

---

## The Execution Flow

```
1. User runs: ix run experiment.yaml

2. ix loads config, creates experiment state machine

3. ix registers components in Matrix:
   - SubjectRunner (needs AgentRuntime)
   - Grader (needs AgentRuntime if LLM-judge, or rule-based)
   - Scorer (row-level + aggregate)
   - Reporter (console, JSON, HTML)

4. State machine drives execution:

   idle ──start──> probing
                    │
                    │  For each (probe x condition x trial):
                    │    SubjectRunner feeds probe to subject via AgentRuntime
                    │    Response appended to Construct as Artifact
                    │
                    ▼
                  sensing
                    │
                    │  For each response:
                    │    Grader evaluates (LLM-judge or rule-based)
                    │    Grade appended to Construct as Artifact
                    │
                    ▼
              ┌─ has more trials? ──> back to probing
              │
              └─ all done ──> scoring
                                │
                                │  Row scores: pass/fail per trial
                                │  Aggregate scores: F1, pass@k, Bayesian CI
                                │
                                ▼
                             reporting
                                │
                                │  Console output, JSON, HTML
                                │
                                ▼
                             completed

5. ix reads Construct, extracts results:
   intent, construct = await matrix.run(experiment)
   scores = construct.last("scorer.row_scores")
   metrics = compute_f1(scores)
```

---

## What Lives Where

| Concern | Owner | Why |
|---------|-------|-----|
| AgentRuntimePort | **Matrix** | Universal — any component can call an LLM |
| Runtime adapters | **Matrix** | Platform infrastructure, swap in config |
| StoragePort | **Matrix** | Shared persistence |
| Container (DI) | **Matrix** | Wires adapters into components |
| Orchestrator (DAG) | **Matrix** | Kind-agnostic execution |
| Construct, Artifact | **Matrix** | Core data plane types |
| Config loader | **Matrix** | Shared config strategy |
| Experiment models | **ix** | Domain-specific |
| Subject (union) | **ix** | ix domain concept |
| Probe = prompt | **ix** | Just data |
| Grader specs | **ix** | ix component config |
| State machine | **ix** | ix lifecycle (pytransitions) |
| Components | **ix** | Registered in Matrix, domain logic lives in ix |
| Scoring (F1, pass@k) | **ix** | ix domain aggregation |
| Templates | **ix** | skill-activation.yaml, methodology-rubric.yaml |
