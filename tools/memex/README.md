# memex

Extended memory for you and your agents. Excavates and connects historical human-AI collaboration artifacts across Claude, OpenAI, and other sources with hybrid search.

Named for Vannevar Bush's 1945 vision of an "enlarged intimate supplement to memory."

## When to Use

- Looking back on past decisions: "where did I decide on auth?"
- Finding patterns across conversations
- Building a searchable corpus of collaboration history
- Running SQL queries against your AI interaction data

## Quick Start

```bash
# Ingest a Claude.ai export
memex ingest ~/Downloads/claude-export.json

# Search with hybrid retrieval (keyword + semantic + reranking)
memex dig "authentication decisions"

# View what's in your corpus
memex corpus

# Power-user SQL escape hatch
memex query "SELECT COUNT(*) FROM fragments"
memex sql  # Interactive shell
```

## Design

- **`dig` is the default** — hybrid search that just works (BM25 + semantic + cross-encoder reranking)
- **SQL for power users** — `query` and `sql` for when you need full control
- **Source-agnostic** — Claude, OpenAI, more to come. Adding a source = one adapter
- **Local-first** — corpus stored at `~/.memex/corpus.duckdb`, project-local with `.memex/`

## Search Modes

| Command | Method | Best For |
|---------|--------|----------|
| `memex dig` | Hybrid (BM25 + semantic + rerank) | General search — start here |
| `memex keyword` | BM25 full-text | Exact terms, code identifiers |
| `memex semantic` | Vector similarity | Conceptual, fuzzy matching |
| `memex query` | Raw SQL | Complex filters, aggregation |

## License

MIT
