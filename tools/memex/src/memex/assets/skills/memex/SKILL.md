# Memex Skill

Extended memory for you and your agents. Query AI conversations from Claude.ai, ChatGPT, and other sources.

## When to Use

| User Intent | Command |
|-------------|---------|
| "Find where I discussed X" | `memex dig "X"` |
| "What did I work on last week?" | `memex dig "last week"` or SQL with date filter |
| "Show me code about Y" | `memex dig "Y" --limit 50` |
| "How many conversations?" | `memex query "SELECT COUNT(*) FROM fragments"` |
| "Is memex set up correctly?" | `memex status` |
| "I imported but search is slow" | `memex backfill` (generate embeddings) |

## Search Strategy

`dig` uses hybrid search by default: BM25 (keyword) + semantic (embeddings) + cross-encoder reranking.

| Scenario | Command | Why |
|----------|---------|-----|
| General search (80% case) | `memex dig "query"` | Best quality: hybrid + reranking |
| Fast search | `memex dig "query" --no-rerank` | Skips reranking, still hybrid |
| Exact keyword match | `memex keyword "OAuth2"` | Only BM25, fastest |
| Conceptual similarity | `memex semantic "authentication"` | Only embeddings, finds related concepts |
| Complex queries | `memex query "SELECT..."` | Raw SQL escape hatch |

### Tuning Hybrid Search

```bash
memex dig "query" --semantic-weight 0.8  # Favor semantic (default: 0.6)
memex dig "query" --semantic-weight 0.3  # Favor keyword
memex dig "query" --no-rerank            # Disable reranking (faster)
```

## Commands

### Search

| Command | Purpose |
|---------|---------|
| `memex dig "<query>"` | Hybrid search: BM25 + semantic + reranking |
| `memex keyword "<query>"` | Keyword-only (BM25) |
| `memex semantic "<query>"` | Embedding-only |

### Ingest

| Command | Purpose |
|---------|---------|
| `memex ingest <file>` | Import with embeddings (default) |
| `memex ingest <file> --no-embed` | Import fast, keyword search only |
| `memex backfill` | Generate embeddings for existing fragments |
| `memex rebuild` | Rebuild search indexes |
| `memex reset` | Delete corpus and start fresh |

### Discovery

| Command | Purpose |
|---------|---------|
| `memex status` | Configuration, capabilities, pending actions |
| `memex corpus` | Corpus statistics |
| `memex sources` | Available source adapters |
| `memex schema` | Database schema |
| `memex init` | First-time setup |

### Power User

| Command | Purpose |
|---------|---------|
| `memex query "<sql>"` | Raw SQL (DuckDB) |
| `memex sql` | Interactive SQL shell |
| `memex --skill` | Output this skill for Claude |
| `memex --skill -r query` | Output specific reference |

## Status Check

`memex status` shows:
- Corpus location and fragment count
- Embedding coverage (how many have embeddings)
- Active capabilities (BM25, semantic, reranking)
- Pending actions (e.g., "run backfill")

Run this first when troubleshooting.

## Schema

```sql
fragments (
    id VARCHAR PRIMARY KEY,
    conversation_id VARCHAR,
    role VARCHAR,           -- 'user' or 'assistant'
    content TEXT,           -- the actual message
    timestamp TIMESTAMPTZ,
    source_kind VARCHAR,    -- 'claude_conversations', 'openai', etc.
    source_id VARCHAR
)
```

## Common Patterns

### No semantic results?

```bash
memex status              # Check embedding coverage
memex backfill            # Generate missing embeddings
```

### Changing embedding model?

```bash
memex reset --backup      # Backup and delete corpus
memex ingest <file>       # Re-import with new model
```

### Quick import, embed later?

```bash
memex ingest <file> --no-embed  # Fast import
memex backfill                  # Embed when ready
```

## References

For detailed patterns, use `memex --skill -r <name>`:

| Reference | Command | Content |
|-----------|---------|---------|
| query | `memex --skill -r query` | SQL query patterns, output formats |
| ingest | `memex --skill -r ingest` | Ingest workflow, embedding options |
| schema | `memex --skill -r schema` | Full schema, index details |
| embeddings | `memex --skill -r embeddings` | Model selection, dimension mismatch, backfill patterns |
