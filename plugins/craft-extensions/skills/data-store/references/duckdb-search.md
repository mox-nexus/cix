# DuckDB Search Capabilities (2026)

## Full-Text Search (FTS Extension)

### Status: Experimental but Stable

The FTS extension implements Okapi BM25 scoring:
- Term frequency (TF)
- Inverse document frequency (IDF)
- Document length normalization

### Index Creation

```sql
-- Install and load
INSTALL fts;
LOAD fts;

-- Create index with options
PRAGMA create_fts_index(
    'fragments',           -- table name
    'id',                  -- document ID column
    'content',             -- text column to index
    stemmer = 'english',   -- Snowball stemmer
    stopwords = 'english', -- built-in stopword list
    ignore = '[^a-zA-Z0-9]',
    strip_accents = 1,
    lower = 1
);
```

### Searching

```sql
-- Basic search
SELECT *, fts_main_fragments.match_bm25(id, 'search terms') AS score
FROM fragments
WHERE score IS NOT NULL
ORDER BY score DESC
LIMIT 20;

-- Multiple columns (title + content)
PRAGMA create_fts_index('docs', 'id', 'title', 'content');
```

### Critical Limitation

**Index does NOT auto-update.** After INSERT/UPDATE/DELETE:

```sql
-- Must rebuild manually
PRAGMA drop_fts_index('fragments');
PRAGMA create_fts_index('fragments', 'id', 'content');
```

**Tip:** Rebuild after bulk ingest operations.

---

## Vector Similarity Search (VSS Extension)

### Status: Experimental, Not Production-Ready

Built on HNSW (Hierarchical Navigable Small Worlds) via usearch library.

### Supported Metrics

- `l2sq` — Euclidean distance squared
- `cosine` — Cosine distance (1 - similarity)
- `ip` — Inner product

### Index Creation

```sql
-- Install and load
INSTALL vss;
LOAD vss;

-- Add embedding column
ALTER TABLE fragments ADD COLUMN embedding FLOAT[768];

-- Create HNSW index
CREATE INDEX idx_embedding ON fragments
    USING HNSW (embedding)
    WITH (metric = 'cosine');
```

### Searching

```sql
SELECT *,
    array_cosine_similarity(embedding, ?::FLOAT[768]) as similarity
FROM fragments
WHERE embedding IS NOT NULL
ORDER BY similarity DESC
LIMIT 20;
```

### Performance Characteristics

| Metric | Observed |
|--------|----------|
| Index build | Fast on pre-populated tables |
| Point query | ~23s overhead (high!) |
| Index lookup | 0.15s once warmed |
| Memory | Index must fit in RAM |

### Limitations

1. **High per-query overhead** — DuckDB's query layer, not HNSW itself
2. **RAM-bound** — No disk spillover for index
3. **Deletes marked, not removed** — Index can grow stale
4. **Scaling limit** — ~50-100M vectors max practical

### When to Graduate to Dedicated Vector DB

| Condition | Action |
|-----------|--------|
| >50M vectors | Weaviate, Qdrant, Pinecone |
| <100ms p99 required | Dedicated vector DB |
| Multi-region needed | Managed service |
| Personal corpus <10K | DuckDB is fine |

---

## Hybrid Search Implementation

### Score Normalization (Important)

BM25 scores: 0 to 100+
Cosine similarity: 0 to 1

**Never blend directly:**
```sql
-- ❌ WRONG
score = 0.7 * bm25_score + 0.3 * cosine_score  -- BM25 dominates
```

### Reciprocal Rank Fusion (RRF)

```sql
-- ✅ Correct approach
WITH keyword_ranked AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY bm25_score DESC) as kw_rank
    FROM fts_results
),
semantic_ranked AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY similarity DESC) as sem_rank
    FROM vss_results
)
SELECT
    COALESCE(k.id, s.id) as id,
    COALESCE(1.0/(k.kw_rank + 60), 0) +
    COALESCE(1.0/(s.sem_rank + 60), 0) as rrf_score
FROM keyword_ranked k
FULL OUTER JOIN semantic_ranked s ON k.id = s.id
ORDER BY rrf_score DESC
LIMIT 20;
```

### Alternative: Min-Max Normalization

```sql
-- Normalize scores to 0-1 range
WITH normalized AS (
    SELECT id,
        (bm25_score - MIN(bm25_score) OVER()) /
        (MAX(bm25_score) OVER() - MIN(bm25_score) OVER()) as norm_bm25,
        similarity as norm_semantic
    FROM combined_results
)
SELECT id, 0.6 * norm_semantic + 0.4 * norm_bm25 as hybrid_score
FROM normalized
ORDER BY hybrid_score DESC;
```

RRF preferred — simpler, more robust.

---

## Bulk Write Performance

### Drop Indexes Before Bulk Operations

DuckDB's HNSW index maintains an in-memory graph. During bulk UPDATEs (e.g., backfilling embeddings), the index incrementally incorporates each new vector — O(n log n) memory growth that can OOM on large datasets.

**Pattern: drop → write → rebuild**

```sql
-- Before bulk write
DROP INDEX IF EXISTS idx_embedding;

-- Bulk operations here (INSERT, UPDATE, etc.)
-- CHECKPOINT every ~1000 rows to flush WAL
CHECKPOINT;

-- After bulk write
CREATE INDEX idx_embedding ON fragments
    USING HNSW (embedding)
    WITH (metric = 'cosine');
```

Building the index once from scratch is both faster and uses a fraction of the memory vs. incremental maintenance. This is the same principle as PostgreSQL's `DROP INDEX` before `COPY` or Elasticsearch's `refresh_interval: -1`.

### Memory and WAL Management

```sql
-- Cap DuckDB memory when running alongside other processes
SET memory_limit = '2GB';
```

DuckDB defaults to 80% of system RAM. In shared environments (e.g., running inside Claude Code), this causes contention. Set an explicit limit.

**WAL accumulation:** DuckDB buffers write-ahead log entries in memory. During tight update loops, auto-checkpoint may not trigger between batches. Force periodic checkpoints to bound memory:

```sql
-- Every ~1000 rows during bulk operations
CHECKPOINT;
```

### FTS Index Rebuild

FTS indexes don't auto-update (see above). After any bulk ingest:

```sql
PRAGMA drop_fts_index('fragments');
PRAGMA create_fts_index('fragments', 'id', 'content',
    stemmer='english', stopwords='english');
```

---

## Production Recommendations

### Phase 1: Keyword Search
- BM25 via FTS extension (not naive ILIKE)
- Works well for small-to-medium corpus

### Phase 2: Hybrid Search
1. Add FTS index for keyword search
2. Add embedding column + VSS index
3. Implement RRF hybrid in service layer

### Phase 3: Scale Out
- If >50K documents: Consider dedicated vector DB (Weaviate, Qdrant)
- If <100ms latency required: Move to PostgreSQL + pgvector or dedicated VDB

---

## Sources

- [DuckDB Full-Text Search Extension](https://duckdb.org/docs/stable/core_extensions/full_text_search)
- [DuckDB VSS Extension](https://duckdb.org/docs/stable/core_extensions/vss)
- [Search in DuckDB - MotherDuck Blog](https://motherduck.com/blog/search-using-duckdb-part-3/)
- [A Hybrid information retriever with DuckDB](https://aetperf.github.io/2024/05/30/A-Hybrid-information-retriever-with-DuckDB.html)
- [DuckSearch - Efficient BM25](https://github.com/lightonai/ducksearch)
