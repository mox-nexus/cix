# Burner Review of memex-next Specification

**Reviewer:** Burner (guild-arch)
**Date:** 2026-04-25
**Subject:** [`design/memex-next/specification.md`](./specification.md)
**Verdict:** OBJECTION (recoverable)

The spec's domain modeling is strong. Structural problems concentrate in three places: a domain entity carrying cache state, a god-port mixing four responsibilities, and a missing application-service layer. Plus seven smaller leaks and one architectural gap (the polyglot question is dodged). All addressable; none reopen Karman's settled domain decisions.

---

## 1. Boundary violations (10)

### V1 — `Frame.principle_verdicts` is cache state in a domain entity (BLOCK-adjacent)

`specification.md:89` embeds LLM-decision cache state in the canonical Frame model. The Frame is content-addressed (`frame_id = blake2b(...)`, immutable per invariant) but `principle_verdicts` mutates without changing `frame_id` — either the field violates content-addressing, or it's not part of the Frame and shouldn't sit on it.

Also: `LifecycleEvent` already exists as the audit row for LLM decisions. `PrincipleVerdict` is a redundant materialization of the same information.

**Fix:** Move out. It's a projection over `LifecycleEvent`. If a fast read is needed, lives in `PrincipleVerdictCache` port (or `MemoryStore.get_latest_verdict(...)`), not as a Frame field.

### V2 — `MemoryStore` is a god-port

Current responsibilities: CRUD for 5 entity types, append-only event log, state-machine enforcement, hybrid search. Four distinct concerns answering different "what changes when implementation changes?" questions.

**Fix:** Split into `EntityStore`, `LifecycleEventLog`, `Recall`, optional `PrincipleVerdictCache`. Mirrors substrate reality: Lance can implement Entity+Recall, SQLite implements EventLog, graph substrate (if used) implements an additional `RelationGraph`.

### V3 — `transition_frame_state` is application logic in a port

State-machine validation (`episodic→reactivated` legal, `crystallized→episodic` illegal, etc.) is domain logic. Every store adapter would re-implement it or drift in interpretation.

**Fix:** Port does atomic field-update only. `LifecycleService.transition_frame_state` in application layer holds the state machine.

### V4 — `LLMDecision.action: LifecycleAction` couples LLM port to domain enum

OK as a domain-language port (closed enum, ports speak domain). But who enforces "decision.action is consistent with principle.severity"? Validation gap, not layering violation. Caller must check.

### V5 — `principle_body: str` as separate parameter is a serialization smell

`decide(principle: Principle, principle_body: str, candidates, context)` — why a separate parameter if `Principle` already has `body_path` and `version_sha`?

**Fix:** `decide(principle: ResolvedPrinciple, candidates, context)` where `ResolvedPrinciple` bundles `(principle_id, version_sha, severity, body_text)`. Caller resolves via `PrincipleStore` first.

### V6 — `Principle.body_path` is a filesystem path on a domain entity

Domain shouldn't know that principles live in markdown files in a directory. That's `PrincipleStore`'s business.

**Fix:** Drop `body_path` from domain `Principle`. Domain knows `(principle_id, title, severity, version_sha, enabled, metadata)`. Body comes from somewhere — the somewhere isn't the domain's concern.

### V7 — Missing application-service layer

The spec defines entities and ports but never names the service that orchestrates `transition_frame_state`, `compact_frame`, `crystallize`, `synthesize_recall`. Without it, orchestration logic ends up smeared into adapters, ports, or CLI entry points.

**Fix:** Add `application/services/`:
```python
class LifecycleService:
    def __init__(self, entities: EntityStore, events: LifecycleEventLog, llm: LLM, principles: PrincipleStore): ...
    def transition_frame_state(self, frame_id: str, new_state: FrameState, event: LifecycleEvent) -> None: ...
    def compact_frame(self, frame_id: str, principle: Principle) -> None: ...
    def crystallize(self, frame_ids: list[str], principle: Principle) -> Artifact: ...
    def synthesize_recall(self, query: str, hits: list[SearchHit]) -> Frame: ...
```
`Sweeper` is also application-layer, not a port.

### V8 — `MemexComposition` straddles layers

The composition spec is read by Claude (external), validated by Pydantic, used to wire adapters. Not a domain entity (`EmbedderSpec.impl: Literal["fastembed", "openai", "ollama"]` — domain has no business knowing impl identifiers).

**Fix:** Place explicitly in `composition/` (or `bootstrap/`, `wiring/`) layer that:
- Imports domain entities AND adapter implementations
- Is imported by CLI/entry-point only
- Is **never** imported by domain or application services

### V9 — `intent: str` lives on `MemexComposition` but its translation pathway is invisible

Two valid stances:
- **External** (recommended): intent-to-YAML happens in Claude conversation outside running system. Runtime only sees validated `MemexComposition`. `intent` is informational metadata.
- **Internal**: `CompositionGenerator` port that takes `intent` and emits `MemexComposition`.

Pick one. If external, say so explicitly: "the runtime never reads `intent` for behavior; it is provenance for replay/audit."

### V10 — `StoreSpec.impl` is single-slot for what may need to be polyglot

Spec opening line says "LanceDB primary, Kuzu graph, SQLite event log" — three substrates. But `StoreSpec` has one `impl` field. Either the Lance adapter internally uses three substrates (hidden polyglot, dishonest enum) or the port is wrong (one port for what should be three).

**Fix:** Split `StoreSpec` to mirror the port split (see §5).

---

## 2. Recommended port restructuring

