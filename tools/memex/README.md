# memex

Extended memory for you and your agents.

Ingest text, documents, and conversation exports. Search with hybrid retrieval (BM25 + semantic + reranking). Navigate via knowledge graph and curated trails.

## Quick Start

```bash
memex init                                    # First-time setup
memex ingest ~/research/                      # Ingest a directory of text files
memex ingest ~/Downloads/claude-export.zip    # Or a Claude/ChatGPT export
memex dig "authentication decisions"          # Hybrid search
```

## What It Ingests

| Source | Formats |
|--------|---------|
| Text files | `.md`, `.txt`, `.rst`, `.py`, `.js`, `.ts`, `.rs`, `.go`, `.sh`, `.sql`, and more |
| Documents | `.pdf`, `.docx` |
| Claude.ai | `.json` or `.zip` export |
| ChatGPT | `.json` or `.zip` export |

Point `memex ingest` at a file or directory — it auto-detects the format, splits intelligently (markdown by headings, PDF by pages, DOCX by heading paragraphs), embeds, and indexes in one step.

## Search

| Command | Method | Best For |
|---------|--------|----------|
| `memex dig` | Hybrid (BM25 + semantic + rerank) | General search — start here |
| `memex keyword` | BM25 full-text | Exact terms, code identifiers |
| `memex semantic` | Vector similarity | Conceptual, fuzzy matching |
| `memex query` | Raw SQL | Complex filters, aggregation |

## Design

- **Local-first** — DuckDB corpus at `~/.memex/`, project-local with `memex init --local`
- **One command to ingest** — parses, stores, embeds, and indexes
- **Source-agnostic** — adding a source = one adapter, zero domain changes
- **Agent-friendly** — Python API (`from memex.api import Memex`), daemon for concurrent access

## License

MIT
