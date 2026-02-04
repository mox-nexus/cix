# Schema Reference

## fragments (main table)

| Column | Type | Description |
|--------|------|-------------|
| id | VARCHAR | Primary key, from source |
| conversation_id | VARCHAR | Groups messages in conversation |
| role | VARCHAR | 'user' or 'assistant' |
| content | TEXT | Message text |
| timestamp | TIMESTAMPTZ | When message was created |
| source_kind | VARCHAR | 'claude_conversations', 'openai', etc. |
| source_id | VARCHAR | Unique ID within source |
| embedding | FLOAT[N] | Vector embedding (N = model dimensions) |

## raw_fragments (immutable archive)

Stores original JSON for rebuild capability. Don't query directly.

## Indexes

| Index | Purpose |
|-------|---------|
| `idx_fragments_timestamp` | Date range queries |
| `idx_fragments_conversation` | Thread queries |
| `idx_fragments_source` | Source filtering |
| FTS index | BM25 keyword search on content |
| VSS (HNSW) index | Semantic similarity on embeddings |

## Source Kinds

| Value | Description |
|-------|-------------|
| `claude_conversations` | Claude.ai exports |
| `openai` | ChatGPT exports |
| `claude_code_logs` | Claude Code session logs (future) |
| `gemini` | Google Gemini (future) |

## Embedding Details

Embeddings are stored as fixed-dimension float arrays. Dimension depends on model:

| Model | Dimensions |
|-------|------------|
| all-MiniLM-L6-v2 (default) | 384 |
| text-embedding-ada-002 | 1536 |
| voyage-large-2 | 1024 |

Check current model: `memex status`

**Important**: Changing models requires `memex reset` - dimensions must match.

## Useful Queries

```sql
-- Embedding coverage
SELECT
    COUNT(*) FILTER (WHERE embedding IS NOT NULL) as with_embedding,
    COUNT(*) as total
FROM fragments;

-- Source breakdown
SELECT source_kind, COUNT(*) FROM fragments GROUP BY source_kind;

-- Recent conversations
SELECT DISTINCT conversation_id, MAX(timestamp) as last_msg
FROM fragments
GROUP BY conversation_id
ORDER BY last_msg DESC
LIMIT 10;

-- Fragments by date
SELECT DATE_TRUNC('month', timestamp) as month, COUNT(*)
FROM fragments
GROUP BY month
ORDER BY month;

-- Longest conversations
SELECT conversation_id, COUNT(*) as msg_count
FROM fragments
GROUP BY conversation_id
ORDER BY msg_count DESC
LIMIT 10;
```
