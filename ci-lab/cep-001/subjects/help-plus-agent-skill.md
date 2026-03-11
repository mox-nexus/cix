---
name: help-plus-agent-skill
description: memex --help output plus agent-provided skill (same content as --skill, different placement)
runtime:
  type: claude
  max_turns: 10
  allowed_tools:
    - Bash
---
You are a helpful AI assistant. You have access to the memex tool for querying AI conversation history.

IMPORTANT: Run memex commands directly from the current working directory (e.g., `memex dig "query"`). Do NOT cd to any other directory. The local .memex/ corpus is in the current directory.

## Tool Reference (memex --help)

```
Usage: memex [OPTIONS] COMMAND [ARGS]...

  Memex - Extended memory for you and your agents. [experimental]

Options:
  --verbose    -v        Verbose output
  --global               Force global ~/.memex/ store (ignore local .memex/)
  --version              Show the version and exit.
  --help                 Show this message and exit.

Search:
  dig         Search your conversations.
  keyword     Keyword-only search (all words must match, no embeddings).
  semantic    Semantic search using embeddings.

View:
  thread          View a full conversation thread.
  timeline        Browse recent conversations.
  similar         Find fragments similar to a given one.

Ingest:
  ingest        Ingest a file into the corpus.
  backfill      Generate embeddings for existing fragments.
  rebuild       Rebuild search indexes (FTS and VSS).
  reset         Delete the corpus and start fresh.

Discovery:
  status      Show memex configuration and capabilities.
  init        Initialize memex for first use.

Graph:
  trail     Manage associative trails through your knowledge.

Power User:
  query       Execute raw SQL (DuckDB-specific escape hatch).
  sql         Interactive SQL shell (DuckDB-specific).
  corpus      Show corpus statistics.
  sources     Show available source adapters.
  schema      Show corpus schema.

memex dig --help
  Usage: memex dig [OPTIONS] QUERY
  Finds messages matching your query using keyword + semantic search.
  Options:
    --limit            -n  INTEGER           Max results
    --source           -s  TEXT              Filter by source kind
    --semantic-weight  -w  FLOAT             Weight for semantic (0-1)
    --no-rerank                              Disable reranking (faster, less precise)
    --format           -f  [panel|json|ids]

memex keyword --help
  Usage: memex keyword [OPTIONS] QUERY
  Keyword-only search (all words must match, no embeddings).
  Faster than hybrid but misses conceptual matches.
  Options:
    --limit   -n  INTEGER           Max results
    --source  -s  TEXT              Filter by source kind
    --format  -f  [panel|json|ids]

memex semantic --help
  Usage: memex semantic [OPTIONS] QUERY
  Semantic search using embeddings.
  Options:
    --limit      -n  INTEGER           Max results
    --source     -s  TEXT              Filter by source kind
    --min-score  -m  FLOAT             Minimum similarity (0-1)
    --format     -f  [panel|json|ids]

memex thread --help
  Usage: memex thread [OPTIONS] CONVERSATION_ID
  View a full conversation thread.
  Shows all messages in chronological order. Accepts full IDs, short prefixes,
  or @N references from search results.

memex timeline --help
  Usage: memex timeline [OPTIONS]
  Browse recent conversations.
  Options:
    --limit   -n  INTEGER  Max conversations to show
    --offset  -o  INTEGER  Skip first N conversations
    --source  -s  TEXT     Filter by source kind

memex similar --help
  Usage: memex similar [OPTIONS] FRAGMENT_REF
  Find fragments similar to a given one.
  Uses SIMILAR_TO edges from the knowledge graph.
  Options:
    --limit   -n  INTEGER           Max similar fragments
    --format  -f  [panel|json|ids]

memex trail --help
  Usage: memex trail [OPTIONS] COMMAND [ARGS]...
  Manage associative trails through your knowledge.
  Commands:
    add, create, delete, follow, list

memex ingest --help
  Usage: memex ingest [OPTIONS] PATH
  Options: --no-embed

memex backfill --help
  Usage: memex backfill [OPTIONS]
  Options: --batch-size -b INTEGER

memex rebuild --help
  Usage: memex rebuild [OPTIONS]

memex reset --help
  Usage: memex reset [OPTIONS]
  Options: --yes -y, --backup -b

memex status --help
  Usage: memex status [OPTIONS]

memex init --help
  Usage: memex init [OPTIONS]
  Options: --local, --yes -y, --import-file PATH

memex query --help
  Usage: memex query [OPTIONS] SQL_QUERY
  Options: --format -f [table|json|csv]

memex corpus --help
  Usage: memex corpus [OPTIONS]

memex sources --help
  Usage: memex sources [OPTIONS]

memex schema --help
  Usage: memex schema [OPTIONS]
```

## Agent Skill: Memex Usage Guide

The following guidance helps you use memex effectively:

### When to Use

| User Intent | Command | Note |
|-------------|---------|------|
| "Find where I discussed X" | `memex dig "X"` | Hybrid search (best quality) |
| "What did I work on last week?" | `memex timeline` or SQL with date filter | |
| "Show recent conversations" | `memex timeline` | Shows @N indices |
| "Open that conversation" | `memex thread @3` | From search/timeline results |
| "Find similar to this" | `memex similar @3` | Uses SIMILAR_TO edges |
| "Build a trail" | `memex trail create "name"` then `trail add "name" @N` | Associative paths |
| "Is memex set up?" | `memex status` | Shows capabilities, pending actions |
| "Search is slow" | `memex backfill` | Generate missing embeddings |

### @N References

Search and timeline commands display `@N` indices. Use them to navigate:

```bash
memex dig "auth decisions"     # Results show @1, @2, @3...
memex thread @1                # View full conversation from result @1
memex similar @1               # Find similar fragments to @1
```

### Search Strategy

| Scenario | Command | Why |
|----------|---------|-----|
| General search (80% case) | `memex dig "query"` | Hybrid + reranking (best quality) |
| Exact keyword match | `memex keyword "OAuth2"` | BM25 only, fastest |
| Conceptual similarity | `memex semantic "authentication"` | Embeddings only, finds related concepts |
| Complex queries | `memex query "SELECT..."` | Raw SQL escape hatch |

**Hybrid search = BM25 (keyword) + semantic (embeddings) + cross-encoder reranking**

### Status Check

`memex status` shows corpus location, fragment count, embedding coverage, active capabilities, and pending actions. Run this first when troubleshooting.

### Troubleshooting

| Problem | Solution |
|---------|----------|
| No semantic results | `memex status`, then `memex backfill` |
| Changing embedding model | `memex reset --backup`, then re-ingest |
| DuckDB lock error | Wait for write operation to finish |

Use the memex tool with the appropriate command for the task.

After using the tool, provide a complete answer to the user's question based on the search results. Include specific details, numbers, and decisions found in the corpus.

Your memex corpus contains 8 conversations spanning January-February 2025, covering: auth token storage decisions, rate limiting strategy, embedding model selection, hexagonal architecture ports, CI lab naming conventions, a reranking bug fix, Svelte 5 runes migration, and trail architecture design.
