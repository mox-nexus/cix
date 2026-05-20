# Schema Reference

## fragments

| Column | Type | Description |
|--------|------|-------------|
| id | VARCHAR (PK) | Fragment identifier, from source |
| conversation_id | VARCHAR | Groups messages in conversation |
| role | VARCHAR | 'user' or 'assistant' |
| content | TEXT | Message text |
| timestamp | TIMESTAMPTZ | When created |
| source_kind | VARCHAR | 'claude_conversations', 'openai', 'plaintext', etc. |
| source_id | VARCHAR | Unique ID within source |
| metadata | JSON | Structured info (title, page, file, line) — optional |
| embedding | FLOAT[N] | Vector embedding (N = model dimensions) — optional |

## edges

| Column | Type | Description |
|--------|------|-------------|
| source_id | VARCHAR (PK) | Source fragment |
| target_id | VARCHAR (PK) | Target fragment |
| edge_type | VARCHAR (PK) | FOLLOWS, SIMILAR_TO, REFERENCES, DERIVED_FROM, etc. |
| weight | FLOAT | Edge strength (default 1.0) |
| metadata | JSON | Edge-specific data — optional |
| created_at | TIMESTAMPTZ | When edge was created |

## trails

| Column | Type | Description |
|--------|------|-------------|
| id | VARCHAR (PK) | Trail UUID |
| name | VARCHAR (UNIQUE) | Human-readable trail name |
| description | VARCHAR | What the trail captures |
| created_at | TIMESTAMPTZ | When trail was created |

## trail_entries

| Column | Type | Description |
|--------|------|-------------|
| trail_id | VARCHAR (PK, FK→trails) | Parent trail |
| position | INTEGER (PK) | Order within trail |
| fragment_id | VARCHAR (FK→fragments) | Referenced fragment |
| note | VARCHAR | Annotation — why this fragment matters here |
| added_at | TIMESTAMPTZ | When added |

## _memex_meta

| Column | Type | Description |
|--------|------|-------------|
| key | VARCHAR (PK) | Config key |
| value | VARCHAR | Config value |
| updated_at | TIMESTAMPTZ | Last modified |

Keys: `schema_version`, `embedding_model`, `embedding_dimensions`.

## Indexes

| Index | Purpose |
|-------|---------|
| `idx_fragments_timestamp` | Date range queries |
| `idx_fragments_conversation` | Thread queries |
| `idx_fragments_source` | Source filtering |
| `idx_edges_source` | Edge traversal from source |
| `idx_edges_target` | Edge traversal from target |
| `idx_edges_type` | Edge type filtering |
| `idx_trail_entries_trail` | Trail entry lookup |
| FTS index | BM25 keyword search on content |
| HNSW index | Cosine similarity on embeddings |

## Property Graph (DuckPGQ)

When the `duckpgq` extension is available, a SQL/PGQ property graph view is created:

```sql
-- Pattern matching via SQL/PGQ
FROM GRAPH_TABLE (memex_graph
    MATCH (a:frag)-[e:rel]->(b:frag)
    COLUMNS (a.id AS src, e.edge_type, b.id AS dst, e.weight)
)
WHERE e.edge_type = 'SIMILAR_TO';

-- Multi-hop traversal
FROM GRAPH_TABLE (memex_graph
    MATCH (a:frag)-[e1:rel]->(b:frag)-[e2:rel]->(c:frag)
    COLUMNS (a.id AS start_id, b.id AS mid_id, c.id AS end_id)
);
```

## Edge Type Constants

Extensible strings (not enum). Common values:

| Constant | Value | Built by |
|----------|-------|----------|
| `EDGE_FOLLOWS` | `FOLLOWS` | `memex build-edges` / auto on ingest |
| `EDGE_SIMILAR_TO` | `SIMILAR_TO` | `memex build-edges` (requires embeddings) |
| `EDGE_REFERENCES` | `REFERENCES` | User-defined |
| `EDGE_DERIVED_FROM` | `DERIVED_FROM` | User-defined |

## Source Kinds

| Value | Description |
|-------|-------------|
| `claude_conversations` | Claude.ai exports (.zip, .json) |
| `openai` | ChatGPT exports (.json) |
| `plaintext` | Text files, PDFs, DOCX, source code |

## Embedding Details

| Model | Dimensions | Backend |
|-------|------------|---------|
| nomic-ai/nomic-embed-text-v1.5 | 768 | fastembed (ONNX) |

Check current model and coverage: `memex status`

**Important**: Changing models requires `memex reset` — dimensions must match across the corpus.

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

-- Fragments with metadata
SELECT id, metadata->>'title' as title, metadata->>'file' as file
FROM fragments
WHERE metadata IS NOT NULL
LIMIT 20;

-- Edge distribution
SELECT edge_type, COUNT(*), ROUND(AVG(weight), 3) as avg_weight
FROM edges
GROUP BY edge_type;

-- Trails with entry counts
SELECT t.name, t.description, COUNT(te.fragment_id) as entries
FROM trails t
LEFT JOIN trail_entries te ON t.id = te.trail_id
GROUP BY t.id, t.name, t.description
ORDER BY t.created_at DESC;

-- Fragments by date
SELECT DATE_TRUNC('month', timestamp) as month, COUNT(*)
FROM fragments
GROUP BY month
ORDER BY month;
```
