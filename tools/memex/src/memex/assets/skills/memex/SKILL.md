# Memex Skill

Extended memory for you and your agents. Query AI conversations from Claude.ai, ChatGPT, and other sources.

## When to Use

| User Intent | Command | Note |
|-------------|---------|------|
| "Find where I discussed X" | `memex dig "X"` | Hybrid search (best quality) |
| "What did I work on last week?" | `memex timeline` or SQL with date filter | |
| "Show recent conversations" | `memex timeline` | Shows @N indices |
| "Open that conversation" | `memex thread @3` | From search/timeline results |
| "Find similar to this" | `memex similar @3` | Uses knowledge graph |
| "Build a trail" | `memex trail create "name"` then `trail add "name" @N` | Associative paths |
| "Is memex set up?" | `memex status` | Shows capabilities, pending actions |
| "Search is slow" | `memex backfill` | Generate missing embeddings |
| "Set up for this project" | `memex init --local` | Creates .memex/ in CWD |

## @N References

Search and timeline commands display `@N` indices. Use them to navigate:

```bash
memex dig "auth decisions"     # Results show @1, @2, @3...
memex thread @1                # View full conversation from result @1
memex similar @1               # Find similar fragments to @1

memex timeline                 # Shows @1, @2, @3...
memex thread @5                # View conversation #5 from timeline
```

Conversation ID prefixes also work: `memex thread 66e1524a` (8+ chars recommended)

## Search Strategy

| Scenario | Command | Why |
|----------|---------|-----|
| General search (80% case) | `memex dig "query"` | Hybrid + reranking (best quality) |
| Fast search | `memex dig "query" --no-rerank` | Skips reranking, still hybrid |
| Exact keyword match | `memex keyword "OAuth2"` | BM25 only, fastest |
| Conceptual similarity | `memex semantic "authentication"` | Embeddings only, finds related concepts |
| Complex queries | `memex query "SELECT..."` | Raw SQL escape hatch |

**Hybrid search = BM25 (keyword) + semantic (embeddings) + cross-encoder reranking**

Tuning (rarely needed): `memex dig "query" --semantic-weight 0.8` (default: 0.6)

## Command Reference

| Command | Purpose |
|---------|---------|
| **Search** | |
| `memex dig "<query>"` | Hybrid search (BM25 + semantic + reranking) |
| `memex keyword "<query>"` | Keyword-only (BM25) |
| `memex semantic "<query>"` | Embedding-only |
| **Navigate** | |
| `memex thread <id or @N>` | View full conversation |
| `memex timeline` | Browse recent conversations |
| `memex timeline --source openai` | Filter by source |
| `memex similar @N` | Find similar fragments via graph |
| **Trails** | |
| `memex trail create "name"` | Create a named trail |
| `memex trail add "name" @N` | Add fragment to trail |
| `memex trail follow "name"` | Walk a trail |
| `memex trail list` | List all trails |
| `memex trail delete "name"` | Delete a trail |
| **Ingest** | |
| `memex ingest <file>` | Import with embeddings (default) |
| `memex ingest <file> --no-embed` | Fast import, keyword search only |
| `memex backfill` | Generate embeddings for existing fragments |
| `memex rebuild` | Rebuild search indexes |
| `memex reset` | Delete corpus and start fresh |
| **Discovery** | |
| `memex status` | Config, capabilities, pending actions |
| `memex init` | First-time global setup |
| `memex init --local` | Project-local store in CWD |
| **Power User** | |
| `memex query "<sql>"` | Raw SQL (DuckDB) |
| `memex sql` | Interactive SQL shell |
| `memex corpus` | Corpus statistics |
| `memex sources` | Available source adapters |
| `memex schema` | Database schema |
| `memex --skill` | Output this skill for Claude |
| `memex --skill -r <name>` | Output specific reference |

## Status Check

`memex status` shows corpus location, fragment count, embedding coverage, active capabilities (BM25, semantic, reranking), and pending actions.

Run this first when troubleshooting.

## Multi-Store (Convention over Config)

Memex uses `.memex/` directories like `.git/` — walks up from CWD to find the active store.

### Precedence (highest wins)

1. `MEMEX_*` env vars
2. Local `.memex/` (walk up from CWD)
3. Global `~/.memex/config.toml`
4. Defaults (`~/.memex/corpus.duckdb`)

### Setup

```bash
memex init              # Global store at ~/.memex/ (user-level, default)
memex init --local      # Project-local store at ./.memex/ (directory-level)
```

Local `.memex/` structure (add to .gitignore):

```
.memex/
├── config.toml         # Optional local config overrides
├── corpus.duckdb       # Project-local corpus
└── last_results.json   # @N register (auto-managed)
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No semantic results | `memex status` (check embedding coverage), then `memex backfill` |
| Changing embedding model | `memex reset --backup`, then `memex ingest <file>` |
| Fast import, embed later | `memex ingest <file> --no-embed`, then `memex backfill` |

## Key Facts

- **Embedding model**: nomic-embed-text-v1.5 (768-dim), via fastembed (ONNX, ~285MB, no torch)
- **Reranking model**: Xenova/ms-marco-MiniLM-L-6-v2 (cross-encoder)
- **Full-text**: DuckDB FTS with BM25
- **Vector search**: DuckDB VSS with HNSW
- **FOLLOWS edges**: auto-computed on ingest (no manual step needed)
- **Fusion**: RRF (k=60)

## References

For detailed patterns, use `memex --skill -r <name>`:

| Reference | Content |
|-----------|---------|
| query | SQL query patterns, output formats |
| ingest | Ingest workflow, embedding options |
| schema | Full schema, index details |
| embeddings | Model selection, dimension mismatch, backfill patterns |
