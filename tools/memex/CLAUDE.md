# Memex

> Extended memory for you and your agents

Memex retrieves and connects historical human-AI collaboration artifacts across heterogeneous sources. Named for Vannevar Bush's 1945 vision of an "enlarged intimate supplement to memory."

---

## Tooling

Best-in-class, modern tooling only. No legacy.

| Task | Use | Never |
|------|-----|-------|
| Python | `uv` | pip, conda, poetry, raw python |
| Run scripts | `uv run` | python directly |
| Add deps | `uv add` | pip install |
| JS (if needed) | `bun` | npm, yarn, node |

```bash
# YES
uv run pytest
uv add rich

# NO
python -m pytest
pip install rich
```

---

## What Memex Is

**Excavating**, not observing. Historical artifacts, not live streams.

- Query conversations from Claude, OpenAI
- Hybrid search: BM25 keyword + semantic (embeddings) + cross-encoder reranking
- Power-user SQL (20%): escape hatch for complex queries

## What Memex Is NOT

- Not live observability
- Not a log viewer
- Not Claude-specific (source-agnostic)

## Design Principles

Follows cix Design Principles (see root CLAUDE.md):

- **Defaults for Most (80%)**: `memex dig "..."` — hybrid search, just works
- **Complexity for Few (20%)**: `memex query "SELECT..."` — SQL escape hatch
- **Pit of Success**: `dig` is primary, SQL is explicit opt-out
- **Transparent Abstractions**: Show what was found, why, from where
- **Convention over Config**: Local `.memex/` overrides global — no flags needed

---

## Configuration Resolution

Memex uses convention-over-config (like `.git/`). A local `.memex/` directory in or above the CWD becomes the active workspace.

### Precedence (highest wins)

| Layer | Source | Example |
|-------|--------|---------|
| 1 | `MEMEX_*` env vars | `MEMEX_CORPUS_PATH=/custom/path` |
| 2 | Local `.memex/` (walk up from CWD) | `./project/.memex/corpus.duckdb` |
| 3 | Global `~/.memex/config.toml` | `~/.memex/corpus.duckdb` |
| 4 | Defaults | `~/.memex/corpus.duckdb` |

### Multi-Store Pattern

```bash
memex init            # Global store at ~/.memex/
memex init --local    # Project-local store at ./.memex/

# In a project with .memex/:
cd myproject/
memex dig "auth"      # Searches local .memex/corpus.duckdb
cd myproject/src/     # Walk-up finds ../myproject/.memex/
memex dig "auth"      # Still uses myproject's local store

# Outside any .memex/:
cd ~
memex dig "auth"      # Falls back to ~/.memex/corpus.duckdb
```

### Local `.memex/` Structure

```
.memex/                    # Project-local workspace (add to .gitignore)
├── config.toml            # Optional local config overrides
└── corpus.duckdb          # Project-local corpus
```

Resolution happens in `config/settings.py`. The rest of the stack receives a `Path` and is workspace-agnostic.

---

## Domain Ontology

### Implemented Entities

| Entity | What It Is |
|--------|------------|
| **Fragment** | Recovered unit of CI (right granularity) — THE canonical entity |
| **Provenance** | Source-agnostic origin (source_kind, source_id, timestamp) |
| **EmbeddingConfig** | Embedding contract (model_name, dimensions) — domain invariant |

### Source Kinds

Extensible strings (not enum). Common values:

```python
SOURCE_CLAUDE_CONVERSATIONS = "claude_conversations"
SOURCE_OPENAI = "openai"
SOURCE_GEMINI = "gemini"  # adapter not yet implemented
SOURCE_CUSTOM = "custom"
```

### Future (Not Yet Implemented)

These entities appeared in the original guild deliberation but are deferred:

- **Intent** — Parsed user request (NL → structured). Requires IntentInterpreterPort.
- **Trail** — Connected fragments (discovered, not declared). Deferred per K's recommendation.
- **Goal** — User intent classification. Depends on Intent.
- **ExcavationScope** — Domain predicate for search scoping. Currently handled by CLI options.

---

## Hexagonal Architecture

```
┌─────────────────────────────────────────────────────┐
│ DRIVING (_in)                                       │
│ └── CLI: memex dig, memex keyword, memex ingest     │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ DOMAIN (Pure, No Dependencies)                      │
│ ├── Fragment, Provenance, EmbeddingConfig           │
│ └── ExcavationService (use case orchestration)      │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ DRIVEN (_out)                                       │
│ ├── CorpusPort → DuckDB (FTS + VSS)                │
│ ├── EmbeddingPort → nomic-embed-text-v1.5 (fastembed)│
│ ├── RerankerPort → MS MARCO cross-encoder (fastembed)│
│ └── SourceAdapterPort → Claude, OpenAI              │
└─────────────────────────────────────────────────────┘
```

### Key Ports

