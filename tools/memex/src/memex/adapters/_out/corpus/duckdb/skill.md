# DuckDB Corpus Skill

Query collaborative intelligence artifacts stored in DuckDB.

## When to Use

- Search fragments: `corpus.search("auth")`
- Get conversation: `corpus.find_by_conversation("uuid")`
- Raw SQL (DuckDB-specific): `corpus.query_sql("SELECT ...")`

## Schema

```sql
fragments (
    id VARCHAR PRIMARY KEY,
    conversation_id VARCHAR,
    role VARCHAR,           -- 'user' or 'assistant'
    content TEXT,           -- message text
    timestamp TIMESTAMPTZ,
    source_kind VARCHAR,    -- 'claude_conversations', 'openai', etc.
    source_id VARCHAR
)
```

## SQL Patterns (DuckDB-specific)

```sql
-- Full-text search
SELECT * FROM fragments WHERE content ILIKE '%pattern%'

-- Date range
SELECT * FROM fragments WHERE timestamp BETWEEN '2026-01-01' AND '2026-01-31'

-- By source
SELECT * FROM fragments WHERE source_kind = 'claude_conversations'

-- Conversation thread
SELECT * FROM fragments WHERE conversation_id = 'uuid' ORDER BY timestamp

-- Aggregate stats
SELECT source_kind, COUNT(*) as count
FROM fragments GROUP BY source_kind
```

## Notes

- `query_sql()` is DuckDB-specific, not part of CorpusPort
- Other corpus backends (Postgres, Parquet) may not support raw SQL
- Use port methods (`search`, `find_by_conversation`) for portable code
