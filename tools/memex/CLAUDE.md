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

## Performance Patterns

### Bulk Write: Drop Index → Write → Rebuild

DuckDB's HNSW index grows O(n log n) in memory when maintained during bulk UPDATEs. For backfill operations (embedding 50K+ fragments), **always** drop the HNSW index first, write in batches with periodic `CHECKPOINT`, then rebuild.

This is implemented in `DuckDBCorpus.backfill_embeddings()` — it calls `_drop_hnsw_index()` before the loop and `_create_hnsw_index()` in a `finally` block. The same principle applies to any future bulk write operation.

Also set `memory_limit = '2GB'` on the DuckDB connection to prevent contention with the host process (e.g., Claude Code).

### DuckDB Single-Process Lock

DuckDB takes a **process-level exclusive lock** on disk-based files. When any process opens a read-write connection, no other process can connect — not even `read_only=True`. This is a [known limitation](https://github.com/duckdb/duckdb/discussions/14676); intra-process MVCC supports concurrent readers + single writer, but cross-process is fully exclusive.

During `backfill` or `ingest`, all other memex commands (including `status`, `dig`) will fail with `Conflicting lock is held`. Don't try to work around it — wait for the write operation to finish. Check with `ps aux | grep memex`.

### Rich Progress Over Manual \\r

Never use `console.print(f"\\r...", end="")` for progress. Rich emits full ANSI escape sequences per call, which GPU-accelerated terminals (Ghostty) buffer indefinitely. Use `rich.progress.Progress` — it rate-limits updates and handles single-line overwrite properly.

### ONNX Resource Model

ONNX Runtime pads all sequences in a batch to the max length, then allocates O(batch * seq_len^2) attention tensors. With real corpus text (avg ~2500 chars), the default batch_size=256 can require ~90GB for 100 documents — instant SIGKILL on most machines.

Two knobs control ONNX memory, exposed via `Settings` (env vars / config.toml):

| Setting | Env Var | Default | Effect |
|---------|---------|---------|--------|
| `onnx_batch_size` | `MEMEX_ONNX_BATCH_SIZE` | 4 | Docs per inference call. Peak RAM scales linearly. |
| `onnx_threads` | `MEMEX_ONNX_THREADS` | 2 | ONNX inter-op threads. Each thread allocates a memory arena. |

Flow: `Settings` (Pydantic) → `composition/get_embedder()` → `FastEmbedEmbedder(onnx_batch_size=..., onnx_threads=...)`. The embedder is a plain adapter — it receives config through constructor injection, never reaches back to settings.

Resource profiles (approximate peak during backfill):

| Profile | batch_size | threads | Peak RAM | Target |
|---------|-----------|---------|----------|--------|
| Conservative | 2 | 1 | ~2GB | 8GB machines, CI |
| Default | 4 | 2 | ~5GB | 16-64GB machines |
| Aggressive | 8 | 4 | ~10GB | 64GB+ with fast backfill |

The SKILL.md documents these for Claude-as-operator to diagnose and tune.

---

## Streaming Pipeline Pattern (Pending Refactor)

The backfill pipeline currently works (OOM-safe, streaming writes) but uses imperative loops with mutable counters. Next step: refactor to functional composition per `craft-tools:python-hex` reference.

### Target Shape

```
source → transform → sink → tap(side effects) → terminal
```

Each stage is a generator. Nothing materializes beyond its batch boundary.

### Current → Target

**Current** (`duckdb/adapter.py` — `backfill_embeddings`):
```python
for batch in self._unembedded_batches(batch_size):
    ids, contents = zip(*batch)
    for frag_id, embedding in zip(ids, embedder_stream(list(contents))):
        self._write_embedding(frag_id, embedding)
        updated += 1
        if updated % 1000 == 0: ...
        if on_progress: ...
```

**Target:**
```python
# Source: flat stream from DB via iter(callable, sentinel)
rows = chain.from_iterable(iter(self._fetch_batch, []))

# Transform: batch → unzip → embed → re-zip (zero accumulation)
embedded = self._embed_rows(rows, embedder, batch_size)

# Sink + side effects as stream operators
pipeline = map(self._write_one, embedded)
pipeline = tap_every(pipeline, 1000, lambda _: self._checkpoint())
if on_progress:
    c = count(1)
    pipeline = tap(pipeline, lambda _: on_progress(next(c), total))

# Terminal
return sum(1 for _ in pipeline)
```

### Port Change Required

`EmbeddingPort.embed_stream` should accept `Iterator[str]` (not `list[str]`). Stream is the primitive; single/batch are free functions derived from it. See `craft-tools:python-hex` port example.

### Helpers Needed

- `tap(iterator, fn)` — observe each element without consuming
- `tap_every(iterator, n, fn)` — side effect every n-th element
- Location: `domain/` or a small `streaming.py` util — these are domain-agnostic pipeline operators

### When

Apply after current backfill completes. Pure refactor — same behavior, different shape. Verify with test.

---

## Pre-1.0 TODO

- [ ] **FP pipeline refactor** — Apply streaming pipeline pattern to backfill (see above). Includes port signature change (`Iterator[str]`).
- [ ] **Wire `embedding_model` setting** — `settings.embedding_model` exists but composition root hardcodes nomic-embed-text-v1.5. Wire through or remove.
- [ ] **Verify `build_similar_edges` index usage** — self-join may be O(N^2) if DuckDB doesn't use HNSW index. Run EXPLAIN to confirm.
- [ ] **Trails** — persistence (separate file per trail in `.memex/trails/`), sharing (trail file IS the artifact), interactive visualization (HTML artifact).
- [ ] **Config format migration path** — TOML works for single-tool config. When cix+memex share infrastructure, consider YAML with layered scoping.
- [ ] **Test coverage** — backfill, ONNX resource paths, settings precedence, enhanced Claude adapter extraction.
- [ ] **Reranker resource controls** — similar ONNX knobs may be needed for the cross-encoder.
- [ ] **Code quality pass** — Pydantic where appropriate (data models, port contracts), type annotations, docstring consistency across adapters.
- [ ] **Clean up stale config** — `embedding_model: str = "minilm"` default is wrong (we use nomic). Reconcile settings with reality.

---

## References

- Vision: `/scratch/memex-vision.md`
- Guild Deliberation: `/scratch/memex-guild-deliberation.md`
- Vannevar Bush, "As We May Think" (1945)
