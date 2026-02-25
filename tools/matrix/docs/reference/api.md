# API Reference

All public types exported from `matrix`.

---

```python
from matrix import (
    Artifact,
    CompilationError,
    Component,
    ComponentRegistry,
    Config,
    Construct,
    DagCompiler,
    DagScheduler,
    MatrixConfig,
    Orchestrator,
)
```

## Core Types

### `Component` (Protocol)

The contract every DAG node must satisfy. Structural typing — no import required.

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Unique identifier within a DAG |
| `requires` | `frozenset[str]` | Artifact kinds this component reads |
| `provides` | `str` | Artifact kind this component produces |

| Method | Signature | Description |
|--------|-----------|-------------|
| `run` | `async (Construct) -> Any` | Read upstream artifacts, do work, return data |

```python
class MyComponent:
    name = "my-component"
    requires = frozenset({"upstream.data"})
    provides = "my-component.output"

    async def run(self, construct):
        data = construct.last("upstream.data")
        return process(data)
```

### `Artifact`

Immutable fact produced by a component. Dataclass, frozen.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `kind` | `str` | required | Artifact type (matches component's `provides`) |
| `producer` | `str` | required | Name of the component that created it |
| `data` | `Any` | required | The actual value |
| `id` | `str` | auto (uuid hex) | Unique identifier |
| `created_at` | `float` | auto (monotonic) | Creation timestamp |

### `Construct[S]`

Append-only ledger of Artifacts. Generic over subject type `S`. Dataclass, frozen.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `subject` | `S` | required | What's being tested/processed |
| `ledger` | `tuple[Artifact, ...]` | `()` | Ordered artifacts |

| Method | Signature | Description |
|--------|-----------|-------------|
| `append` | `(Artifact) -> Construct[S]` | Return new Construct with artifact added |
| `last` | `(kind: str) -> Any` | Data from most recent artifact of `kind`. Raises `LookupError` |
| `all` | `(kind: str) -> tuple[Artifact, ...]` | All artifacts matching `kind`, in order |
| `kinds` | `() -> frozenset[str]` | Set of all artifact kinds in the ledger |

---

## Orchestration

### `Orchestrator`

Compiles and executes a DAG of components.

```python
orch = Orchestrator([probe, sensor, scorer])
construct = await orch.run("my-subject")
```

| Method | Signature | Description |
|--------|-----------|-------------|
| `__init__` | `(components: list[Any])` | Compile topology from component list |
| `run` | `async (subject: S) -> Construct[S]` | Execute DAG, return Construct with all artifacts |

`__init__` calls `DagCompiler.compile()` — topology errors surface immediately.

### `DagCompiler`

Static topology validation. Call directly when you need edges without execution.

```python
registry, edges = DagCompiler.compile([probe, sensor, scorer])
# registry: {"probe": <Probe>, "sensor": <Sensor>, "scorer": <Scorer>}
# edges: {"probe": set(), "sensor": {"probe"}, "scorer": {"sensor"}}
```

| Method | Signature | Description |
|--------|-----------|-------------|
| `compile` | `(components: list) -> tuple[dict, dict]` | Validate and return (registry, edges) |

Raises `CompilationError` on:
- Missing producer (component requires a kind nobody provides)
- Duplicate output kind (two components provide the same kind)
- Duplicate component name
- Cycle in the dependency graph

### `DagScheduler`

Yields topological execution batches. Components within a batch are independent.

```python
scheduler = DagScheduler(registry, edges)
for batch in scheduler.batches():
    # batch is a tuple of components
    for component in batch:
        ...
```

| Method | Signature | Description |
|--------|-----------|-------------|
| `__init__` | `(registry: dict, edges: dict)` | Accept compiled topology |
| `batches` | `() -> Iterator[tuple[Any, ...]]` | Yield batches in topological order |

### `CompilationError`

Exception raised by `DagCompiler.compile()` when topology validation fails.

---

## Configuration

Matrix provides a config composition system. Each consumer (ix, memex, radix) defines its own config model. Matrix provides the platform config and the loading/merging utilities.

### `MatrixConfig`

Platform settings Matrix owns. Frozen Pydantic model.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `runtime.model` | `str` | `"claude-sonnet-4-5-20250929"` | Default model |
| `runtime.max_tokens` | `int` | `2048` | Default max tokens |

### `Config[C]`

Composes Matrix platform settings with one client's settings. Each consumer gets its own `Config[C]`.

```python
from matrix import load_config, Config, MatrixConfig
from pydantic import BaseModel, ConfigDict

# Each consumer defines what it needs
class IxConfig(BaseModel):
    model_config = ConfigDict(frozen=True)
    default_trials: int = 5

# Load from YAML — matrix section shared, client section per-consumer
config = load_config(IxConfig, client_key="ix")
config.matrix.runtime.model    # "claude-sonnet-4-5-20250929"
config.client.default_trials   # 5
```

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `matrix` | `MatrixConfig` | defaults | Platform-level settings |
| `client` | `C` | required | Client-provided Pydantic model |

### `load_config`

Reads YAML sources, merges tiers, validates both sections.

```python
config = load_config(
    client_type=IxConfig,      # Pydantic model for client section
    client_key="ix",           # YAML key (required)
    sources=[Path("ix.yaml")], # Optional — defaults to 3-tier discovery
)
```

3-tier discovery (when `sources` is omitted):
1. Pydantic model defaults (no file)
2. User-level: `~/.{client_key}/config.yaml`
3. Project-level: `./{client_key}.yaml`

Later tiers override earlier ones. `deep_merge` handles nested dicts.

### Multi-consumer YAML

One YAML file can serve multiple consumers. Each reads its own section:

```yaml
matrix:
  runtime:
    model: claude-sonnet-4-5-20250929
ix:
  default_trials: 5
memex:
  chunk_size: 512
```

```python
ix_config    = load_config(IxConfig, "ix")       # reads matrix: + ix:
memex_config = load_config(MemexConfig, "memex")  # reads matrix: + memex:
```

Both share the same `matrix:` section. Each gets its own client section.

---

## Component Registry

### `ComponentRegistry`

Type URL to factory mapping. For Container-based DI.

```python
registry = (
    ComponentRegistry()
    .register("app.probe", make_probe)
    .register("app.sensor", make_sensor)
)

component = registry.create("app.probe", {"name": "custom"})
```

| Method | Signature | Description |
|--------|-----------|-------------|
| `register` | `(type_url: str, factory) -> ComponentRegistry` | Register factory. Returns self (chainable). Raises `ValueError` on duplicate |
| `create` | `(type_url: str, config: dict \| None) -> Any` | Create component. Raises `KeyError` if unknown |
| `types` | `() -> frozenset[str]` | All registered type URLs |
| `__contains__` | `(type_url: str) -> bool` | Check if type URL is registered |
| `__len__` | `() -> int` | Number of registered factories |

A factory is any callable that accepts `**config` keyword arguments and returns a component.
