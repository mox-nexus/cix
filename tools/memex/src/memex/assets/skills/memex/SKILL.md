# Memex Skill

Query collaborative intelligence artifacts from Claude.ai, ChatGPT, and other sources.

## When to Use

- "Find where I discussed X" → `memex dig "X"`
- "What did I work on last week?" → `memex dig "last week"` or SQL with date filter
- "Show me code about Y" → `memex dig "Y" --limit 50`
- "How many conversations?" → `memex query "SELECT COUNT(*) FROM fragments"`

## Commands

| Command | Purpose |
|---------|---------|
| `memex dig "<query>"` | Search fragments (80% case) |
| `memex query "<sql>"` | Raw SQL (20% power-user) |
| `memex corpus` | Show stats |
| `memex schema` | Show tables/columns |
| `memex sources` | Available source adapters |

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

## Common Queries

```sql
-- Count by source
SELECT source_kind, COUNT(*) FROM fragments GROUP BY source_kind

-- Recent conversations
SELECT DISTINCT conversation_id, MAX(timestamp) as last_msg
FROM fragments GROUP BY conversation_id ORDER BY last_msg DESC LIMIT 10

-- Search with date filter
SELECT * FROM fragments
WHERE content ILIKE '%auth%' AND timestamp > '2026-01-01'
ORDER BY timestamp DESC LIMIT 20
```

## References

- `references/query.md` - SQL query patterns
- `references/ingest.md` - Adding new sources
- `references/schema.md` - Full schema details
