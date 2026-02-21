# The Data Model

Matrix's core data model is two types: **Construct** and **Artifact**. Together they form an append-only execution ledger that grows as components run.

---

## Artifact

An atomic, immutable fact produced by a component.

```python
@dataclass(frozen=True)
class Artifact:
    kind: str           # "probe.response", "sensor.grade", etc.
    producer: str       # component name that created this
    data: Any           # the actual value
    id: str             # uuid hex (auto-generated)
    created_at: float   # monotonic timestamp (auto-generated)
```

`kind` is how components find each other. A sensor that `requires={"probe.response"}` finds its upstream data via `construct.last("probe.response")`.

`data` is `Any` — Matrix doesn't constrain what components produce. Lists, dicts, Pydantic models, primitives — the consuming domain decides the shape.

## Construct

The append-only ledger. Immutable — every `append()` returns a new Construct.

```python
@dataclass(frozen=True)
class Construct(Generic[S]):
    subject: S                        # pass-through for consuming domain
    ledger: tuple[Artifact, ...] = () # ordered artifacts
```

### Reading Artifacts

```python
# Most recent artifact of a kind
data = construct.last("probe.response")

# All artifacts of a kind (in ledger order)
all_grades = construct.all("sensor.grade")

# What kinds exist
kinds = construct.kinds()  # frozenset({"probe.response", "sensor.grade"})
```

`last()` raises `LookupError` if no artifact of that kind exists. The DagCompiler guarantees that if a component's `requires` are satisfied at compile time, the artifacts will be present at runtime.

### Why Append-Only

Append-only means components can't overwrite upstream artifacts. This eliminates a class of bugs where component B accidentally corrupts component A's output. It also enables replay: the ledger is a complete record of what happened.

The trade-off: the full ledger stays in memory. For pipelines with many large artifacts, this matters. For typical 2-3 node DAGs, it's negligible.

## A Note on Subject

`Construct` is `Generic[S]` and carries a `subject` field. This is a pass-through for the consuming domain — Matrix never inspects it. In ix, the subject is the System Under Test. In another consumer, it could be a repo reference, a task ID, or anything else. Matrix just passes it through.

## The Execution Flow

```
1. Orchestrator.run(subject)
2. Construct = Construct(subject)        ← empty ledger
3. For each batch:
     For each component:
       data = component.run(construct)
       artifact = Artifact(kind, producer, data)
       construct = construct.append(artifact)  ← new Construct
4. Return Construct
```

Each component sees the full Construct at the time it runs — all upstream artifacts are available. The Construct grows monotonically. Nothing is removed or overwritten.
