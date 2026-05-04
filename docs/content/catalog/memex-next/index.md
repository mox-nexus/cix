# memex-next

*Personal memory system for human-AI collaboration archives. In active design, no implementation yet — this doc reflects the current architectural state.*

**Status:** Pre-implementation. Branch: `lance`. Specification at `design/memex-next/specification.md`. Design thesis at `research/concepts.md`. Canonical knowledge-representation theory: SMRT (Vyas, in progress).

---

## What memex is

A personal memory substrate that sits underneath your work, captures conversations and documents, and amplifies what matches your principles while letting most things fade. It augments natural cognition rather than replacing it.

The thesis from `research/concepts.md`:

> Memex is a selective amplifier. Encoding is broad (Wilson). Decay is default (biology). Amplification is principle-gated (collaborative). LLM is the executor (post-2023 affordance).

Forgetting is the default state. Preservation is what costs energy. The principles you write — in plain English — drive the LLM that decides per-interaction what to keep, what to compress, what to thread together. You don't curate item-by-item; you curate at the policy level.

## What memex does — the kernel

At the base level, **every interaction with memex is a graph-write event.** Everything else is engineering around that one operation.

| Interaction | What gets written |
|---|---|
| Ingest a conversation | Frames (one per message), Episode (the conversation), Relations (`follows` between turns), LifecycleEvent (`ingest_admit`) |
| Recall something | LifecycleEvent (`synthesize_recall`), state transitions on touched Frames (`episodic → reactivated`) — recall is itself a write (Nader's reconsolidation) |
| Annotate | New Frame (the annotation), Relation (`annotates` linking annotation to target) |
| LLM threads a Trail under a principle | TrailEntry (positioned Relation), LifecycleEvent (`thread`) recording principle + model + rationale |
| Compaction (long-unaccessed Frame) | New gist Frame, `compacted_into` Relation, original Frame state moves to `compacted` (hide-not-delete) |

The graph is the memex. Read or write, with structure intact.

---

## Domain model

Seven entities, with vocabulary aligned to **SMRT** (Situated Modal Relation Triplet) — the cross-disciplinary semantic-atom thesis from the parallel research project.

### Frame — the encoding atom

The retrieval-sized unit. Discriminated union by `kind`, with state on a separate axis.

```python
Frame = RecordFrame | AbstractFrame | ExtractFrame
```

| Kind | What it is | Source |
|---|---|---|
| `record` | Captured-as-witnessed (a message, a document chunk, an observation) | `ingest.conversation` / `ingest.document` / `ingest.observation` |
| `abstract` | Derived/summarized/distilled. Has `parts: list[frame_id]` (composite) — alignment events live here | `derivation.alignment` / `derivation.compaction` / `derivation.synthesis` |
| `extract` | Verbatim content pulled from an artifact (a claim, a section). Has `derived_from: list[frame_id]` | `derivation.extract` |

**State** is independent of kind:

```
episodic → reactivated → crystallized → compacted
```

`episodic` = fresh. `reactivated` = accessed at least once (Nader: every recall is a write). `crystallized` = earned durability via reactivation × principle-match. `compacted` = original hidden ≥90 days (hide-not-delete), gist Frame written as new row.

Frames carry the **embedding**. Nothing else does. They are the only unit that retrieval surfaces.

### Episode — the temporally-bounded container

A conversation, a document-ingest event, an observation stream. Temporally bounded. Contextually unified. Episodic memory in Tulving's sense — event-specific, contextually-situated, with that "reliving" quality.

Single class with `role: Literal["conversation", "document", "observation_stream"]`. Per-role invariants enforced by validators (e.g., `role="conversation"` requires ≥2 distinct participants).

### Artifact — the stored-whole thing

Full content stored whole. Format-discriminated, not semantic-kind-discriminated. The thing memex points at when you say "the JWT paper."

```python
class Artifact:
    artifact_id: str
    format: str               # txt, md, pdf, py, jsonl, html, svg, png, ...
    title: Optional[str]
    content: Optional[str]    # textual artifacts stored inline
    source_uri: Optional[str] # for blobs / external
    author: Optional[str]     # human, model name, "memex", or None
    episode_id: Optional[str]
    created_at: datetime
    metadata: dict[str, str]
```

Origins are two: **uploaded** (user brings in a paper, code, document) or **generated** (Claude produces a long response that's substantial enough to keep whole). Both produce the same entity. Origin is implicit in `author` and the `IngestAdapter` that produced it.

**No embedding on Artifact.** Frames are the retrieval atoms; Artifacts are reached via the Frames extracted from them (`extract` Frames carrying `derived_from = artifact_id`).

### Relation — the meaning-bearing entity

This is the load-bearing entity. **Meaning lives in Relations**, not in Frames. A Frame's content has weight only because of its relational placement.

Per SMRT, every Relation has three intrinsic facets:

```python
class Relation:
    relation_id: str
    src_id: str
    src_kind: EndpointKind          # frame | artifact | episode
    dst_id: str
    dst_kind: EndpointKind
    kind: RelationKind              # the connection type
    register: Literal["structural", "semantic"]
    
    situation: Situation            # encoding context (when, where, by whom, under what)
    modality: Modality              # epistemic-practical stance
    
    weight: float = 1.0
```

**Relation kinds** (closed, split into two registers):

- **Structural** (mechanical, system-asserted): `follows`, `references`, `derived_from`, `similar_to`, `part_of`
- **Semantic** (judgment-bearing, LLM-asserted): `confirms`, `contradicts`, `supersedes`, `refines`, `summarizes`

**Situation** captures the encoding context:

```python
class Situation:
    asserted_at: datetime
    asserted_by: Literal["system", "llm", "user"]
    episode_id: Optional[str]
    principle_id: Optional[str]
    principle_version_sha: Optional[str]
    lifecycle_event_id: Optional[str]
    valid_from: Optional[datetime]
    valid_to: Optional[datetime]
```

**Modality** is the SMRT three-mode state machine:

```python
modality: Literal["potential", "assertoric", "directive"]
```

- **Potential (?)** — under investigation, hypothesis, abductive
- **Assertoric (.)** — established operational fact, falsifiable, the assertoric default
- **Directive (!)** — action commitment, deontic ("must hold")

All six pairwise transitions valid. Modal pressure (the readiness to transition) is a fuzzy gradient updated on reactivation × evidence × commitment events. v0 stores the field; v1+ uses the state machine.

The **ontological/epistemic axis firewall** (canonical SMRT discipline): modality tracks the agent's stance, not the proposition's truth properties. Truth-of-content lives in the Relation; stance-toward-content lives in the Modality.

### Trail — the named, ordered, authored sequence

Bush's central innovation. Per the design thesis: trails are first-class but **not a separate user task** — they are LLM-executed under user-defined principles. Humans set policies; the LLM threads entities into trails on every interaction.

```python
class Trail:
    trail_id: str
    name: str                       # unique per workspace
    description: str
    entries: list[TrailEntry]       # dense, ordered, position 0..n-1
    author: Literal["llm", "user"]
    forked_from: Optional[str]
    roles: set[str]
```

A TrailEntry is a positioned Relation: `(position, target_id, target_kind, annotation, principle_id, added_at, added_by)`.

### Principle — the user-authored selector

Markdown body, git-versioned. The DB row is a pointer/cache; the source of truth is the file.

```python
class Principle:
    principle_id: str               # stable across versions
    title: str
    severity: Literal["preserve", "compress", "elevate", "thread", "discard"]
    version_sha: str                # git blob sha
    enabled: bool
    metadata: dict[str, str]
```

A `LifecycleEvent` produced under principle `P` records `P`'s `version_sha` at decision time — replayable audit trail.

### LifecycleEvent — the audit row

Append-only event log. Every consequential LLM decision writes one. Every state transition writes one. Every reactivation writes one.

```python
class LifecycleEvent:
    event_id: str
    action: LifecycleAction         # ingest_admit | reactivate | crystallize | compact | thread | annotate | synthesize_recall | ...
    occurred_at: datetime
    principle_id: Optional[str]
    principle_version_sha: Optional[str]
    model: Optional[str]            # "claude-opus-4-7"
    model_version: Optional[str]
    llm_output: Optional[str]
    llm_input_digest: Optional[str] # blake2b of prompt — for replay
    affected: list[tuple[EndpointKind, str]]
    extras: dict[str, str]
```

This is what `memex why <id>` reads to reconstruct decision history. Append-only, never updated, never deleted.

---

## Architecture — hexagonal

Layers, with strict dependency direction (inward only):

```
┌──────────────────────────────────────────────────┐
│  ENTRYPOINTS  (CLI, API, etc.)                   │
└──────────────────────────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────────────┐
│  COMPOSITION                                     │
│  Wires concrete adapters to ports per spec       │
└──────────────────────────────────────────────────┘
              │
              ▼
┌──────────────────────────────────────────────────┐
│  ADAPTERS                                        │
│  LanceStore, FastEmbedEmbedder, AnthropicLLM,    │
│  ClaudeIngestAdapter, MarkdownPrincipleStore...  │
└──────────────────────────────────────────────────┘
              │ implements
              ▼
┌──────────────────────────────────────────────────┐
│  APPLICATION                                     │
│  LifecycleService, IngestService, RecallService, │
│  Sweeper. Owns orchestration + state machines.   │
└──────────────────────────────────────────────────┘
              │ depends on
              ▼
┌──────────────────────────────────────────────────┐
│  DOMAIN                                          │
│  Entities + Ports (Protocol) + invariants.       │
│  Pure. No infrastructure imports.                │
└──────────────────────────────────────────────────┘
```

### Ports

Per Burner's adapter-discipline review, the persistence god-port splits into four:

| Port | Responsibility |
|---|---|
| `EntityStore` | CRUD by id over Frame, Episode, Artifact, Relation, Trail. Atomic state field updates. **No** state-machine validation — that's application logic. |
| `LifecycleEventLog` | Append-only event log. Different durability profile (often a different substrate than entities — SQLite vs Lance). |
| `Recall` | Hybrid search (BM25 + vector + RRF, eventually + context vector for ecphoric retrieval). Different scaling profile, may swap independently. |
| `PrincipleVerdictCache` | (Optional) fast read of cached LLM decisions, projection over `LifecycleEventLog`. Add only when perf demands. |

Plus four more ports for cross-cutting concerns:

| Port | Responsibility |
|---|---|
| `Embedder` | `text → vector[float]`. Has `model_name` + `dimensions`. Frame-only embeddings. |
| `LLM` | `decide(principle, candidates, context) → LLMDecision` and `synthesize(query, hits, loaded, context) → str`. All consequential calls produce a `LifecycleEvent`. |
| `IngestAdapter` | Source-side parser. One per upstream system (Claude conversations, OpenAI exports, document directories, observation streams). Yields `Episode`s and `Frame`s. |
| `PrincipleStore` | Reads markdown principles from a git-versioned directory, returns them with their current `version_sha`. |
| `RelationIndexer` | Builds **structural** relations only (`follows`, `references`, `similar_to`, `derived_from`, `part_of`). Distinct from `LLM` because these are mechanical. |

**No `RelationGraph` port for v1.** Trails and graph traversal queries run as DuckDB recursive CTEs over Lance-backed Relation tables. No separate graph DB. Kuzu was the prior plan; Kuzu was archived October 2025 (Apple acquired Kuzu Inc.); we evaluated alternatives and concluded that at memex's personal scale (<1M frames), recursive CTEs are sufficient. Add a `RelationGraph` port behind a `GraphSpec.impl` slot if a real query shape demands it.

### Application services

Not ports. They're the orchestration layer that holds state machines and policies.

| Service | Responsibility |
|---|---|
| `LifecycleService` | Owns the Frame state machine. Validates legal transitions before calling `EntityStore.update_frame_state`. Owns `compact_frame`, `crystallize`, `synthesize_recall`. |
| `IngestService` | Orchestrates `discover → episode → frames → admit/reject` (write-side principle gate). |
| `RecallService` | Two-stage recall: hybrid search → top-k → `LLM.synthesize`. Writes the `synthesize_recall` LifecycleEvent + reactivation transitions. |
| `Sweeper` | Background lifecycle processor. Compaction candidates, similarity-edge maintenance. Refuses to run when LLM is unavailable (per Taleb). |

### Adapters (current planned set)

| Port | v0/v1 adapter | Future options |
|---|---|---|
| `EntityStore` | `LanceEntityStore` | `DuckDBEntityStore`, `RemoteEntityStore` |
| `LifecycleEventLog` | `LanceLifecycleEventLog` (or `SQLiteLifecycleEventLog`) | `DuckDBLifecycleEventLog` |
| `Recall` | `LanceHybridRecall` (BM25 + vector + RRF) | `TantivyPlusLanceRecall`, `RemoteRecall` |
| `Embedder` | `FastEmbedEmbedder` (nomic-embed-text-v1.5, ~768d) | `OpenAIEmbedder`, `OllamaEmbedder` |
| `LLM` | `AnthropicLLM` (claude-opus-4-7) | `OpenAILLM`, `OllamaLLM` |
| `IngestAdapter` | `ClaudeIngestAdapter`, `FilesystemDocumentIngestAdapter` | `OpenAIIngestAdapter`, `LinearIngestAdapter`, `RSSObservationAdapter` |
| `PrincipleStore` | `GitMarkdownPrincipleStore` | `RemotePrincipleStore` |
| `RelationIndexer` | `LanceRelationIndexer` (recursive CTEs) | DuckPGQ-backed if perf demands |

A single substrate (LanceDB) typically implements multiple ports for v0 — one concrete `LanceStore` class can implement `EntityStore`, `LifecycleEventLog`, `Recall`, and the structural-relation parts of `RelationIndexer`. Splitting impl ↔ port is a composition concern; the port catalog stays honest.

### Forbidden imports in `domain/`

The discipline that makes hexagonal hold:

```
Forbidden in domain/:
  Substrates: lancedb, pyarrow, kuzu, duckdb, sqlite3, tantivy
  LLM clients: anthropic, openai, ollama, fastembed, sentence_transformers
  HTTP/network: httpx, requests, aiohttp, boto3, socket
  Frameworks: fastapi, click, typer, argparse
  Filesystem-resolving: os.path resolve operations, os.environ, subprocess

Allowed in domain/:
  pydantic (committed dependency, treat as domain-modeling tool)
  Standard library: typing, datetime, hashlib, enum, dataclasses, uuid
  typing.Protocol for port definitions
```

Enforced via `import-linter` contracts in `pyproject.toml` from the first commit. Layered architecture rule:
`entrypoints → composition → adapters → application → domain` (strictly inward).

---

## Composition — what makes a memex *this* memex

A **composition** is a declarative spec that turns the memex codebase into a specific instance. You can have multiple compositions per user — each is a separate memex with its own data, principles, and tuning, all using the same codebase.

The spec is YAML, validated by Pydantic:

```yaml
name: claude-code-memex
intent: |
  Memex for code conversations with Claude. Preserve unresolved technical tensions.
  Compress chitchat after a week.
workspace_path: ~/.memex/claude-code

store:
  impl: lance
  path: ~/.memex/claude-code/lance

embedder:
  impl: fastembed
  model_name: nomic-embed-text-v1.5
  dimensions: 768

llm:
  impl: anthropic
  model: claude-opus-4-7

principles_dir: ~/.memex/claude-code/principles
principles:
  - { principle_id: preserve-unresolved-tensions, severity: preserve }
  - { principle_id: compress-chitchat,             severity: compress }
  - { principle_id: elevate-design-decisions,      severity: elevate }
  - { principle_id: thread-debugging-arcs,         severity: thread }

ingests:
  - adapter_id: claude_conversations
    source_uri: ~/Downloads/claude-export
    schedule: watch

recall:
  top_k: 8
  use_context_vector: true

lifecycle:
  compaction_age_days: 90
  reactivation_threshold: 3

declared_roles: [unresolved-tension, chitchat, design-decision, debugging-arc, insight]
```

This document IS the memex. It declares which adapters wire to which ports, which principles are active, what the lifecycle parameters are.

**The intent-driven path:** users don't write YAML. They describe intent in natural language ("memex for my code conversations, preserving unresolved tensions, compressing chitchat after a week"). Claude generates the composition spec. Pydantic validates. The runtime instantiates adapters per the spec.

Configuration-as-composition: the spec doesn't *configure* an existing memex; it *defines what this memex is*.

---

## Current state — what's v0, what's deferred

### v0 (target: working ingest + recall, no principle layer yet)

| Capability | v0.1 | v0.2 | v0.3 |
|---|---|---|---|
| Project scaffolding (domain, application, adapters, composition, entrypoints) | ✓ | | |
| Forbidden-imports CI gate | ✓ | | |
| Domain entities + ports as Protocol | ✓ | | |
| ClaudeIngestAdapter + FastEmbedEmbedder + LanceStore | ✓ | | |
| `memex ingest` CLI | ✓ | | |
| Hybrid search (BM25 + vector + RRF, no context vector) | | ✓ | |
| `memex recall` CLI | | ✓ | |
| LifecycleEvent on every reactivation | | ✓ | |
| `memex why <id>` audit verb | | ✓ | |
| Long-content promotion (Frame → Artifact + abstract Frame) | | | ✓ |
| Trail entity, basic LLM-executed threading under one default principle | | | ✓ |

### v1 (target: principle layer + LLM execution + state machine in use)

- Principle markdown files + GitMarkdownPrincipleStore
- LLM port (AnthropicLLM) wired into write-side gate (ingest filtering) and read-side synthesis (two-stage recall stage 2)
- LifecycleService state-machine validation in use (full episodic→reactivated→crystallized transitions)
- Crystallization gates earning Artifacts from reactivated Frames
- Modality field actively used (mostly assertoric, principle-driven directives)
- `memex principles edit` CLI with dry-run validation

### v2+ (deferred until evidence forces them)

- Compaction (hide-not-delete after ≥90 days)
- Sweeper (background lifecycle processor)
- Ecphoric retrieval (current-state context vector + Situation matching)
- Full SMRT modal state machine with bidirectional transitions
- Modal transition pressure (fuzzy gradient updateable on reactivation)
- Burner's full port split with separate adapter implementations (vs sharing a backend)
- Multi-substrate polyglot (DuckDB/Kuzu-replacement/etc. — only if Lance + DuckDB CTEs hit a real wall)
- Frame-level Modality (currently only on Relations)

The deferral discipline: **port boundaries hold from day 1**, even when adapters share a backend. Splitting impls later is a composition change, not a domain refactor.

---

## Pointers to deeper material

In-repo:

| Document | Purpose |
|---|---|
| [`design/memex-next/specification.md`](../../../../design/memex-next/specification.md) | Full Pydantic-shaped specification (domain entities + ports + composition schema + 2 example YAMLs) |
| [`design/memex-next/burner-review.md`](../../../../design/memex-next/burner-review.md) | Burner's structural review — the 10 boundary violations + port restructuring + CI gates |
| [`research/concepts.md`](../../../../research/concepts.md) | The design thesis, distillation of cognitive-science research, methodology notes (research-grounded vs synthesis-inference) |

External theoretical anchors (cited by name; not in this repo):

- **SMRT** (Vyas, in progress) — Situated Modal Relation Triplet; the canonical knowledge-representation theory memex implements
- **Cognitive-science substrate** — Tulving on encoding specificity and ecphory, Bartlett on schemas, Nader on reconsolidation, Wilson on encoding-broad principles, Pickering on interactive alignment / mergence in dialogue. The design thesis (`research/concepts.md`) cites these inline where they're load-bearing
- **Comparative landscape** — Mem0, Letta, Zep/Graphiti, Cognee; LanceDB / DuckDB hybrid storage; UMR / FactBank / MPQA annotation schemes for R/M/S facets. Citations inline in the design thesis

---

## Open architectural questions

These are still open as of 2026-04-27 and worth tracking:

1. **The `register: structural | semantic` split on Relation.** Burner's review introduced it for adapter discipline. SMRT doesn't carve relations into registers — it's all one atom. Is the split memex-implementation concern (audit + write-source separation) or domain concern? Possible simplification post-v0.
2. **Frame.parts vs Relation `part_of`.** Frame has `parts: list[frame_id]` for composites (alignment events). There's also a `part_of` structural relation kind. One is canonical; the other is a read-side projection. Pick.
3. **Frame-level Modality.** Currently Modality lives on Relation. Should `extract` Frames carry their own Modality (since they're standalone claims pulled from sources)? Or do they always flow through a Relation that carries it?
4. **Intent translation pathway.** Composition spec preserves `intent: str`. Is intent-to-YAML translation (a) a Claude conversation outside the runtime, or (b) a `CompositionGenerator` port the runtime calls? Default leaning: (a) — runtime never reads `intent` for behavior, it's provenance for replay/audit.
5. **`Sweeper` placement.** Application service vs separate background-process layer. Currently called application service; may need its own layer if process boundaries differ from the running memex.
6. **Ecphoric retrieval design.** What goes into the context vector (current cognitive state)? How is it composed? What's the scoring formula combining content + Situation + modality + decay? Open thread; needs Karman + Erlang + Ace as a triad.

---

*Last updated: 2026-04-27 — reflects design state after Round 2 verification (SHIP), Karman ontology spec, Burner adapter-discipline review, Kuzu-drop decision, and SMRT alignment.*
