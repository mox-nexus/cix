# Memex-Next: Domain Ontology and Port Catalog

**Branch:** `lance` · **Status:** Specification (zero implementation) · **Substrate:** LanceDB primary, Kuzu graph, SQLite event log

This document is the contract between (a) the user's natural-language intent, (b) the Claude-generated composition spec, and (c) the runtime that wires adapters to ports. Everything in here is committed: types are committed, enums are closed where named closed, Protocols are the boundary the adapters meet.

Produced by Karman (guild-arch) on 2026-04-25, building on the prior Guild deliberation's load-bearing design constraints (see `research/concepts.md` and `scratch/session-2026-04-25-round-2-and-3.md`).

---

## 1. Entities

### 1.1 `Frame` — the encoding unit

The canonical record of one captured cognitive event. Stored broadly (Wilson). Two-axis: `kind` is what it IS at birth (record/abstract/extract); `state` is where it is in the lifecycle (episodic/reactivated/crystallized/compacted). Both are sum-types; both are exhaustive; neither subsumes the other.

```python
from typing import Literal, Optional
from datetime import datetime
from pydantic import BaseModel, Field

FrameKind = Literal["record", "abstract", "extract"]
# record  — captured-as-witnessed (a message, a document chunk, an observation)
# abstract — derived alignment/composite (Pickering alignment events, multi-frame gist)
# extract — LLM-derived assertion lifted from one or more records (a fact, a claim)

FrameState = Literal["episodic", "reactivated", "crystallized", "compacted"]
# episodic     — fresh; carries reliving-quality context (Wilson)
# reactivated  — accessed at least once since ingestion (Nader: every recall is a write)
# crystallized — earned durability via reactivation × principle-match
# compacted    — original hidden ≥90 days; gist-Frame written as new row (kind=abstract)

Speaker = Literal["user", "assistant", "system", "tool", "document", "observer"]
# closed: who-uttered. NOT source-of-derivation.

ProvenanceSource = Literal[
    "ingest.conversation",   # captured from a chat export
    "ingest.document",       # captured from a document/file
    "ingest.observation",    # captured from an external observer (logs, agent traces)
    "derivation.alignment",  # produced by alignment detector over records
    "derivation.extract",    # produced by extraction LLM over records
    "derivation.compaction", # produced by compaction LLM (gist of an aged Frame)
    "derivation.synthesis",  # produced by recall synthesizer (Frame from a recall event)
]

class Provenance(BaseModel):
    source: ProvenanceSource
    parents: list[str] = Field(default_factory=list)   # frame_ids derived from
    adapter: str                                        # adapter id that produced this Frame
    adapter_version: str
    captured_at: datetime                               # when memex saw it
    occurred_at: Optional[datetime] = None              # when it actually happened (if known)

class Frame(BaseModel):
    frame_id: str                                # blake2b(provenance.adapter, upstream_id, occurred_at)
    kind: FrameKind
    state: FrameState

    # Content
    content: str                                 # the textual payload (verbatim if record)
    content_format: Literal["text", "markdown", "code", "json"] = "text"
    embedding: Optional[list[float]] = None      # nullable; backfill-able
    embedding_model: Optional[str] = None        # which embedder produced this vector

    # Authorship (split per constraint #4)
    speaker: Speaker
    speaker_label: Optional[str] = None          # free-form display (e.g. "Yash", "Claude Opus 4.7")

    # Provenance (the OTHER axis of authorship)
    provenance: Provenance

    # Domain attachment
    episode_id: Optional[str] = None             # the conversation/document this Frame belongs to
    parts: list[str] = Field(default_factory=list)  # for kind=abstract: constituent frame_ids

    # Open vocabulary (extensibility lives here — see §3)
    roles: set[str] = Field(default_factory=set)

    # Decay/lifecycle telemetry (read by gates, written by lifecycle service)
    access_count: int = 0
    last_accessed_at: Optional[datetime] = None
    principle_match_count: int = 0               # cumulative principle-match events
    decay_score: float = 1.0                     # 1.0 = fresh, → 0 with disuse
    compacted_at: Optional[datetime] = None
    compacted_into: Optional[str] = None         # frame_id of the gist-Frame (if state=compacted)
    superseded_by: Optional[str] = None          # frame_id (relations.kind=supersedes mirror)

    # Cached principle verdicts (constraint #10 — single LLM synthesis lives downstream)
    principle_verdicts: dict[str, "PrincipleVerdict"] = Field(default_factory=dict)

class PrincipleVerdict(BaseModel):
    principle_id: str
    principle_version_sha: str
    verdict: Literal["match", "miss", "abstain"]
    confidence: float                             # 0..1
    decided_at: datetime
    model: str                                    # e.g. "claude-opus-4-7"
    rationale: Optional[str] = None
```

**Invariants** (domain-validator enforced):

