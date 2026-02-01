# Query Reference

## dig (80% case)

```bash
memex dig "auth implementation"
memex dig "rate limiting" --limit 50
memex dig "hexagonal" --source claude_conversations
```

## query (20% SQL escape hatch)

```bash
memex query "SELECT COUNT(*) FROM fragments"
memex query "SELECT * FROM fragments WHERE role='user' LIMIT 5" --format json
memex query "SELECT * FROM fragments ORDER BY timestamp DESC LIMIT 10" --format csv
```

## Output formats

- `--format table` (default)
- `--format json`
- `--format csv`

## SQL patterns

```sql
-- Full-text search (case-insensitive)
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
```
