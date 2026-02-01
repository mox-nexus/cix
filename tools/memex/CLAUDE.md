# Memex

> Excavating Collaborative Intelligence Artifacts

Memex retrieves and connects historical human-AI collaboration artifacts across heterogeneous sources. Named for Vannevar Bush's 1945 vision of an "enlarged intimate supplement to memory."

## What Memex Is

**Excavating**, not observing. Historical artifacts, not live streams.

- Query conversations from Claude, Gemini, OpenAI, agent logs
- Intent-driven (80%): "where did I decide on auth?"
- Power-user SQL (20%): escape hatch for complex queries
- Trail discovery: connections across sources and time

## What Memex Is NOT

- Not live observability
- Not a log viewer
- Not Claude-specific (source-agnostic)

## Design Principles

Follows cix Design Principles (see root CLAUDE.md):

- **Defaults for Most (80%)**: `memex dig "..."` — intent-driven, just works
- **Complexity for Few (20%)**: `memex query "SELECT..."` — SQL escape hatch
- **Pit of Success**: Natural language is primary, SQL is explicit opt-out
- **Transparent Abstractions**: Show what was found, why, from where

---

## Guild Decisions

Architecture reviewed by arch-guild (2026-02-01). Key decisions:

### From K (Strategic)
- Trails belong in **Future**, not MVP — prove usage first
- Scope boundary: excavation and linking only, no live observation

### From Karman (Ontology)
- **Fragment** not Message — right granularity for excavation
- **Provenance** not source-specific fields — source-agnostic origin
- Messages have **parent_id** — they're trees, not flat lists
- **TrailLink** with typed refs — avoid polymorphic FK antipattern

### From Burner (Boundaries)
- SQL stays in adapters — domain uses predicates
- **IntentInterpreterPort** — separate concern for NL parsing
- Multiple source adapters behind single port

### From Ace (DX)
- Discovery commands: `corpus`, `sources`, `trails`
- Output contracts: `--format json`, `--format ids` for piping
- Error messages with suggestions, not just "not found"

### From Lamport (Consistency)
- **Two-layer schema**: raw (immutable) + interpreted (rebuildable)
- Watermarks: size + head-hash, not mtime
- **Idempotent writes**: `(source_kind, source_id)` composite key
- Timestamps for display only — clocks lie
- Trail positions are **human assertions**, not inferred

### From Ixian (Validation)
- MVP success: ingest Claude.ai, search works, < 1s latency
- Kill criteria: zero queries in 2-week period

---

## Domain Ontology

### Core Entities

| Entity | What It Is |
|--------|------------|
| **Excavation** | The act of retrieval — user intent → fragments |
| **Intent** | Parsed user request (NL → structured) |
| **Fragment** | Recovered unit of CI (right granularity) |
| **Provenance** | Source-agnostic origin |
| **Trail** | Connected fragments (discovered, not declared) |
| **Corpus** | All ingested sources, unified |

### Source Kinds

```python
class SourceKind(Enum):
    CLAUDE_CONVERSATIONS = "claude_conversations"
    CLAUDE_CODE_LOGS = "claude_code_logs"
    GEMINI = "gemini"
    OPENAI = "openai"
    AGENT_LOG = "agent_log"
    CUSTOM = "custom"
```

### Goals (What Users Want)

```python
class Goal(Enum):
    FIND_CODE = "find_code"
    RECALL_DECISION = "recall_decision"
    TRACE_EVOLUTION = "trace_evolution"
    RECOVER_CONTEXT = "recover_context"
    FIND_PATTERN = "find_pattern"
    EXPORT_ARTIFACTS = "export_artifacts"
```

---

## Hexagonal Architecture

```
┌─────────────────────────────────────────────────────┐
│ DRIVING (User-Facing)                               │
│ ├── CLI: memex dig, memex query, memex ingest      │
│ └── Future: Agent SDK app, MCP server              │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ DOMAIN (Pure, No Dependencies)                      │
│ ├── Excavation, Intent, Fragment, Provenance       │
│ ├── Trail, Corpus                                  │
│ └── Goal, TemporalConstraint                       │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ DRIVEN (Infrastructure)                             │
│ ├── IntentInterpreterPort → Claude, Gemini, Local  │
│ ├── SemanticSearchPort → Embeddings                │
│ ├── SourceAdapterPort → Claude, Gemini, OpenAI...  │
│ └── CorpusPort → DuckDB                            │
└─────────────────────────────────────────────────────┘
```

