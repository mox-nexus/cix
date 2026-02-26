# Storage Backends for Search (2026)

## Decision Framework

```
What's your scale?
├── <100K vectors → DuckDB, SQLite + vec, LanceDB (embedded)
├── 100K-50M → PostgreSQL + pgvector (recommended)
├── 50M-1B → Qdrant, Weaviate, Milvus (dedicated VDBs)
└── >1B → Milvus distributed, ClickHouse
```

---

## Storage Selection Matrix

| Backend | Scale | Latency | Cost | Ops Complexity | Best For |
|---------|-------|---------|------|----------------|----------|
| **DuckDB** | <10M | 1-5s | $0 | Minimal | Analytics, local ML, batch |
| **SQLite + vec** | <100K | 100ms+ | $0 | Minimal | Embedded apps, mobile |
| **LanceDB** | <50M | 10-100ms | $0 | Low | Python apps, multimodal |
| **PostgreSQL + pgvector** | <50M | 10-50ms | $100/mo | Medium | **General purpose (recommended)** |
| **Supabase/Neon** | <50M | 10-50ms | $25-100/mo | Low | Serverless + auth bundled |
| **Qdrant** | 10M-1B | 10-50ms | $150/mo+ | High | Low-latency, complex filtering |
| **Weaviate** | 10M-1B | 30-50ms | $150/mo+ | High | Enterprise hybrid search |
| **Milvus** | 100M-10B | 40-80ms | $200/mo+ | Very High | Massive scale |
| **Pinecone** | 100M-1B | 30ms p99 | $100/mo+ | None | Zero ops, startup speed |
| **ClickHouse** | 100M-1B | 50-500ms | $200/mo+ | Medium-High | Analytics + vectors |

---

## When to Use What

### DuckDB (Embedded, Personal Use)

**Use when:**
- Personal/single-user application
- Batch processing, not real-time
- Analytics queries alongside search
- <10M vectors

**Avoid when:**
- Concurrent users (OLAP-optimized, not OLTP)
- Real-time updates
- <100ms latency required

**Gotchas:**
- FTS index doesn't auto-update (rebuild after changes)
- VSS extension still experimental
- Can't handle concurrent writes well

### PostgreSQL + pgvector

**Use when:**
- 95% of applications (seriously)
- Need ACID transactions
- Hybrid search (text + vector)
- Team already knows Postgres

**Why it wins 2026:**
- pgvectorscale extension: scales to 50M+ vectors
- Supabase/Neon: instant setup, free tier
- No vendor lock-in
- Full SQL power

**Gotchas:**
- HNSW index needs careful tuning
- Cold cache = slow first queries (47-minute warmup observed)
- Not as fast as dedicated VDBs at scale

### Dedicated Vector DBs (Qdrant, Weaviate, Milvus)

**Use when:**
- >50M vectors
- Complex filtering during search
- Sub-50ms latency at scale
- Real-time updates

**Selection within category:**
- **Qdrant**: Simplest ops, best filtering, lower latency
- **Weaviate**: Enterprise features, hybrid built-in
- **Milvus**: Highest throughput, most complex

---

## Cost Analysis (10M vectors, 1000 QPS)

| Backend | Monthly Cost |
|---------|-------------|
| PostgreSQL (Supabase) | $100 (fixed) |
| Neon (serverless) | $60-150 |
| Pinecone | $500-2000 |
| Qdrant (managed) | $432 |
| Weaviate (managed) | $300 |
| Qdrant (self-hosted AWS) | $1200-1800 |

**Break-even:** Self-hosting wins at >100M queries/month.

---

## Index Types

### HNSW (Hierarchical Navigable Small World)

**Best for:** Read-heavy, <500M vectors
- Excellent query speed
- Memory-intensive (entire graph in RAM)
- Slow index builds

**Parameters (start here):**
| Use Case | M | efConstruction | efSearch |
|----------|---|----------------|----------|
| Real-time | 12 | 200 | 100 |
| Balanced | 16-24 | 200-400 | 200 |
| High-recall | 24-48 | 400-800 | 500-1000 |

### IVF (Inverted File)

**Best for:** High-update workloads, heavy filtering
- Fast index builds
- Lower memory than HNSW
- Better filtering performance

**When to prefer IVF:**
- Real-time updates (Airbnb chose IVF over HNSW)
- Filtering eliminates >50% of results
- Memory constraints

---

## Production Gotchas

### Embedding Model Versioning

**Problem:** New embedding models produce incompatible vectors.

**Solution:**
```sql
CREATE TABLE fragments (
    id TEXT PRIMARY KEY,
    content TEXT,
    embedding FLOAT[768],
    embedding_model TEXT,      -- "nomic-embed-v1.5"
    embedding_version TEXT,    -- "2026-01-15"
    embedded_at TIMESTAMPTZ
);
```

**On model upgrade:**
1. Add new embedding column
2. Backfill in background
3. Validate with test queries
4. Switch traffic
5. Drop old column

### Migration Cold Cache

**Problem:** Post-migration latencies spike for 30-60 minutes.

**Solution:**
- Pre-warm with common queries before cutover
- Use read replicas for validation
- Migrate during low-traffic windows

### Filter-Aware Index Selection

**Problem:** HNSW struggles when filtering eliminates most results.

**Solution:**
```
Filtering selectivity > 50%? → Use IVF
Filtering selectivity < 50%? → HNSW is fine
```

---

## Migration Paths

### DuckDB → PostgreSQL

**When:** Need concurrent users, <100ms latency

**Steps:**
1. Export via SQL: `COPY fragments TO 'export.parquet'`
2. Load to Postgres: `COPY fragments FROM 'export.parquet'`
3. Create pgvector index: `CREATE INDEX ... USING hnsw`
4. Update connection strings
5. Warm cache before cutover

### Pinecone → PostgreSQL

**When:** Cost reduction (90% savings typical)

**Steps:**
1. Export via Pinecone API (paginated)
2. Load to PostgreSQL + pgvectorscale
3. Parallel reads (both systems) for validation
4. Switch traffic
5. Sunset Pinecone

---

## Sources

- [Airbyte: DuckDB vs PostgreSQL](https://airbyte.com/data-engineering-resources/duckdb-vs-postgres)
- [NewTuple: Vector Search Performance](https://www.newtuple.com/post/speed-and-scalability-in-vector-search)
- [FireCrawl: Best Vector Databases 2025](https://www.firecrawl.dev/blog/best-vector-databases-2025)
- [Ryz Labs: Pinecone vs Weaviate vs Qdrant](https://learn.ryzlabs.com/rag-vector-search/pinecone-vs-weaviate-qdrant-the-best-vector-database-for-rag-in-2026)
- [Milvus: HNSW vs IVF](https://milvus.io/blog/understanding-ivf-vector-index-how-It-works-and-when-to-choose-it-over-hnsw.md)
- [Medium: PostgreSQL for AI Startups](https://medium.com/@takafumi.endo/why-ai-startups-choose-postgresql-supabase-neon-pgvector-7d1e1383b3dd)
