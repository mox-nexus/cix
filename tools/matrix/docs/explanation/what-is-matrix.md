# What is Matrix?

Matrix is a component runtime. It takes a composed DAG of components, validates the topology, and executes them in topological order. Components in, artifacts out.

Matrix sits at the bottom of the stack. By the time it sees anything, the consuming domain has already decomposed its intent into concrete components with concrete configuration. Matrix doesn't need to understand why — it runs what it's given.

---

## The Problem

DAG execution recurs across domains. An eval pipeline runs probe → sensor. A code intelligence pipeline runs parser → transformer → emitter. A data pipeline runs extract → transform → load. The components differ. The orchestration is the same: compile topology, schedule batches, execute, collect results.

Building orchestration into each domain means every domain re-derives cycle detection, topological sorting, artifact passing, and error propagation. The alternative: a shared runtime that knows nothing about any domain but handles all execution concerns.

## How Matrix Works

Matrix operates in three phases:

**1. Compile** — `DagCompiler` reads each component's `requires` (what artifact kinds it needs) and `provides` (what artifact kind it produces). From these declarations it infers edges, detects missing producers, duplicate outputs, duplicate names, and cycles. The result is a validated registry and adjacency map.

**2. Schedule** — `DagScheduler` generates execution batches via `graphlib.TopologicalSorter`. Components within a batch are independent of each other and could run in parallel. Batches execute sequentially.

**3. Execute** — `Orchestrator` drives each component in order. Before a component runs, all its upstream artifacts are available in the `Construct` (an append-only ledger). Each component's return value is wrapped in an `Artifact` and appended to the Construct.

```
Compile: [Probe, Sensor, Scorer] → edges, registry
Schedule: edges → [[Probe], [Sensor], [Scorer]]
Execute: for batch in schedule:
           for component in batch:
             data = component.run(construct)
             construct = construct.append(Artifact(kind, producer, data))
```

## Where Matrix Fits

```
Domain (ix, radix, ...)
  → Decomposes hypothesis / task into components + config
    → Composition resolves concrete components
      → Matrix receives the composed DAG and executes it
```

Matrix is downstream of all the interesting decisions. The consuming domain owns intent, decomposition, and composition. Matrix owns compilation, scheduling, and execution.

## Design Decisions

### Kind-Agnostic

Matrix uses `kind: str` — an extensible string, not an enum. Matrix doesn't know or care about probes, sensors, or scorers. It sees components with dependencies and orchestrates them.

This means any domain can map onto Matrix:
- **ix**: trial → sensor_node (experimentation)
- **radix**: parser → transformer → emitter (code intelligence)
- **ETL**: extract → transform → load (data pipelines)

Same runtime. Different vocabularies.

### Structural Typing

The `Component` protocol uses `typing.Protocol` — structural subtyping. Applications implement the shape without importing Matrix. No base classes, no inheritance, no framework coupling.

```python
# This IS a Component — no import needed
class MyThing:
    name = "my-thing"
    requires = frozenset({"upstream.data"})
    provides = "my-thing.output"

    async def run(self, construct):
        data = construct.last("upstream.data")
        return transform(data)
```

### Append-Only Ledger

The `Construct` is immutable. `append()` returns a new instance. Components can't mutate artifacts written by upstream components — they read via `construct.last(kind)` and produce new data.

This prevents mutation bugs and enables replay: given the same inputs and components, execution is deterministic.

### Static Validation

Topology errors are caught at compile time, before any component runs:

| Error | When |
|-------|------|
| Missing producer | Component requires a kind nobody provides |
| Duplicate output | Two components provide the same kind |
| Duplicate name | Two components share a name |
| Cycle | A → B → A dependency loop |

## What Matrix Is Not

| Matrix Is | Matrix Is Not |
|-----------|---------------|
| A component runtime | A workflow engine (no retries, no persistence) |
| Kind-agnostic | Domain-aware (no probes, sensors, hypotheses) |
| Sequential execution | Parallel execution (batches are sequential currently) |
| Compile-time validation | Runtime validation (no dynamic re-wiring) |
| A library | A service (no daemon, no API) |

The boundaries are deliberate. Matrix handles topology and execution. Decomposition, persistence, retries, and domain semantics belong to the consuming application.

## A Note on Subject

`Construct` carries a `subject` field as a pass-through for the consuming domain. Matrix never inspects it. In ix, the subject is the System Under Test. In another consumer, it could be a repo reference or a task identifier. Matrix just passes it through.