### Key Ports

**IntentInterpreterPort** — Swappable LLM backend:
```python
class IntentInterpreterPort(Protocol):
    def interpret(self, raw: str, context: ExcavationContext) -> Intent: ...
    def clarify(self, intent: Intent, question: str) -> Intent: ...
    def synthesize_trail(self, fragments: list[Fragment]) -> str: ...
```

**SourceAdapterPort** — Ingest different formats:
```python
class SourceAdapterPort(Protocol):
    def can_handle(self, path: Path) -> bool: ...
    def ingest(self, path: Path) -> Iterator[Fragment]: ...
    def source_kind(self) -> SourceKind: ...
```

**CorpusPort** — Persistence:
```python
class CorpusPort(Protocol):
    def store(self, fragment: Fragment) -> None: ...
    def query(self, sql: str) -> list[Fragment]: ...  # Power-user escape hatch
    def find_in_scope(self, scope: ExcavationScope) -> list[Fragment]: ...
```

---

## CLI Design

### 80% Intent-Driven
```bash
memex dig "where did I decide on auth?"
memex dig "code related to rate limiting"
memex dig "what was I working on last Tuesday?"
```

### Discovery
```bash
memex corpus                    # What's ingested
memex sources                   # Available source kinds
memex trails                    # Discovered trails
```

### Ingestion
```bash
memex ingest ~/Downloads/claude-export.json
memex ingest ~/.claude/projects/
memex sync                      # Update from known sources
```

### 20% Power-User
```bash
memex query "SELECT * FROM fragments WHERE ..."
memex sql                       # Interactive shell
```

---

## Consistency Model

### Two-Layer Schema
```sql
-- Raw layer (append-only, never reinterpreted)
raw_fragments (id, source_kind, source_id, raw_json, ingested_at)

-- Interpreted layer (rebuildable from raw)
fragments (id, content, provenance, context, schema_version)
```

### Watermarks
- Size + head-hash checkpoints (not mtime)
- Idempotent writes: `(source_kind, source_id)` composite key
- Re-ingestion is safe, just wasteful

### Ordering
- Timestamps for display only (clocks lie)
- Trail positions are explicit human assertions
- No inferred causality

---

## Directory Structure

```
tools/memex/
├── pyproject.toml
├── CLAUDE.md                   # This file
└── src/memex/
    ├── domain/
    │   ├── models.py           # Excavation, Intent, Fragment, etc.
    │   ├── goals.py            # Goal enum, temporal types
    │   └── connections.py      # Trail discovery (pure)
    ├── ports/
    │   ├── driving/
    │   │   └── excavation.py
    │   └── driven/
    │       ├── interpreter.py  # IntentInterpreterPort
    │       ├── search.py       # SemanticSearchPort
    │       ├── corpus.py       # CorpusPort
    │       └── source.py       # SourceAdapterPort
    ├── adapters/
    │   ├── interpreters/
    │   │   ├── claude.py
    │   │   ├── gemini.py
    │   │   └── local.py
    │   ├── sources/
    │   │   ├── claude_conversations.py
    │   │   ├── claude_code_logs.py
    │   │   ├── gemini.py
    │   │   └── openai.py
    │   └── corpus/
    │       ├── duckdb.py
    │       └── memory.py
    └── application/
        └── excavate.py
```

---

## Working Conventions

### SQL Stays in Adapters
Domain uses predicates (`ExcavationScope`, `TemporalConstraint`).
Adapters translate to SQL.

### Fragment Is the Atom
Not too small (message), not too large (conversation).
A meaningful, self-contained unit of collaborative work.

### Trails Are Discovered
Don't ask users to declare connections.
Find them: temporal proximity, semantic similarity, shared artifacts.

### Source-Agnostic Domain
`SourceKind` is metadata, not architecture.
Adding Gemini should be one adapter, not domain changes.

---

## References

- Vision: `/scratch/memex-vision.md`
- Guild Deliberation: `/scratch/memex-guild-deliberation.md`
- Ontology Details: `/scratch/memex-ontology.md`
- Vannevar Bush, "As We May Think" (1945)