- `kind="abstract"` ⇒ `len(parts) >= 2` (composites are by definition multi-Frame).
- `kind="record"` ⇒ `parts == []` and `provenance.source` is one of the `ingest.*` values.
- `kind="extract"` ⇒ `len(parents) >= 1` and `provenance.source = "derivation.extract"`.
- `state="compacted"` ⇒ `compacted_at is not None` AND `compacted_into is not None`. Original Frame row persists (constraint #9: hide-not-delete).
- `state="crystallized"` ⇒ at least one `Artifact.derived_from_frames` contains this `frame_id` AND `principle_match_count >= 1`.
- `embedding is not None` ⇒ `embedding_model is not None`.
- `speaker="document"` ⇒ `provenance.source == "ingest.document"`.
- `frame_id` is content-addressed and immutable. Mutations write a new Frame and a `supersedes` Relation.

**Lifecycle:** `episodic → reactivated` on first access (recall-as-write, Nader). `reactivated → crystallized` on principle-match × reactivation gate (the gate is composition-configured). `episodic|reactivated → compacted` after age-threshold without principle-match. `crystallized` Frames can fade their *Frames* (the schema-supporting Frames compact) without losing the `Artifact` they support.

**Relationships:** belongs-to one `Episode` (or none, for derived Frames); points to other Frames via `Relation` rows; can be `derived_from` parents (provenance) and `parts` (composite); cited by zero-or-more `Artifact`s; cited by zero-or-more `Trail`s.

---

### 1.2 `Episode` — the conversation/document container

Per constraint #2, `Archive` is renamed to `Episode` to restore the cognitive-domain term. Document-ingest is a `role` on the Episode, not a sibling entity.

```python
EpisodeRole = Literal["conversation", "document", "observation_stream"]
# closed-enum role: what this Episode IS structurally.

class Episode(BaseModel):
    episode_id: str
    role: EpisodeRole
    title: Optional[str] = None
    started_at: datetime
    ended_at: Optional[datetime] = None         # None for open / streaming
    source_adapter: str                          # which ingest adapter produced this
    source_upstream_id: Optional[str] = None     # adapter-native id (conversation uuid, file path, etc.)
    participants: list[str] = Field(default_factory=list)  # speaker_labels seen
    frame_count: int = 0
    metadata: dict[str, str] = Field(default_factory=dict) # adapter-defined, opaque to domain
```

**Invariants:**

- `episode_id` is unique. Re-ingesting the same source must hit the same `episode_id` (idempotent).
- `frame_count` is a maintained materialization, not authoritative; the count of Frames where `episode_id == self.episode_id` is the truth.
- `role="document"` ⇒ Frames in this Episode have `speaker="document"`.
- `role="conversation"` ⇒ Frames have `speaker ∈ {user, assistant, system, tool}`.
- An Episode is never deleted while any of its Frames exist (referential integrity).

**Lifecycle:** Episodes are largely immutable post-ingest. `ended_at` may be set when a streaming source closes. `metadata` is append-only.

---

### 1.3 `Artifact` — the crystallized schema

The durable, context-free knowledge that emerged from one or more Frames. Per constraint #3, the Frame ↔ Artifact link is a `derived_from` Relation, not identity transfer. **Both persist.**

```python
ArtifactKind = Literal["principle", "decision", "design_note", "summary", "definition", "open_question"]

class Artifact(BaseModel):
    artifact_id: str
    kind: ArtifactKind
    title: str
    body: str                                    # markdown
    embedding: Optional[list[float]] = None
    embedding_model: Optional[str] = None

    derived_from_frames: list[str]               # frame_ids — the provenance chain
    crystallized_at: datetime
    crystallized_by: str                         # principle_id that earned crystallization

    version: int = 1
    supersedes: Optional[str] = None             # prior artifact_id, if this is a refinement
    superseded_by: Optional[str] = None

    roles: set[str] = Field(default_factory=set) # open vocabulary
```

**Invariants:**

- `len(derived_from_frames) >= 1`.
- An Artifact is never deleted; refinement creates a new Artifact and writes `supersedes`/`superseded_by`. Old versions stay queryable.
- `crystallized_by` must reference an existing `Principle.principle_id` at some version.

**Lifecycle:** Created when crystallization gate fires. Refined by writing `version+1` with `supersedes` pointing to current head. The supporting Frames may compact independently — the Artifact remains the schema even after its Frames lose episodic detail (Squire).

**Relationships:** points to Frames via `derived_from_frames`; chain of versions via `supersedes`; cited by `Trail`.

---

### 1.4 `Relation` — the typed edge

Per constraint #5, relation kinds split into structural (mechanical/derivable) vs semantic (meaning-bearing, often LLM-asserted). Both first-class.

```python
StructuralRelationKind = Literal[
    "follows",        # temporal: A precedes B in same Episode
    "references",     # mention: A textually references B
    "derived_from",   # provenance: A was produced from B (Frame→Frame, Artifact→Frame)
    "similar_to",     # embedding-distance: A and B are near in vector space
    "part_of",        # compositional: A is a part of composite B (mirror of Frame.parts)
]

SemanticRelationKind = Literal[
    "confirms",       # B confirms A's claim
    "contradicts",    # B contradicts A's claim
    "supersedes",     # B replaces A as the current understanding
    "refines",        # B sharpens A without replacing
    "summarizes",     # B is a gist of A
]

RelationKind = Literal[
    "follows", "references", "derived_from", "similar_to", "part_of",
    "confirms", "contradicts", "supersedes", "refines", "summarizes",
]

RelationRegister = Literal["structural", "semantic"]

EndpointKind = Literal["frame", "artifact", "episode"]  # what a relation endpoint can BE

class Relation(BaseModel):
    relation_id: str
    kind: RelationKind
    register: RelationRegister                   # derivable from kind; stored for query

    src_id: str
    src_kind: EndpointKind
    dst_id: str
    dst_kind: EndpointKind

    weight: float = 1.0                          # similarity score, confidence, etc.
    asserted_by: Literal["system", "llm", "user"] # who created this edge
    asserted_at: datetime

    # For LLM-asserted semantic relations: provenance of the assertion
    lifecycle_event_id: Optional[str] = None

    # Bi-temporal (structural relations may be eternal; semantic ones expire under contradiction)
    valid_from: Optional[datetime] = None
    valid_to: Optional[datetime] = None
```

**Invariants:**

- `register` MUST match the kind's category. `kind ∈ structural set ⇒ register="structural"`; same for semantic.
- `asserted_by="llm"` ⇒ `lifecycle_event_id is not None` (constraint #8).
- `kind="similar_to"` ⇒ `register="structural"`, `asserted_by="system"`, `weight ∈ (0, 1]`.
- `src_id != dst_id` (no self-loops).
- `kind="supersedes"` is **append-only**: writing a new supersedes does not delete the old; it adds a chain.

**Lifecycle:** Structural relations are written at ingest or by background indexers and live forever (or until `similar_to` is recomputed under a new embedding model — old rows expire by `valid_to`). Semantic relations are written by the LLM in service of recall or compaction and carry a `lifecycle_event_id` linking back to the principle that produced them.

---

### 1.5 `Trail` — the named, ordered, authored sequence

Bush's central innovation. Per the thesis: trails are first-class but **not a separate user task** — they are LLM-executed under user-set principles.

```python
class TrailEntry(BaseModel):
    position: int                                # 0-indexed sequence position
    target_id: str
    target_kind: EndpointKind                    # frame | artifact | episode
    annotation: Optional[str] = None             # LLM- or user-authored
    added_at: datetime
    added_by: Literal["llm", "user"]
    principle_id: Optional[str] = None           # which principle threaded this in

class Trail(BaseModel):
    trail_id: str
    name: str                                    # human-readable, unique per workspace
    description: str
    created_at: datetime
    updated_at: datetime
    author: Literal["llm", "user"]               # primary curator
    entries: list[TrailEntry]
    forked_from: Optional[str] = None            # trail_id of parent if forked
    roles: set[str] = Field(default_factory=set)
```

**Invariants:**

- `entries` is dense and ordered: positions are `0..n-1`, no gaps, monotonically increasing `added_at` is **not** required (back-insertion is allowed; position is authoritative).
- `name` is unique within a workspace.
- `target_id` must resolve to an existing entity of `target_kind`.
- A Trail is never destructively edited: removing an entry writes a `LifecycleEvent` and creates a new Trail version; the old version remains queryable via the event log.

**Lifecycle:** Trails grow as the LLM threads new entities under matching principles. Trails can be forked (`forked_from`) — a divergent version of a trail with its own annotations.

---

### 1.6 `Principle` — the user-authored selector

Per constraint #8: principles live in markdown, git-versioned. The DB row is a pointer/cache; the source of truth is the file.

```python
PrincipleSeverity = Literal["preserve", "compress", "elevate", "thread", "discard"]
# What kind of action this principle authorizes the LLM to take.

class Principle(BaseModel):
    principle_id: str                            # stable across versions, e.g. "preserve-unresolved-tensions"
    title: str
    severity: PrincipleSeverity
    body_path: str                               # repo-relative path to the markdown file
    version_sha: str                             # git blob sha of current body
    enabled: bool = True
    metadata: dict[str, str] = Field(default_factory=dict)  # open vocabulary
```

**Invariants:**

- `principle_id` is stable across versions; only `version_sha` changes when body changes.
- A `LifecycleEvent` produced under principle P MUST record P's `version_sha` at decision time (constraint #8).
- `severity="discard"` is reserved for write-side gating (a Frame matching a discard principle is never persisted past staging) — see §4 MemoryStore semantics.

**Lifecycle:** Principles are authored, refined, deprecated. Disabling a principle does not invalidate past `LifecycleEvent`s; it stops new ones from being produced under it.

---

### 1.7 `LifecycleEvent` — the audit row for every consequential LLM decision

Per constraint #8: every consequential LLM decision writes one. This is the system's own memory of how it decided.

```python
LifecycleAction = Literal[
    "ingest_admit",        # admitted to store
    "ingest_reject",       # rejected at write-side gate (severity=discard)
    "reactivate",          # state episodic → reactivated
    "crystallize",         # Frame(s) → Artifact created
    "refine",              # Artifact version+1 written
    "compact",             # Frame state → compacted, gist Frame written
    "supersede",           # supersedes relation written
    "thread",              # entity added to a Trail
    "annotate",            # annotation added (Trail entry, Frame role, etc.)
    "synthesize_recall",   # recall synthesizer produced a derivation.synthesis Frame
]

class LifecycleEvent(BaseModel):
    event_id: str
    action: LifecycleAction
    occurred_at: datetime

    # Decision provenance (constraint #8)
    principle_id: Optional[str]                  # None only for system-mechanical actions
    principle_version_sha: Optional[str]
    model: Optional[str]                         # "claude-opus-4-7" — None for non-LLM events
    model_version: Optional[str]

    # What the LLM actually output (verbatim)
    llm_output: Optional[str] = None
    llm_input_digest: Optional[str] = None       # blake2b of prompt — for replay/audit

    # What entities this action affected
    affected: list[tuple[EndpointKind, str]] = Field(default_factory=list)

    # Open extensibility
    extras: dict[str, str] = Field(default_factory=dict)
```

**Invariants:**

- `action ∈ {ingest_admit, ingest_reject, reactivate, crystallize, refine, compact, thread, annotate, synthesize_recall, supersede}` — closed.
- If `model is not None` then `principle_id` and `principle_version_sha` MUST be set (every LLM decision is principle-grounded).
- Append-only. `LifecycleEvent` rows are never updated or deleted.

**Lifecycle:** Write-only. Read by audit/debug paths and by the read-side decay projection (constraint #7) which uses event density as a signal.

---

## 2. Closed Enumerations

These are the committed sum-types. Adding a value is a schema change requiring deliberation.

| Enum | Values |
|---|---|
| `FrameKind` | `record`, `abstract`, `extract` |
| `FrameState` | `episodic`, `reactivated`, `crystallized`, `compacted` |
| `Speaker` | `user`, `assistant`, `system`, `tool`, `document`, `observer` |
| `ProvenanceSource` | `ingest.conversation`, `ingest.document`, `ingest.observation`, `derivation.alignment`, `derivation.extract`, `derivation.compaction`, `derivation.synthesis` |
| `EpisodeRole` | `conversation`, `document`, `observation_stream` |
| `ArtifactKind` | `principle`, `decision`, `design_note`, `summary`, `definition`, `open_question` |
| `StructuralRelationKind` | `follows`, `references`, `derived_from`, `similar_to`, `part_of` |
| `SemanticRelationKind` | `confirms`, `contradicts`, `supersedes`, `refines`, `summarizes` |
| `RelationRegister` | `structural`, `semantic` |
| `EndpointKind` | `frame`, `artifact`, `episode` |
| `LifecycleAction` | `ingest_admit`, `ingest_reject`, `reactivate`, `crystallize`, `refine`, `compact`, `supersede`, `thread`, `annotate`, `synthesize_recall` |
| `PrincipleSeverity` | `preserve`, `compress`, `elevate`, `thread`, `discard` |
| `ContentFormat` | `text`, `markdown`, `code`, `json` |

---

## 3. Open Vocabularies

Where extensibility lives. These are `set[str]` or `dict[str, str]` — domain validators do not constrain them; principles and adapters define their own conventions.

- **`Frame.roles`** — accrued attributes attached to a Frame post-ingest. Examples a Claude config might use: `"unresolved-tension"`, `"chitchat"`, `"design-decision"`, `"debugging-arc"`, `"insight"`, `"reactor-pipeline"`. Roles are added by LifecycleEvents (action=`annotate`); they are the principle-domain's vocabulary, not the engine's.
- **`Artifact.roles`** — same shape, applied to crystallized schemas. E.g. `"core-thesis"`, `"open-question"`.
- **`Trail.roles`** — e.g. `"active"`, `"archived"`, `"shared"`.
- **`Principle.metadata`** — adapter-defined hints. Examples: `{"compaction_age_days": "7"}`, `{"min_reactivation_count": "3"}`.
- **`LifecycleEvent.extras`** — opaque tag bag for adapter-specific debugging or replay.
- **`Episode.metadata`** — source-adapter-defined opaque metadata (e.g. Claude conversation uuid, file mtime, etc.). The domain does not parse this.

---

## 4. Port Catalog

Each port is a `typing.Protocol`. Methods speak domain language only; substrate translation is the adapter's job.

### 4.1 `MemoryStore`

The persistence and retrieval port. One concrete adapter: `LanceMemoryStore` (LanceDB-backed). Future: `DuckDBMemoryStore`, `RemoteMemoryStore` (daemon).

```python
from typing import Protocol, Iterable, Optional

class MemoryStore(Protocol):
    # ---- writes ----
    def put_frame(self, frame: Frame) -> None: ...
    """Idempotent on frame_id. Raises FrameInvariantError if domain invariants violated.
       Pre: frame.embedding may be None (backfill is allowed).
       Post: subsequent get_frame(frame.frame_id) returns an equivalent Frame."""

    def put_episode(self, episode: Episode) -> None: ...
    """Idempotent on episode_id."""

    def put_artifact(self, artifact: Artifact) -> None: ...
    """Idempotent on artifact_id. Raises if derived_from_frames contains unknown frame_ids."""

    def put_relation(self, relation: Relation) -> None: ...
    """Idempotent on relation_id. Raises EndpointMissingError if src_id/dst_id do not resolve."""

    def put_trail(self, trail: Trail) -> None: ...
    """Idempotent on trail_id. Replaces entries atomically (the trail is the unit, not the entry)."""

    def append_lifecycle_event(self, event: LifecycleEvent) -> None: ...
    """Append-only. Raises if event_id already exists."""

    # ---- state transitions (write-side gates apply here) ----
    def transition_frame_state(
        self, frame_id: str, new_state: FrameState, event_id: str
    ) -> None: ...
    """Atomic: validates the transition is legal, applies it, links the LifecycleEvent.
       Pre: event_id must reference an existing LifecycleEvent.
       Legal transitions: episodic→reactivated, reactivated→crystallized,
       {episodic,reactivated}→compacted. Raises IllegalTransitionError otherwise."""

    def compact_frame(self, frame_id: str, gist_frame: Frame, event_id: str) -> None: ...
    """Hide-not-delete (constraint #9): original Frame stays; gist_frame is written;
       original.compacted_into = gist_frame.frame_id; original.state = 'compacted'.
       Pre: gist_frame.kind == 'abstract' AND frame_id ∈ gist_frame.parts."""

    # ---- reads ----
    def get_frame(self, frame_id: str) -> Optional[Frame]: ...
    def get_episode(self, episode_id: str) -> Optional[Episode]: ...
    def get_artifact(self, artifact_id: str) -> Optional[Artifact]: ...
    def get_trail(self, trail_id: str) -> Optional[Trail]: ...

    def list_frames_in_episode(self, episode_id: str) -> Iterable[Frame]: ...
    def list_relations(
        self,
        src_id: Optional[str] = None,
        dst_id: Optional[str] = None,
        kind: Optional[RelationKind] = None,
    ) -> Iterable[Relation]: ...
    def list_lifecycle_events(self, frame_id: str) -> Iterable[LifecycleEvent]: ...

    # ---- search ----
    def hybrid_search(
        self,
        query_text: str,
        query_embedding: Optional[list[float]] = None,
        context_embedding: Optional[list[float]] = None,   # ecphoric: current cognitive state
        top_k: int = 10,
        kinds: Optional[set[EndpointKind]] = None,
        states: Optional[set[FrameState]] = None,           # filter by lifecycle state
        roles_any: Optional[set[str]] = None,               # open-vocab match-any
    ) -> list["SearchHit"]: ...
    """Two-stage recall stage 1 (constraint #10). Returns top-k=5–10 typically.
       Pre: at least one of query_text or query_embedding is provided.
       Post: results are ranked; scoring is hybrid (BM25 + vector + context-vector if provided);
       the read-side decay projection (constraint #7) is applied to scores."""

class SearchHit(BaseModel):
    target_id: str
    target_kind: EndpointKind
    score: float
    score_components: dict[str, float]   # {"bm25": .., "vector": .., "context": .., "decay": ..}
```

### 4.2 `Embedder`

```python
class Embedder(Protocol):
    model_name: str
    dimensions: int

    def embed(self, texts: list[str]) -> list[list[float]]: ...
    """Pre: all texts non-empty. Post: returns vectors of length self.dimensions in same order."""

    def embed_one(self, text: str) -> list[float]: ...
```

**Semantics:** `model_name` is the identity of the embedding contract. Changing models requires re-embedding (Frames retain `embedding_model` so side-by-side migration is possible).

### 4.3 `LLM`

The decision-maker. All consequential calls go through this port and produce a `LifecycleEvent`.

```python
class LLMDecision(BaseModel):
    action: LifecycleAction
    rationale: str
    confidence: float
    affected: list[tuple[EndpointKind, str]]
    extras: dict[str, str] = Field(default_factory=dict)

class LLM(Protocol):
    model: str
    model_version: str

    def decide(
        self,
        principle: Principle,
        principle_body: str,                 # the markdown body at version_sha
        candidates: list[Frame | Artifact],  # what the principle is evaluating
        context: Optional[str] = None,       # current cognitive state, recent activity
    ) -> LLMDecision: ...
    """Pre: principle.enabled. Post: decision.action is consistent with principle.severity
       (e.g. severity='discard' admits action='ingest_reject'). The runtime is responsible for
       writing the LifecycleEvent from the decision; the LLM port does not write."""

    def synthesize(
        self,
        query: str,
        hits: list[SearchHit],
        loaded: list[Frame | Artifact],      # the resolved entities for hits
        context: Optional[str] = None,
    ) -> str: ...
    """Two-stage recall stage 2 (constraint #10). Single LLM synthesis over top-k hits.
       Returns the answer text. The runtime writes a derivation.synthesis Frame and
       a synthesize_recall LifecycleEvent."""
```

### 4.4 `Sweeper`

Background lifecycle processor. Per constraint #7, decay is read-side primary; the sweeper handles compaction (write-side gate for the 90-day rule) and similarity-edge maintenance. Not the primary mechanism for forgetting.

```python
class Sweeper(Protocol):
    def sweep_compaction_candidates(self, now: datetime) -> Iterable[str]: ...
    """Returns frame_ids eligible for compaction (age ≥ 90 days, no recent reactivation,
       no principle_match). Caller resolves the LLM decision and writes the gist."""

    def rebuild_similar_edges(self, embedding_model: str) -> int: ...
    """Recomputes similar_to relations under the given embedding model. Returns count written.
       Old similar_to relations under prior models are valid_to-stamped, not deleted."""
```

### 4.5 `IngestAdapter`

Source-side. One per upstream system (Claude conversations, OpenAI, document folder, observation stream).

```python
class IngestAdapter(Protocol):
    adapter_id: str           # stable identifier, e.g. "claude_conversations"
    adapter_version: str

    def discover(self, source_uri: str) -> Iterable["RawCapture"]: ...
    """Walk the upstream source and yield RawCapture units."""

    def to_episode(self, raw: "RawCapture") -> Episode: ...
    def to_frames(self, raw: "RawCapture") -> Iterable[Frame]: ...

class RawCapture(BaseModel):
    upstream_id: str
    payload: dict
    discovered_at: datetime
```

### 4.6 `PrincipleStore`

Reads markdown principles from a git-versioned directory and returns them with current `version_sha`.

```python
class PrincipleStore(Protocol):
    def list_principles(self) -> list[Principle]: ...
    def get_principle(self, principle_id: str) -> Optional[Principle]: ...
    def get_body(self, principle_id: str, version_sha: str) -> str: ...
    """Returns the markdown body at the given sha — for replay/audit fidelity."""
```

### 4.7 `RelationIndexer`

Builds structural relations (`follows`, `references`, `similar_to`, `derived_from`, `part_of`). Distinct from the LLM port because these are mechanical.

```python
class RelationIndexer(Protocol):
    def build_follows(self, episode_id: str) -> int: ...
    def build_similar_to(self, frame_id: str, top_k: int = 8) -> int: ...
    def build_references(self, frame_id: str) -> int: ...
```

---

## 5. Configuration Shape

The composition spec is the boundary between user intent and runtime wiring. It is YAML, schema-validated by Pydantic. Claude reads user intent and emits one of these.

### 5.1 Schema

```python
class EmbedderSpec(BaseModel):
    impl: Literal["fastembed", "openai", "ollama"]
    model_name: str
    dimensions: int
    config: dict[str, str] = Field(default_factory=dict)

class LLMSpec(BaseModel):
    impl: Literal["anthropic", "openai", "ollama"]
    model: str
    model_version: str
    config: dict[str, str] = Field(default_factory=dict)

class StoreSpec(BaseModel):
    impl: Literal["lance", "duckdb", "remote"]
    path: str
    config: dict[str, str] = Field(default_factory=dict)

class IngestSpec(BaseModel):
    adapter_id: str                              # must match a registered IngestAdapter
    source_uri: str
    schedule: Literal["once", "watch", "manual"] = "manual"
    config: dict[str, str] = Field(default_factory=dict)

class PrincipleSpec(BaseModel):
    principle_id: str
    body_path: str                               # relative to principles_dir
    severity: PrincipleSeverity
    metadata: dict[str, str] = Field(default_factory=dict)

class RecallSpec(BaseModel):
    top_k: int = 8
    use_context_vector: bool = True
    structural_filters: list[StructuralRelationKind] = Field(default_factory=list)
    semantic_filters: list[SemanticRelationKind] = Field(default_factory=list)

class LifecycleSpec(BaseModel):
    compaction_age_days: int = 90
    reactivation_threshold: int = 3              # accesses needed before crystallize gate runs
    crystallize_requires_principle_match: bool = True

class MemexComposition(BaseModel):
    """The full spec that instantiates a memex."""
    name: str                                    # workspace name
    intent: str                                  # the original natural-language request, preserved
    workspace_path: str                          # where .memex/ lives

    store: StoreSpec
    embedder: EmbedderSpec
    llm: LLMSpec

    principles_dir: str                          # markdown principles, git-versioned
    principles: list[PrincipleSpec]              # active set

    ingests: list[IngestSpec]                    # one or more sources
    recall: RecallSpec = RecallSpec()
    lifecycle: LifecycleSpec = LifecycleSpec()

    # Open vocabulary roles this composition uses (declared upfront for validation)
    declared_roles: set[str] = Field(default_factory=set)
```

### 5.2 Validation rules (so bad LLM output fails loudly)

- `name` must match `^[a-z][a-z0-9-]{1,63}$`.
- `principles_dir` must exist; every `principles[i].body_path` must resolve under it.
- `ingests` must be non-empty.
- Every `ingests[i].adapter_id` must match a registered adapter at runtime startup; unknown ⇒ refuse to start.
- `embedder.dimensions` must be > 0 and ≤ 4096.
- `llm.model` is a free string but `llm.impl` is closed; mismatch (impl=anthropic, model=gpt-4) is a warning not a refusal.
- `lifecycle.compaction_age_days >= 7` (constraint #9 floor: compaction is hide-not-delete for ≥ 90 days; the *body* is preserved either way, but values < 7 are likely user error).
- `recall.top_k` must be in `[1, 50]`.
- At least one `principles[i].severity` must be in `{preserve, elevate}` (a memex with only `discard` principles is incoherent).

### 5.3 Example: "memex over my Claude conversations"

User intent: *"I want a memex for my code conversations with Claude, prioritizing unresolved technical tensions, compressing chitchat after a week."*

```yaml
name: claude-code-memex
intent: |
  Memex for code conversations with Claude. Prioritize unresolved technical tensions.
  Compress chitchat after a week.
workspace_path: ~/.memex/claude-code

store:
  impl: lance
  path: ~/.memex/claude-code/lance
  config:
    table_frames: frames
    table_artifacts: artifacts

embedder:
  impl: fastembed
  model_name: nomic-embed-text-v1.5
  dimensions: 768

llm:
  impl: anthropic
  model: claude-opus-4-7
  model_version: "1m"

principles_dir: ~/.memex/claude-code/principles
principles:
  - principle_id: preserve-unresolved-tensions
    body_path: preserve-unresolved-tensions.md
    severity: preserve
    metadata:
      crystallize_after_reactivations: "3"
  - principle_id: compress-chitchat
    body_path: compress-chitchat.md
    severity: compress
    metadata:
      compaction_age_days: "7"
  - principle_id: elevate-design-decisions
    body_path: elevate-design-decisions.md
    severity: elevate
  - principle_id: thread-debugging-arcs
    body_path: thread-debugging-arcs.md
    severity: thread

ingests:
  - adapter_id: claude_conversations
    source_uri: ~/Downloads/claude-export
    schedule: watch

recall:
  top_k: 8
  use_context_vector: true
  semantic_filters: [confirms, contradicts, refines]

lifecycle:
  compaction_age_days: 90
  reactivation_threshold: 3
  crystallize_requires_principle_match: true

declared_roles:
  - unresolved-tension
  - chitchat
  - design-decision
  - debugging-arc
  - insight
```

### 5.4 Example: "memex over code repository documents + conversations"

User intent: *"Memex over my repo's docs and my Claude conversations about that repo, so I can ask questions that span design notes and the discussions that produced them."*

```yaml
name: repo-knowledge-memex
intent: |
  Memex over repo documents AND Claude conversations about the repo. Span design notes
  and the discussions that produced them.
workspace_path: ./.memex

store:
  impl: lance
  path: ./.memex/lance

embedder:
  impl: fastembed
  model_name: nomic-embed-text-v1.5
  dimensions: 768

llm:
  impl: anthropic
  model: claude-opus-4-7
  model_version: "1m"

principles_dir: ./.memex/principles
principles:
  - principle_id: preserve-design-rationale
    body_path: preserve-design-rationale.md
    severity: preserve
  - principle_id: link-doc-to-conversation
    body_path: link-doc-to-conversation.md
    severity: thread
    metadata:
      relation_kind: references
  - principle_id: crystallize-recurring-decisions
    body_path: crystallize-recurring-decisions.md
    severity: elevate
    metadata:
      crystallize_after_reactivations: "2"

ingests:
  - adapter_id: filesystem_documents
    source_uri: ./docs
    schedule: watch
    config:
      glob: "**/*.md"
  - adapter_id: filesystem_documents
    source_uri: ./
    schedule: watch
    config:
      glob: "**/CLAUDE.md"
  - adapter_id: claude_conversations
    source_uri: ~/Downloads/claude-export
    schedule: watch
    config:
      filter_episode_title: repo-knowledge

recall:
  top_k: 10
  use_context_vector: true
  structural_filters: [references, derived_from]
  semantic_filters: [refines, supersedes]

lifecycle:
  compaction_age_days: 180
  reactivation_threshold: 2

declared_roles:
  - design-rationale
  - architectural-decision
  - implementation-note
  - api-contract
```

---

## 6. Author / Provenance Model

Per constraint #4, `Author` splits into two distinct concepts that compose with `kind` and `state`.

### 6.1 `speaker` — closed enum, dialogue role

`Speaker = Literal["user", "assistant", "system", "tool", "document", "observer"]`

**Why closed:** the dialogue-role registers are stable across systems. A new "speaker" usually isn't a new role — it's a new label within an existing role. `speaker_label` is the open string for display ("Claude Opus 4.7", "Yash", "vim plugin"); `speaker` is the structural slot.

**Composition:**
- `speaker="user"` Frames anchor encoding-specificity retrieval (Stafford: own-words are the part most likely to need preservation).
- `speaker="document"` Frames must come from `EpisodeRole="document"` (invariant).
- `speaker="observer"` is for non-conversational captures (agent traces, log lines).

### 6.2 `provenance.source` — closed enum, derivation pathway

```
ingest.conversation
ingest.document
ingest.observation
derivation.alignment
derivation.extract
derivation.compaction
derivation.synthesis
```

**Why closed:** the *pathways* by which a Frame can come to exist are bounded by the system architecture itself. Adding a new pathway is an architectural change, not a config change. New ingest *adapters* don't add new pathways — they all use `ingest.conversation` or `ingest.document` or `ingest.observation`.

**Composition with `kind`:**

| `provenance.source` | Required `kind` | Required `state` at birth |
|---|---|---|
| `ingest.conversation` | `record` | `episodic` |
| `ingest.document` | `record` | `episodic` |
| `ingest.observation` | `record` | `episodic` |
| `derivation.alignment` | `abstract` | `episodic` (composite of recently-active Frames) |
| `derivation.extract` | `extract` | `episodic` |
| `derivation.compaction` | `abstract` | `crystallized` (the gist replaces the original's role) |
| `derivation.synthesis` | `abstract` | `episodic` (a recall-event Frame; reconsolidates parent Frames) |

**Composition with `state`:**

State is orthogonal to provenance after birth. A `derivation.extract` Frame can age into `compacted` like any other. A `derivation.synthesis` Frame triggers `state` transitions on its `parents` (each parent goes `episodic → reactivated`) — that's reconsolidation captured (Nader).

### 6.3 The two-axis discipline

`kind` answers: *what kind of object IS this?* (immutable after birth)
`state` answers: *where is it in its lifecycle?* (mutates over time, monotonically along the legal-transition graph)
`speaker` answers: *whose voice is in the content?* (immutable)
`provenance.source` answers: *by what process did it come to exist?* (immutable)

These four axes are independent. The product is a finite, enumerable space — every Frame has a coordinate `(kind, state, speaker, provenance.source)` and the validator enforces the legal product.

---

## Closing Note: What This Specification Commits To

- **The atom is `Frame`**, not `Fragment`. The legacy vocabulary in `tools/memex/src/memex/domain/models.py` is wrong-shaped per the thesis: `Fragment` collapses dialogue role, derivation pathway, and lifecycle state into one flat model.
- **The container is `Episode`**, not `Archive`. Document-ingest is `EpisodeRole="document"`, a role on Episode, not a sibling type.
- **Frame ↔ Artifact is `derived_from`**, not identity transfer. Both rows persist forever (modulo compaction's hide-not-delete). The Artifact survives the Frame's episodic detail loss; the Frame survives the Artifact's revision.
- **Two relation registers**, both first-class: structural (mechanical) and semantic (LLM-asserted under principle).
- **Decay is read-side projection** (scoring) plus a write-side compaction gate that hides-not-deletes after ≥ 90 days. Sweeper is supportive, not primary.
- **Every consequential LLM decision is a `LifecycleEvent`** with principle_id, principle_version_sha, model identity, and verbatim llm_output. Replayable, auditable.
- **Configuration is the composition spec.** A YAML/Pydantic schema is the boundary between Claude-generated intent-translation and runtime wiring.
- **Closed enums where the registers are bounded by the system's own architecture; open vocabularies where the principle-domain accumulates.** The line is drawn explicitly, not by accident.
