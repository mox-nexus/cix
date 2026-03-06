# Memex

> Extended memory for you and your agents

Memex retrieves and connects historical human-AI collaboration artifacts across heterogeneous sources. Named for Vannevar Bush's 1945 vision of an "enlarged intimate supplement to memory."

---

## Tooling

| Task | Use | Never |
|------|-----|-------|
| Python | `uv` | pip, conda, poetry, raw python |
| Run scripts | `uv run` | python directly |
| Add deps | `uv add` | pip install |
| JS (if needed) | `bun` | npm, yarn, node |

---

## What Memex Is

Historical artifacts, not live streams. Excavation, not observation.

- Query conversations from Claude, OpenAI
- Hybrid search: BM25 keyword + semantic (embeddings) + cross-encoder reranking
- Graph: FOLLOWS (temporal) + SIMILAR_TO (semantic) edges between fragments
- Trails: curated, annotated paths through fragments
- Power-user SQL (20%): escape hatch for complex queries

## What Memex Is NOT

- Not live observability or log viewing
- Not Claude-specific (source-agnostic via adapters)

## Design Principles

Follows cix Design Principles (see root CLAUDE.md):

- **Defaults for Most (80%)**: `memex dig "..."` — hybrid search, just works
- **Complexity for Few (20%)**: `memex query "SELECT..."` — SQL escape hatch
- **Pit of Success**: `dig` is primary, SQL is explicit opt-out
- **Transparent Abstractions**: Show what was found, why, from where
- **Convention over Config**: Local `.memex/` overrides global — no flags needed

---

## Configuration Resolution

Convention-over-config (like `.git/`). A local `.memex/` directory in or above the CWD becomes the active workspace.

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

cd myproject/
memex dig "auth"      # Searches local .memex/corpus.duckdb
cd myproject/src/     # Walk-up finds ../myproject/.memex/
memex dig "auth"      # Still uses myproject's local store

cd ~
memex dig "auth"      # Falls back to ~/.memex/corpus.duckdb
```

Resolution happens in `config/settings.py`. The rest of the stack receives a `Path` and is workspace-agnostic.

---

## Domain Ontology

### Entities

| Entity | What It Is |
|--------|------------|
| **Fragment** | Recovered unit of CI — THE canonical entity |
| **Provenance** | Source-agnostic origin (source_kind, source_id, timestamp) |
| **EmbeddingConfig** | Embedding contract (model_name, dimensions) — domain invariant |
| **EmbeddingCoverage** | Coverage stats (with_embeddings, total) |
| **TrailSummary** | Trail metadata (name, description, entry_count) |
| **CorpusStats** | Corpus-level aggregate (fragments, conversations, time range) |
| **EdgeTypeStats** | Per-edge-type count and average weight |

### Source Kinds

Extensible strings (not enum). Common values:

```python
SOURCE_CLAUDE_CONVERSATIONS = "claude_conversations"
SOURCE_OPENAI = "openai"
SOURCE_GEMINI = "gemini"  # adapter not yet implemented
SOURCE_CUSTOM = "custom"
```

---

## Hexagonal Architecture

```
┌─────────────────────────────────────────────────────┐
│ DRIVING (_in)                                       │
│ ├── CLI: memex dig, memex ingest, memexd start      │
│ └── API: from memex.api import Memex                │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ DOMAIN (Pure, No Dependencies)                      │
│ ├── Fragment, Provenance, EmbeddingConfig, ...      │
│ └── ExcavationService (use case orchestration)      │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ DRIVEN (_out)                                       │
│ ├── CorpusPort   → DuckDB (local) / Remote (daemon) │
│ ├── GraphPort    → DuckDB edges (FOLLOWS, SIMILAR)  │
│ ├── TrailPort    → DuckDB trails                    │
│ ├── EmbeddingPort → nomic-embed-text-v1.5 (ONNX)   │
│ ├── RerankerPort  → MS MARCO cross-encoder (ONNX)   │
│ └── SourceAdapterPort → Claude, OpenAI              │
└─────────────────────────────────────────────────────┘
```

### Port Split

The original mega-port was split into three focused protocols:

| Port | Responsibility | Methods |
|------|---------------|---------|
| **CorpusPort** | Storage, search, embeddings, metadata | `store`, `search`, `semantic_search`, `backfill_embeddings`, `rebuild_search_index`, ... |
| **GraphPort** | Fragment relationships | `find_similar`, `build_follows_edges`, `build_similar_edges`, `edge_stats` |
| **TrailPort** | Curated paths | `create_trail`, `add_to_trail`, `get_trail`, `list_trails`, `delete_trail` |

`DuckDBCorpus` implements all three. `RemoteCorpusAdapter` (daemon client) also implements all three. The service holds them separately: `service.corpus`, `service.graph`, `service.trails`.

### API Facade

`memex.api.Memex` is the stable entry point for agents and libraries:

```python
from memex.api import Memex

