---
name: Memex
description: >
  This skill should be used when the user asks to "search my conversations",
  "find where I discussed", "what did I decide about", "what did I work on",
  "recall that conversation about", "import conversations", "ingest my files",
  "ingest directory", "create a trail", "find similar", "show recent",
  "search my notes", "search my docs", "dig through my history",
  "what's in my memex", or mentions searching AI conversation history,
  text files, research notes, PDFs, conversation memory, or knowledge trails.
---

# Memex

Extended memory for you and your agents. Search across ingested conversations
(Claude, ChatGPT, Gemini), text files, PDFs, and source code with hybrid
retrieval.

## When to Use

| User Intent | Command |
|-------------|---------|
| "Find where I discussed X" | `memex dig "X"` |
| "Import my conversations" | `memex ingest ~/Downloads/export.zip` |
| "Ingest my research notes" | `memex ingest ~/research/` |
| "What did I work on last week?" | `memex timeline` |
| "Open that conversation" | `memex thread @3` |
| "Find similar to this" | `memex similar @3` |
| "What's connected to this?" | `memex traverse @3` |
| "Build a trail of related findings" | `memex trail create "name"` |
| "Is memex set up?" | `memex status` |
| "Set up memex" | `memex init` |
| "Set up for this project" | `memex init --local` |

## @N References

Search and timeline results display `@N` indices for navigation:

```bash
memex dig "auth decisions"     # Results show @1, @2, @3...
memex thread @1                # View full conversation
memex similar @1               # Find semantically similar fragments

memex timeline                 # Shows @1, @2, @3...
memex thread @5                # Jump to conversation #5
```

Conversation ID prefixes also work: `memex thread 66e1524a`

## Search Strategy

| Scenario | Command |
|----------|---------|
| General search (start here) | `memex dig "query"` |
| Exact keyword match | `memex keyword "OAuth2"` |
| Conceptual similarity | `memex semantic "authentication"` |
| Complex filters | `memex query "SELECT..."` |

`dig` combines keyword + semantic + reranking. Default for all search.

Tuning (rarely needed): `memex dig "query" --semantic-weight 0.8`

## Ingestion

### Supported Sources

| Source | Formats |
|--------|---------|
| Claude.ai | `.json` or `.zip` export |
| ChatGPT | `.json` or `.zip` export (including sharded) |
| Gemini | Google Takeout `.zip` (My Activity HTML) |
| Text files | `.md`, `.txt`, `.rst`, `.py`, `.js`, `.ts`, `.rs`, `.go`, `.sh`, `.sql`, and more |
| Documents | `.pdf`, `.docx` |
| Data | `.json`, `.jsonl`, `.yaml`, `.toml`, `.csv` |

### Large Imports

For large exports (1000+ conversations), separate storage from embedding:

```bash
memex ingest ~/exports/large-export.zip --no-embed   # Fast (minutes)
memex backfill                                        # Slower (run separately)
```

Re-ingesting the same export is safe — existing fragments are skipped.

## Command Reference

| Command | Purpose |
|---------|---------|
| **Search** | |
| `memex dig "<query>"` | Hybrid search (keyword + semantic + reranking) |
| `memex keyword "<query>"` | Keyword-only search |
| `memex semantic "<query>"` | Embedding-only search |
| **Navigate** | |
| `memex thread <id or @N>` | View full conversation |
| `memex timeline` | Browse recent conversations |
| `memex similar @N` | Find similar fragments |
| `memex traverse @N` | Multi-hop graph traversal |
| **Trails** | |
| `memex trail create "name"` | Create a named trail |
| `memex trail add "name" @N` | Add fragment to trail |
| `memex trail follow "name"` | Walk a trail |
| `memex trail list` | List all trails |
| `memex trail search "query"` | Search trails by name/description |
| `memex trail delete "name"` | Delete a trail |
| **Ingest** | |
| `memex ingest <file or dir>` | Parse, store, embed, and index |
| `memex ingest <path> --no-embed` | Store without embedding (fast) |
| `memex backfill` | Generate missing embeddings |
| `memex build-edges` | Build similarity edges from embeddings |
| `memex rebuild` | Rebuild search indexes |
| `memex reset` | Delete corpus, start fresh |
| **Discovery** | |
| `memex status` | Corpus stats, capabilities, pending actions |
| `memex init` | First-time setup |
| `memex init --local` | Project-local store in CWD |
| **Power User** | |
| `memex query "<sql>"` | Raw SQL query |
| `memex sql` | Interactive SQL shell |
| `memex corpus` | Corpus statistics |
| `memex schema` | Database schema |

## Multi-Store

Memex uses `.memex/` directories like `.git/` — walks up from CWD to find the
active store. Local `.memex/` overrides global `~/.memex/`. No flags needed.

```bash
memex init                # Global store (~/.memex/)
memex init --local        # Project-local store (./.memex/)
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No semantic results | `memex status` → check embedding coverage → `memex backfill` |
| Lock error | Another memex process is writing. Wait or check `ps aux \| grep memex` |
| Ingest interrupted | `memex backfill` to finish embeddings |
| Changing embedding model | `memex reset`, then re-ingest |

## Key Behaviors

- **Backfill is idempotent** — safe to interrupt and restart, resumes where it left off
- **FOLLOWS edges** are auto-computed on ingest (temporal ordering)
- **SIMILAR_TO edges** require explicit `memex build-edges` after embedding
- **Graph traversal** follows chains of edges across fragments via `memex traverse`
- **Fragment metadata** (title, page, file) is queryable via SQL: `metadata->>'title'`
- **Single writer** — only one ingest/backfill at a time; reads work concurrently

## References

For detailed patterns, consult `memex --skill -r <name>`:

| Reference | Content |
|-----------|---------|
| `query` | SQL patterns, output formats |
| `ingest` | Supported formats, directory ingest, large imports |
| `schema` | Full schema, index details |
| `embeddings` | Backfill patterns, model configuration |
| `trails` | Trail usage patterns, examples |
| `use-cases` | Agent memory, research notes, code search |