**CorpusPort** — Persistence + search:
```python
class CorpusPort(Protocol):
    def store(self, fragments: Iterable[Fragment]) -> int: ...
    def search(self, query: str, limit: int, source_kind: str | None) -> list[Fragment]: ...
    def semantic_search(self, query_embedding: list[float], ...) -> list[tuple[Fragment, float]]: ...
    def has_semantic_search(self) -> bool: ...
    def has_keyword_search(self) -> bool: ...
    def rebuild_fts_index(self) -> None: ...
    def backfill_embeddings(self, embedder_batch, batch_size, on_progress) -> int: ...
```

**EmbeddingPort** — Vector generation:
```python
class EmbeddingPort(Protocol):
    def embed(self, text: str) -> list[float]: ...
    def embed_batch(self, texts: list[str]) -> list[list[float]]: ...
    model_name: str
    dimensions: int
```

**SourceAdapterPort** — Ingest different formats:
```python
class SourceAdapterPort(Protocol):
    def can_handle(self, path: Path) -> bool: ...
    def ingest(self, path: Path) -> Iterator[Fragment]: ...
    def source_kind(self) -> str: ...
```

---

## CLI Design

### Hybrid Search (default)
```bash
memex dig "where did I decide on auth?"
memex dig "authentication" --semantic-weight 0.8
memex dig "OAuth" --no-rerank
```

### Keyword / Semantic
```bash
memex keyword "OAuth" --limit 50
memex semantic "authentication decisions" --min-score 0.5
```

### Setup
```bash
memex init                     # Global store (~/.memex/)
memex init --local             # Project-local store (./.memex/)
```

### Discovery
```bash
memex status                   # Store, config, capabilities, coverage
memex corpus                   # What's ingested
memex sources                  # Available source kinds
```

### Ingestion
```bash
memex ingest ~/Downloads/conversations.json
memex ingest export.zip --no-embed
memex backfill                 # Generate embeddings for existing fragments
memex rebuild                  # Rebuild FTS index
memex reset                    # Delete corpus, start fresh
```

### SQL Escape Hatch
```bash
memex query "SELECT * FROM fragments WHERE ..."
memex sql                      # Interactive shell
```

---

## Directory Structure

```
tools/memex/
├── pyproject.toml
├── CLAUDE.md                              # This file
├── tests/
│   ├── conftest.py                        # Shared fixtures (sample_fragments)
│   ├── test_excavation_service.py         # Service integration tests
│   ├── test_reranker.py                   # Cross-encoder tests
│   └── test_source_*.py                   # Source adapter tests
└── src/memex/
    ├── __init__.py                        # Version, status
    ├── skill.py                           # Skill documentation loader
    ├── config/
    │   └── settings.py                    # Pydantic settings (TOML + env vars + local walk-up)
    ├── composition/
    │   └── __init__.py                    # Dependency injection root
    ├── domain/
    │   ├── models.py                      # Fragment, Provenance, EmbeddingConfig
    │   ├── services/
    │   │   └── excavate.py                # ExcavationService (use case orchestration)
    │   └── ports/
    │       └── _out/
    │           ├── corpus.py              # CorpusPort
    │           ├── embedding.py           # EmbeddingPort
    │           ├── reranker.py            # RerankerPort
    │           └── source.py              # SourceAdapterPort
    └── adapters/
        ├── _in/
        │   └── cli/
        │       ├── main.py                # Rich Click CLI (driving adapter)
        │       ├── formatters.py          # Output formatting
        │       └── observability.py       # Console output helpers
        └── _out/
            ├── corpus/
            │   └── duckdb/
            │       ├── adapter.py         # DuckDB + FTS + VSS
            │       └── skill.md           # Corpus skill doc
            ├── embedding/
            │   └── fastembed_embedder.py  # nomic-embed-text-v1.5 (768-dim, ONNX)
            ├── reranking/
            │   └── fastembed_reranker.py  # MS MARCO cross-encoder (ONNX)
            └── sources/
                ├── claude_conversations/  # Claude.ai export adapter
                └── openai_conversations/  # ChatGPT export adapter
```

---

## Working Conventions

### SQL Stays in Adapters
Domain uses ports and protocols. DuckDB SQL is implementation detail in `adapters/_out/corpus/duckdb/`.

### Fragment Is the Atom
Not too small (message), not too large (conversation).
A meaningful, self-contained unit of collaborative work.

### CLI Delegates to Service
The CLI is a thin driving adapter. It calls `ExcavationService` methods, never reaches through to infrastructure directly. Power-user commands (`query`, `sql`) use `create_corpus()` for direct access.

### Source-Agnostic Domain
`source_kind` is an extensible string, not an enum. Adding a new source means one adapter, zero domain changes.

---

## Known Tech Debt

- **Config format**: TOML works for single-tool config. When cix+memex share infrastructure, consider YAML with full layered scoping (packaged → project → user → global).
- **Embedding model config**: `settings.embedding_model` exists but isn't wired into the composition root — `FastEmbedEmbedder()` is hardcoded to nomic-embed-text-v1.5. Wire the setting or remove it.

---

## References

- Vision: `/scratch/memex-vision.md`
- Guild Deliberation: `/scratch/memex-guild-deliberation.md`
- Vannevar Bush, "As We May Think" (1945)