with Memex() as m:
    results = m.search("auth decisions")
    trails = m.list_trails()
    similar = m.find_similar("fragment-id")
```

Accepts `direct=True` to skip daemon auto-detect (for write-heavy operations).

### Daemon (`memexd`)

Solves DuckDB's single-process lock. One process owns the database, clients connect via Unix socket.

```bash
memexd start           # Double-fork daemon
memexd start -f        # Foreground (debugging)
memexd stop
memexd status
```

- JSON-RPC over length-prefixed Unix socket
- `ThreadPoolExecutor(max_workers=16)` for concurrent reads
- `fcntl.flock` on PID file (no TOCTOU race)
- `os.umask(0o077)` around socket bind (no chmod race)
- `MEMEX_NO_DAEMON=1` kill switch

Auto-detect: `create_service()` checks for running daemon. If found, returns `RemoteCorpusAdapter`. If not, direct DuckDB. Transparent to callers.

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
memex rebuild                  # Rebuild search index
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
│   ├── test_corpus.py                     # DuckDB corpus adapter tests
│   ├── test_api.py                        # API facade tests
│   ├── test_daemon.py                     # Daemon protocol + socket tests
│   ├── test_excavation_service.py         # Service integration tests
│   ├── test_models.py                     # Domain model tests
│   ├── test_settings.py                   # Config resolution tests
│   ├── test_reranker.py                   # Cross-encoder tests
│   └── test_source_adapters.py            # Source adapter tests
└── src/memex/
    ├── __init__.py                        # Version
    ├── api.py                             # Public API facade (Memex class)
    ├── skill.py                           # Skill documentation loader
    ├── config/
    │   └── settings.py                    # Pydantic settings (TOML + env vars + walk-up)
    ├── composition/
    │   └── __init__.py                    # Dependency injection root
    ├── daemon/
    │   ├── cli.py                         # memexd start/stop/status
    │   ├── server.py                      # Unix socket server + thread pool
    │   ├── protocol.py                    # JSON-RPC dispatcher
    │   └── wire.py                        # Length-prefixed framing
    ├── domain/
    │   ├── __init__.py                    # Domain re-exports
    │   ├── models.py                      # Fragment, Provenance, EmbeddingConfig, ...
    │   ├── services/
    │   │   └── excavate.py                # ExcavationService (use case orchestration)
    │   └── ports/
    │       └── _out/
    │           ├── corpus.py              # CorpusPort (storage + search)
    │           ├── graph.py               # GraphPort (edges)
    │           ├── trail.py               # TrailPort (curated paths)
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
            │   ├── duckdb/
            │   │   ├── adapter.py         # DuckDB + FTS + VSS
            │   │   └── skill.md           # Corpus skill doc
            │   └── remote.py              # Daemon client adapter
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
Not too small (message), not too large (conversation). A meaningful, self-contained unit of collaborative work.

### CLI Delegates to Service
The CLI is a thin driving adapter. It calls `ExcavationService` methods and accesses ports via `service.corpus`, `service.graph`, `service.trails`. Power-user commands (`query`, `sql`) use `create_corpus()` for direct access.

### Port Names Are Implementation-Agnostic
Port methods use domain language: `rebuild_search_index()` not `rebuild_fts_index()`, `has_semantic_search()` not `has_hnsw()`. Implementation details (BM25, HNSW, DuckDB) stay in adapters.

### Source-Agnostic Domain
`source_kind` is an extensible string, not an enum. Adding a new source means one adapter, zero domain changes.

---

## Performance Patterns

### Bulk Write: Drop Index → Write → Rebuild

DuckDB's HNSW index grows O(n log n) in memory when maintained during bulk UPDATEs. For backfill operations (embedding 50K+ fragments), **always** drop the HNSW index first, write in batches with periodic `CHECKPOINT`, then rebuild.

Implemented in `DuckDBCorpus.backfill_embeddings()` — calls `_drop_hnsw_index()` before the loop and `_create_hnsw_index()` in a `finally` block.

Also set `memory_limit = '2GB'` on the DuckDB connection to prevent contention with the host process (e.g., Claude Code).

### DuckDB Single-Process Lock

DuckDB takes a **process-level exclusive lock** on disk-based files. No other process can connect — not even `read_only=True`. This is why the daemon exists.

During `backfill` or `ingest`, all other memex commands fail with `Conflicting lock is held`. Don't try to work around it — wait for the write operation to finish. Check with `ps aux | grep memex`.

### HNSW Index Activation

`build_similar_edges` fetches each fragment's embedding, then queries with a literal vector parameter. This ensures DuckDB activates the HNSW index. A self-join (`FROM fragments f1, fragments f2`) bypasses it and falls to O(n²) brute force.

### Rich Progress Over Manual \\r

Never use `console.print(f"\\r...", end="")` for progress. Rich emits full ANSI escape sequences per call, which GPU-accelerated terminals (Ghostty) buffer indefinitely. Use `rich.progress.Progress` — it rate-limits updates and handles single-line overwrite properly.

### ONNX Resource Model

ONNX Runtime pads all sequences in a batch to the max length, then allocates O(batch * seq_len^2) attention tensors. With real corpus text (avg ~2500 chars), the default batch_size=256 can require ~90GB for 100 documents — instant SIGKILL on most machines.

Two knobs control ONNX memory, exposed via `Settings` (env vars / config.toml):

| Setting | Env Var | Default | Effect |
|---------|---------|---------|--------|
| `onnx_batch_size` | `MEMEX_ONNX_BATCH_SIZE` | 4 | Docs per inference call. Peak RAM scales linearly. |
| `onnx_threads` | `MEMEX_ONNX_THREADS` | 2 | ONNX inter-op threads. Each thread allocates a memory arena. |

Resource profiles (approximate peak during backfill):

| Profile | batch_size | threads | Peak RAM | Target |
|---------|-----------|---------|----------|--------|
| Conservative | 2 | 1 | ~2GB | 8GB machines, CI |
| Default | 4 | 2 | ~5GB | 16-64GB machines |
| Aggressive | 8 | 4 | ~10GB | 64GB+ with fast backfill |

---

## Pre-1.0 TODO

- [ ] **FP pipeline refactor** — Streaming pipeline pattern for backfill. Includes `EmbeddingPort.embed_stream` accepting `Iterator[str]`.
- [ ] **Wire `embedding_model` setting** — composition root hardcodes nomic-embed-text-v1.5. Wire through or remove.
- [ ] **Reranker resource controls** — similar ONNX knobs may be needed for the cross-encoder.
- [ ] **Clean up stale config** — `embedding_model: str = "minilm"` default is wrong (we use nomic).

---

## References

- Vision: `/scratch/memex-vision.md`
- Guild Deliberation: `/scratch/memex-guild-deliberation.md`
- Vannevar Bush, "As We May Think" (1945)
