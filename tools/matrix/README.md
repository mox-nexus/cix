# Matrix

Component runtime for DAG execution.

## What Matrix Does

Matrix is the runtime where composed components execute. A consuming domain (like ix) decomposes its intent into a component configuration — which components to run, with what config. Matrix takes that composed DAG, validates the topology, and executes it. Components in, artifacts out.

Matrix doesn't know what probes, sensors, or hypotheses are. It knows what components are. Your domain decomposes its concepts into components and hands them to Matrix for execution.

## Usage

```python
from matrix import Orchestrator, Construct

# Components declare what they need and what they produce
class Probe:
    name = "probe"
    requires = frozenset()           # root node — no dependencies
    provides = "probe.response"

    async def run(self, construct: Construct) -> str:
        return "hello"

class Sensor:
    name = "sensor"
    requires = frozenset({"probe.response"})
    provides = "sensor.grade"

    async def run(self, construct: Construct) -> bool:
        upstream = construct.last("probe.response")
        return upstream == "hello"

# Domain decomposes work into components, Matrix just runs them
orch = Orchestrator([Probe(), Sensor()])
construct = await orch.run("my-experiment")

construct.last("sensor.grade")  # True
```

## The Component Protocol

One contract. Four fields. No base class.

```python
class Component(Protocol):
    name: str                  # unique identifier
    requires: frozenset[str]   # artifact kinds this component reads
    provides: str              # artifact kind this component produces

    async def run(self, construct: Construct) -> Any:
        """Read upstream artifacts, do work, return data."""
        ...
```

Structural typing via `typing.Protocol`. Implement the shape — you never need to import Matrix.

## Documentation

| Document | Description |
|----------|-------------|
| [What is Matrix?](docs/explanation/what-is-matrix.md) | Why it exists, design decisions, what it's not |
| [The Data Model](docs/explanation/data-model.md) | Construct and Artifact — the append-only execution ledger |
| [API Reference](docs/reference/api.md) | All public types: Component, Orchestrator, DagCompiler, ... |
