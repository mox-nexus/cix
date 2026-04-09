# Changelog

All notable changes to memex will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2026-03-18

### Added

- **Fragment.metadata** — optional `dict[str, Any]` for structured data (title, page, file, line). JSONL entries get `{"line": N, ...raw_fields}`, PDFs get `{"page": N}`, all plaintext gets `{"title": ..., "file": ...}`.
- **Graph traversal** — `traverse(fragment_id, max_hops, edge_type)` for multi-hop reachability via recursive CTE. Returns `(Fragment, hops, edge_type)` tuples.
- **Searchable trails** — `search_trails(query)` finds trails by name/description (ILIKE). `trails_for_fragment(fragment_id)` returns all trails containing a given fragment.
- **Edge metadata** — edges table gains optional `metadata` JSON column for edge-level context.
- **Edge type constants** — `EDGE_FOLLOWS`, `EDGE_SIMILAR_TO`, `EDGE_REFERENCES`, `EDGE_DERIVED_FROM` as extensible strings in domain models.
- **DuckPGQ property graph** — SQL/PGQ `MATCH` queries via `memex sql` for power-user graph pattern matching. Installed from community extensions, graceful fallback if unavailable.
- **Schema migration** — `_ensure_column()` helper adds new columns to existing corpora on connection. Existing databases upgrade automatically.

### Changed

- **Adapter split** — monolithic `DuckDBCorpus` refactored into four focused classes sharing one `DuckDBConnection`:
  - `DuckDBConnection` — schema, extensions, lifecycle
  - `DuckDBCorpusAdapter` — CorpusPort (store, search, backfill)
  - `DuckDBGraphAdapter` — GraphPort (edges, traverse, similar)
  - `DuckDBTrailAdapter` — TrailPort (trails, search)
  - `DuckDBCorpus` remains as thin facade — zero breaking changes to callers.

### Fixed

- **Daemon dispatcher** — `search_trails` and `trails_for_fragment` handlers were defined but not registered in the JSON-RPC method table. Calls over the daemon returned `METHOD_NOT_FOUND`. Now wired correctly.

## [0.2.1] - 2026-03-01

### Added

- **Plaintext adapter** — ingest `.md`, `.txt`, `.rst`, `.pdf`, `.docx`, source code (`.py`, `.js`, `.ts`, `.rs`, `.go`, etc.), `.json`, `.jsonl`, `.yaml`, `.toml`, `.csv`, `.log`, and more.
- **JSONL structural parsing** — each JSON line becomes a fragment with curated metadata, not treated as plain text.
- **Daemon auto-start** — `ensure_daemon()` starts memexd automatically on first read command. Transparent to callers.
- **ONNX GPU auto-detect** — CoreML on macOS, CUDA on Linux, CPU fallback. No manual config.
- **ONNX noise suppression** — CoreML stderr warnings silenced via fd-level redirect.

### Changed

- **Streaming backfill** — generator-based pipeline replaces list-based. Memory stays flat regardless of corpus size.
- **Length-sorted ONNX batching** — groups similar-length texts to reduce padding waste.

## [0.2.0] - 2026-02-15

### Added

- **Hexagonal architecture** — domain (Fragment, Provenance, ports) fully separated from adapters (DuckDB, CLI, daemon).
- **Three ports** — `CorpusPort` (storage + search), `GraphPort` (edges), `TrailPort` (curated paths). Split from original mega-port.
- **Daemon (`memexd`)** — Unix socket server solving DuckDB single-process lock. JSON-RPC protocol, thread pool, PID file locking.
- **API facade** — `memex.api.Memex` as stable entry point for agents and libraries.
- **Trails** — named, ordered, annotated paths through fragments. `create`, `add`, `follow`, `list`, `delete`.
- **Graph edges** — `FOLLOWS` (temporal ordering) and `SIMILAR_TO` (embedding cosine similarity).
- **Convention-over-config** — `.memex/` directory walk-up, multi-store pattern, env var overrides.
- **Interactive init wizard** — detects exports in ~/Downloads, offers source selection, runs inline ingest.

## [0.1.0] - 2025-11-15

### Added

- **Hybrid search** — BM25 keyword + semantic embeddings + cross-encoder reranking, fused via RRF (k=60).
- **Embedding model** — nomic-embed-text-v1.5 (768-dim) via fastembed (ONNX, no torch dependency).
- **Reranking model** — Xenova/ms-marco-MiniLM-L-6-v2 cross-encoder.
- **DuckDB storage** — FTS (BM25) + VSS (HNSW) in single engine.
- **Source adapters** — Claude.ai export (.zip, .json) and ChatGPT export (.json).
- **CLI** — `memex dig`, `memex ingest`, `memex backfill`, `memex query`, `memex sql`, `memex status`.
- **@N references** — search/timeline results indexed for navigation (`memex thread @3`, `memex similar @1`).
- **Skill system** — `memex --skill` outputs skill doc for Claude, `--skill -r <name>` for specific references.

[Unreleased]: https://github.com/mox-nexus/cix/compare/memex-v0.3.0...HEAD
[0.3.0]: https://github.com/mox-nexus/cix/compare/memex-v0.2.1...memex-v0.3.0
[0.2.1]: https://github.com/mox-nexus/cix/compare/memex-v0.2.0...memex-v0.2.1
[0.2.0]: https://github.com/mox-nexus/cix/compare/memex-v0.1.0...memex-v0.2.0
[0.1.0]: https://github.com/mox-nexus/cix/releases/tag/memex-v0.1.0
