# Query Reference

## Search Commands

### dig (hybrid - 80% case)

Best quality. Uses BM25 + semantic + cross-encoder reranking.

```bash
memex dig "auth implementation"
memex dig "rate limiting" --limit 50
memex dig "hexagonal" --source claude_conversations
memex dig "OAuth" --semantic-weight 0.8   # Favor semantic
memex dig "OAuth" --no-rerank             # Skip reranking (faster)
```

Options:
- `--limit, -n` - Max results (default: 20)
- `--source, -s` - Filter by source kind
- `--semantic-weight, -w` - Balance keyword vs semantic (default: 0.6, range: 0-1)
- `--no-rerank` - Disable cross-encoder reranking
- `--format, -f` - Output format: panel, json, ids

### keyword (BM25 only)

Fastest. Matches exact terms.

```bash
memex keyword "OAuth2" --limit 50
memex keyword "hexagonal architecture" --source claude_conversations
```

### semantic (embeddings only)

Finds conceptually similar content even without keyword overlap.

```bash
memex semantic "authentication decisions"
memex semantic "rate limiting" --min-score 0.5
```

Options:
- `--min-score, -m` - Minimum similarity threshold (default: 0.3)

## SQL Escape Hatch

### query (single SQL)

```bash
memex query "SELECT COUNT(*) FROM fragments"
memex query "SELECT * FROM fragments WHERE role='user' LIMIT 5" --format json
memex query "SELECT * FROM fragments ORDER BY timestamp DESC LIMIT 10" --format csv
```

Output formats: `table` (default), `json`, `csv`

### sql (interactive shell)

```bash
memex sql
memex> SELECT source_kind, COUNT(*) FROM fragments GROUP BY source_kind
memex> exit
```

## SQL Patterns

```sql
-- Full-text search (BM25 via FTS)
SELECT * FROM fragments WHERE fts_main_fragments.match_bm25(id, 'auth') IS NOT NULL

-- Case-insensitive pattern match (slower, no index)
SELECT * FROM fragments WHERE content ILIKE '%pattern%'

-- Date range
SELECT * FROM fragments WHERE timestamp BETWEEN '2026-01-01' AND '2026-01-31'

-- By source
SELECT * FROM fragments WHERE source_kind = 'claude_conversations'

-- Conversation thread
SELECT * FROM fragments WHERE conversation_id = 'uuid' ORDER BY timestamp

-- Aggregate stats
SELECT
    source_kind,
    COUNT(*) as fragments,
    COUNT(DISTINCT conversation_id) as conversations
FROM fragments
GROUP BY source_kind

-- Embedding coverage
SELECT
    COUNT(*) FILTER (WHERE embedding IS NOT NULL) as with_embedding,
    COUNT(*) as total
FROM fragments
```

## Output Formats

| Format | Use Case |
|--------|----------|
| `panel` | Human reading (default for dig) |
| `table` | Human reading (default for query) |
| `json` | Piping to other tools |
| `ids` | Piping fragment IDs |
| `csv` | Spreadsheet export |
