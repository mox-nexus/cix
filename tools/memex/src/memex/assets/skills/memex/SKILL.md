---
name: Memex
description: >
  This skill should be used when the user asks to "search my conversations",
  "find where I discussed", "what did I decide about", "what did I work on",
  "set up memex", "import conversations", "ingest export", "ingest text files",
  "ingest directory", "create a trail", "find similar", "show recent",
  "memex timeline", "memex status", "dig through conversations",
  "agent memory", "search my notes", "search my docs", or mentions
  searching AI conversation history, text files, research notes,
  conversation memory, or knowledge trails.
---

# Memex Skill

Extended memory for you and your agents. Ingest text files, conversation exports, PDFs, and source code into a searchable corpus with hybrid search (BM25 + semantic + reranking).

## When to Use

| User Intent | Command | Note |
|-------------|---------|------|
| "Ingest my research notes" | `memex ingest ~/research/` | Recurses directory, finds all text/md/pdf/code |
| "Search my docs for X" | `memex dig "X"` | Hybrid search (best quality) |
| "Import conversations" | `memex ingest ~/Downloads/export.zip` | Claude.ai, ChatGPT exports |
| "Find where I discussed X" | `memex dig "X"` | Works across all ingested sources |
| "What did I work on last week?" | `memex timeline` or SQL with date filter | |
| "Show recent" | `memex timeline` | Shows @N indices |
| "Open that conversation" | `memex thread @3` | From search/timeline results |
| "Find similar to this" | `memex similar @3` | SIMILAR_TO edges (embedding similarity) |
| "Build a trail" | `memex trail create "name"` then `trail add "name" @N` | Associative paths |
| "Is memex set up?" | `memex status` | Shows capabilities, pending actions |
| "Search is slow" | `memex backfill` | Generate missing embeddings |
| "Set up memex" | `memex init` | Guided wizard (first run, TTY) |
| "Set up for this project" | `memex init --local` | Creates .memex/ in CWD |
| "Connect related fragments" | `memex build-edges` | Builds SIMILAR_TO edges from embeddings |

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
| `memex ingest <file>` | Parse, store, embed, and index in one step |
| `memex ingest <dir>` | Recurse directory, import matching files |
| `memex backfill` | Finish embedding if ingest was interrupted |
| `memex build-edges` | Build SIMILAR_TO edges (requires embeddings) |
| `memex build-edges -t 0.7 -k 10` | Custom threshold and max edges per fragment |
| `memex rebuild` | Rebuild search indexes |
| `memex reset` | Delete corpus and start fresh |
| **Discovery** | |
| `memex status` | Config, capabilities, pending actions |
| `memex init` | Guided first-time setup (wizard on TTY) |
| `memex init --yes` | Silent setup (CI/scripts, no prompts) |
| `memex init --import-file <path>` | Setup + immediate import |
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
memex init                                       # Guided wizard (detects exports, offers import)
memex init --yes                                 # Silent (CI/scripts, no prompts)
memex init --import-file ~/Downloads/conv.json   # Setup + immediate import
memex init --local                               # Project-local store at ./.memex/
```

On first run with a TTY, `memex init` launches an interactive wizard that detects conversation exports in ~/Downloads and ~/Desktop, offers source selection (Claude/ChatGPT), and runs inline ingest. Use `--yes` to skip all prompts.

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
| Ingest interrupted mid-embedding | `memex backfill` to finish |
| Backfill killed / OOM | Tune ONNX resources (see below) |
| DuckDB lock error during backfill | Normal — DuckDB holds an exclusive write lock. Wait for backfill to finish. Check with `ps aux \| grep memex` |
| Any command fails with `Conflicting lock` | Another memex process is running (backfill, ingest). Only one writer at a time. |

## Resource Tuning (Backfill / Embedding)

ONNX Runtime memory scales with `batch_size × seq_len²`. Before running `memex backfill` on large corpora (10K+ fragments), check available RAM and tune if needed.

**Defaults work for 16-64GB machines.** Only tune for constrained environments.

| Machine RAM | Set before backfill |
|-------------|---------------------|
| 64GB+ | Defaults are fine |
| 16-32GB | Defaults are fine |
| 8-16GB | `MEMEX_ONNX_BATCH_SIZE=2 MEMEX_ONNX_THREADS=1` |
| <8GB / CI | `MEMEX_ONNX_BATCH_SIZE=1 MEMEX_ONNX_THREADS=1` |

Or set permanently in `~/.memex/config.toml`:

```toml
[embedding]
onnx_batch_size = 2
onnx_threads = 1
```

**Diagnosis**: If `memex backfill` exits silently (SIGKILL, exit 137), it's OOM. Lower `onnx_batch_size` first (biggest lever), then `onnx_threads`.

## Key Facts

- **Embedding model**: nomic-embed-text-v1.5 (768-dim), via fastembed (ONNX, ~285MB, no torch)
- **Reranking model**: Xenova/ms-marco-MiniLM-L-6-v2 (cross-encoder)
- **Full-text**: DuckDB FTS with BM25
- **Vector search**: DuckDB VSS with HNSW
- **FOLLOWS edges**: auto-computed on ingest (no manual step needed)
- **SIMILAR_TO edges**: built via `memex build-edges` (requires `memex backfill` first)
- **Fusion**: RRF (k=60)
- **Backfill is idempotent**: `memex backfill` resumes from where it left off (`WHERE embedding IS NULL`). Safe to interrupt and restart.
- **Backfill is memory-safe**: drops HNSW index before bulk writes, checkpoints periodically, rebuilds index after. DuckDB capped at 2GB.
- **DuckDB is single-writer**: only one process can write at a time. During backfill/ingest, all other memex commands will fail with a lock error. This is expected — wait or check `ps aux | grep memex`.

## Use Cases

### Agent memory — ingest a directory of text files

```bash
memex init --local                    # Project-local store at ./.memex/
memex ingest ~/research/              # Recurse directory, import all matching files
memex dig "authentication patterns"   # Search across everything
```

Supported: `.md`, `.txt`, `.rst`, `.py`, `.js`, `.ts`, `.rs`, `.go`, `.json`, `.jsonl`, `.yaml`, `.toml`, `.pdf`, `.docx`, `.csv`, `.log`, `.sql`, `.html`, `.css`, `.xml`, `.sh`, and more.

Text files split by markdown headings. PDFs split by page. DOCX by heading paragraphs. Files without headings become a single fragment.

### Conversation history — Claude.ai / ChatGPT exports

```bash
memex ingest ~/Downloads/claude-export.zip
memex ingest ~/Downloads/conversations.json    # ChatGPT export
memex dig "what did I decide about auth?"
```

### Project-local knowledge base

```bash
cd myproject/
memex init --local                              # .memex/ in project root
memex ingest docs/ src/                         # Index docs and source code
memex dig "error handling"                      # Search project knowledge
```

Local `.memex/` is isolated — won't mix with global store. Add `.memex/` to `.gitignore`.

## References

For detailed patterns, use `memex --skill -r <name>`:

| Reference | Content |
|-----------|---------|
| query | SQL query patterns, output formats |
| ingest | Ingest workflow, supported formats, directory ingest |
| schema | Full schema, index details |
| embeddings | Model details, dimension mismatch, backfill patterns |
| trails | Trail usage patterns, examples, design tips |
| use-cases | Specific use cases: agent memory, research notes, code search |