```python
# Pure persistence — CRUD by id, no logic
class EntityStore(Protocol):
    def put_frame(self, frame: Frame) -> None: ...
    def get_frame(self, frame_id: str) -> Optional[Frame]: ...
    # ... episodes, artifacts, relations, trails ...
    def update_frame_state(self, frame_id: str, new_state: FrameState, event_id: str) -> None: ...
    # ^ atomic field update + event link, NO validation

# Append-only event log — different durability/access pattern
class LifecycleEventLog(Protocol):
    def append(self, event: LifecycleEvent) -> None: ...
    def list_for_entity(self, kind: EndpointKind, entity_id: str) -> Iterable[LifecycleEvent]: ...
    def list_for_principle(self, principle_id: str, since: datetime) -> Iterable[LifecycleEvent]: ...

# Search — different scaling profile, may swap independently
class Recall(Protocol):
    def hybrid_search(...) -> list[SearchHit]: ...

# Optional cache projection
class PrincipleVerdictCache(Protocol):
    def get_latest(self, frame_id: str, principle_id: str) -> Optional[PrincipleVerdict]: ...
    def put(self, frame_id: str, verdict: PrincipleVerdict) -> None: ...
```

Plus tightened `LLM`:
```python
class ResolvedPrinciple(BaseModel):
    principle_id: str
    version_sha: str
    severity: PrincipleSeverity
    body: str

class LLM(Protocol):
    def decide(self, principle: ResolvedPrinciple, candidates: list[Frame | Artifact], context: Optional[str]) -> LLMDecision: ...
    def synthesize(self, query: str, hits: list[SearchHit], loaded: list[Frame | Artifact], context: Optional[str]) -> str: ...
```

---

## 3. Forbidden-imports list for `domain/`

**Substrates / I/O:**
`lancedb`, `pylance`, `pyarrow`, `kuzu`, `duckdb`, `sqlite3`, `psycopg`, `tantivy`, `meilisearch`, `redis`, `os.path` (for resolving), `os.environ`, `os.system`, `subprocess`, `socket`, `httpx`, `requests`, `aiohttp`, `boto3`.

**LLM / Embedding clients:**
`anthropic`, `openai`, `ollama`, `cohere`, `voyage`, `fastembed`, `sentence_transformers`, `transformers`, `tiktoken`.

**Framework / Web:**
`fastapi`, `flask`, `django`, `starlette`, `click`, `typer`, `argparse`.

**Allowed in domain:**
- `pydantic` (committed dependency, treat as domain-modeling tool; `pydantic.BaseModel` only, no `pydantic-settings`)
- Standard library: `typing`, `datetime`, `hashlib`, `enum`, `dataclasses`, `uuid`, `decimal`
- `typing.Protocol` for port definitions

**Layer rules:**
- `application/services/` may import domain + ports + stdlib + pydantic; NOT adapter impls
- `adapters/<x>/` may import its substrate + domain entities/ports; NOT other adapters
- `composition/` is the ONLY place that constructs concrete adapters and wires them as ports
- `entrypoints/` (CLI etc.) imports from composition

---

## 4. The polyglot question — answer

Split `StoreSpec` to mirror port split:

```python
class EntityStoreSpec(BaseModel):
    impl: Literal["lance", "duckdb", "remote"]
    path: str

class EventLogSpec(BaseModel):
    impl: Literal["sqlite", "lance", "duckdb"]
    path: str

class RecallSpec(BaseModel):  # rename existing RecallSpec → RecallTuningSpec
    impl: Literal["lance_hybrid", "tantivy_plus_lance", "remote"]

class GraphSpec(BaseModel):  # OPTIONAL — see Kuzu-replacement decision
    impl: Literal["none", "duckpgq", "in_lance"]
```

Polyglot adapter (one impl that internally wires three substrates) hides the polyglot from the boundary — exactly what kills swap-ability. With the split, substrate changes ripple to one spec line, not to the port catalog.

---

## 5. Validation criteria — CI gates

**Import-linter contracts** in `pyproject.toml`:
```toml
[[importlinter.contracts]]
name = "Domain has no infrastructure imports"
type = "forbidden"
source_modules = ["memex_next.domain"]
forbidden_modules = [
    "lancedb", "pyarrow", "kuzu", "duckdb", "sqlite3",
    "anthropic", "openai", "ollama",
    "fastembed", "sentence_transformers", "transformers",
    "httpx", "requests", "aiohttp", "boto3",
    "fastapi", "click", "typer",
]

[[importlinter.contracts]]
name = "Layered architecture"
type = "layers"
layers = [
    "memex_next.entrypoints",
    "memex_next.composition",
    "memex_next.adapters",
    "memex_next.application",
    "memex_next.domain",
]
```

**Structural unit tests**:
- `test_frame_id_is_stable_across_principle_verdict_changes()` — Frame identity must not depend on transient state
- `test_legal_state_transitions_enforced_by_service_not_store()` — direct EntityStore.update_frame_state succeeds; LifecycleService.transition_frame_state raises IllegalTransitionError
- `test_principle_does_not_carry_filesystem_path()` — `"body_path" not in Principle.model_fields`
- `test_frame_does_not_carry_principle_verdicts()` — verdicts live in event log
- `test_no_port_exceeds_responsibility_budget()` — heuristic max-methods (rule of thumb: 8) on Protocol classes

**Polyglot-swap acceptance test**:
1. Boot with `entity_store=lance, event_log=sqlite, graph=none, recall=lance_hybrid`
2. Ingest fixture, run recall, crystallize artifact
3. Stop, swap composition: `entity_store=lance, event_log=duckdb, graph=duckpgq`
4. Boot pointed at same data dirs (event log migration allowed)
5. Run same recall — semantically equivalent results

If this test cannot be made to pass cleanly, boundaries leak.
