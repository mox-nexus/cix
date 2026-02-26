# Storage and Search: Methodology

Why these patterns exist and what trade-offs they navigate.

---

## The Core Challenge

Search is not one problem. It's three simultaneous problems with conflicting solutions.

| Problem | Requirement | Conflicts With |
|---------|-------------|----------------|
| **Recall** | Find all relevant results | Precision (noise) |
| **Precision** | Only relevant results | Recall (completeness) |
| **Latency** | Fast enough for users | Index quality |

Single-mode search optimizes one dimension and sacrifices the others.

**The insight:** Hybrid search with multiple signals recovers what single modes miss.

---

## Why Hybrid Search Wins

### The Research Evidence

**MTEB Benchmark (2024):** Pure semantic search achieves 0.72 recall on average.

**Industry adoption:** Elasticsearch (2023), Azure Cognitive Search (2024), OpenSearch (2024) all converged on hybrid as default.

**Measured improvement:** BM25 + semantic with RRF fusion: 0.72 → 0.91 recall.

**Why the improvement:**

| Search Mode | Catches | Misses |
|-------------|---------|--------|
| **Keyword (BM25)** | Exact terms, acronyms, code | Conceptual similarity |
| **Semantic** | Intent, paraphrases | Exact technical terms |
| **Hybrid** | Both categories | (minimal) |

### Real-World Example

Query: "where did I decide on authentication?"

**BM25 alone:**
- Finds: "We chose OAuth 2.0 for authentication"
- Misses: "Login will use token-based auth" (no exact match)

**Semantic alone:**
- Finds: Both of the above
- Also finds: "User management system" (too broad)

**Hybrid:**
- Finds: Both relevant results
- Ranks exact matches higher
- Reduces false positives

The combination recovers precision without losing recall.

---

## The RRF Pattern

### Why Not Score Blending?

The naive approach: weighted combination of scores.

```python
# ❌ This looks reasonable but fails
final_score = 0.7 * bm25_score + 0.3 * semantic_score
```

**The problem:** Score scales are incomparable.

| Search Mode | Score Range | Meaning |
|-------------|-------------|---------|
| BM25 | 0 to 100+ | Term frequency × IDF |
| Cosine similarity | 0.0 to 1.0 | Angular distance |

A BM25 score of 5.0 and cosine of 0.5 mean completely different things. No normalization function transfers reliably across query distributions.

### Reciprocal Rank Fusion (RRF)

**Source:** Cormack et al., SIGIR 2009

Instead of scores, use ranks:

```python
k = 60  # Constant across all major search engines
rrf_score = 1/(bm25_rank + k) + 1/(semantic_rank + k)
```

**Why this works:**

1. **Scale-invariant** — Ranks are comparable (1st, 2nd, 3rd...)
2. **No tuning** — k=60 is production standard
3. **Robust** — Handles score distributions without normalization
4. **Simple** — No machine learning, no training data

**Adoption:** Elasticsearch (default), Azure Cognitive Search (default), OpenSearch (default), Pinecone (hybrid mode).

**The consensus:** When all major search platforms converge on the same solution, trust it.

---

## Storage Backend Selection

### The 2026 Reality

PostgreSQL + pgvector won the <50M vector space.

**Evidence:**

| Source | Claim |
|--------|-------|
| Airbyte (2025) | "PostgreSQL handles most workloads, specialized VDBs for >50M" |
| Medium (2025) | "AI startups choose PostgreSQL + Supabase" |
| FireCrawl (2025) | "Pinecone costs 90% more than self-hosted Postgres" |

**Why PostgreSQL wins:**

1. **ACID transactions** — Data integrity guarantees
2. **Known tooling** — Teams already understand it
3. **Hybrid search** — Full-text + vectors in one query
4. **No vendor lock-in** — Standard SQL, portable data
5. **Managed options** — Supabase/Neon for serverless

**When to upgrade:** >50M vectors, <50ms latency at scale, complex runtime filtering.

### DuckDB for Personal Use

**Why DuckDB for memex:**

| Feature | Benefit |
|---------|---------|
| Embedded | No server management |
| Analytical | Complex queries for exploration |
| Parquet-native | Efficient columnar storage |
| Zero cost | No infrastructure required |

**Trade-offs:**

| Can Do | Can't Do |
|--------|----------|
| Batch processing | Concurrent writes |
| Complex analytics | Real-time updates |
| Personal scale (<10M vectors) | Production multi-user |

**The fit:** Personal knowledge bases are OLAP workloads (read-heavy analytics), not OLTP (transactional updates). DuckDB is optimized for this.

---

## Embedding Model Selection

### The 768-Dimension Sweet Spot

**Evidence:**

| Dimension | Quality Gain | Storage Cost |
|-----------|-------------|--------------|
| 384 | Baseline | 50% less |
| 768 | +12% over 384 | Baseline |
| 1024 | +3% over 768 | +33% |
| 1536 | +1% over 1024 | +100% |

**Source:** MTEB benchmarks, Nomic Embed documentation.

**The curve flattens:** Diminishing returns above 768 dimensions.

**Implication:** Use 768 unless you have specific evidence that higher dimensions help your domain.

### Nomic Embed v1.5 (Recommended)

**Why this model:**

1. **Open source** — Apache 2.0, no API costs
2. **Quality** — Beats OpenAI v3 on MTEB benchmarks
3. **Efficient** — Mixture of Experts architecture
4. **Multilingual** — 100+ languages
5. **Production-ready** — 8K context, battle-tested

**Alternative:** all-MiniLM-L6-v2 for speed (384 dims, 5x faster, acceptable quality trade-off).

**When to use APIs:** Voyage-4-Large when you need absolute best quality and cost isn't a constraint (14% better than OpenAI, but $0.06-0.18 per 1M tokens).

---

## Index Selection: HNSW vs IVF

### When HNSW Wins

**Use case:** Read-heavy, <500M vectors, query speed critical

**How it works:** Hierarchical graph traversal (like skip lists for vectors)

**Characteristics:**
- Excellent query speed (sub-50ms)
- Memory-intensive (entire graph in RAM)
- Slow index builds
- Production standard for most applications

**Parameters (start here):**
- M = 16 (graph connectivity)
- efConstruction = 200 (build quality)
- efSearch = 100 (query quality)

**Source:** Milvus, Qdrant, pgvector documentation convergence.

### When IVF Wins

**Use case:** Heavy filtering (>50% results eliminated), high update rates

**How it works:** Inverted index with clustering (like traditional search indexes)

**Why filtering matters:**

HNSW builds a graph assuming all points are candidates. When filtering eliminates 80% of results, HNSW wastes time traversing irrelevant graph regions.

IVF partitions by cluster, can skip entire clusters based on filters.

**Real-world case:** Airbnb chose IVF over HNSW for real-time inventory updates.

**Source:** Milvus blog (2024), "Understanding IVF Vector Index: How It Works and When to Choose It Over HNSW."

---

## The Migration Pattern

### Embedding Model Versioning

**The problem:** New embedding models produce incompatible vectors. Old embeddings can't be compared to new ones.

**The solution:** Version tracking in schema.

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

**Migration strategy:**
1. Add new embedding column
2. Backfill in background (batch processing)
3. Validate with test queries
4. Switch production traffic
5. Drop old column after monitoring period

**Why this order:** Zero downtime, easy rollback, validated before commitment.

### Cold Cache Problem

**The observation:** Post-migration latencies spike for 30-60 minutes.

**Why:** Vector indexes (HNSW especially) benefit enormously from memory caching. Cold cache = disk I/O = 10-100x slower.

**The solution:** Pre-warm with common queries before cutover.

**Evidence:** NewTuple (2024) documented 47-minute warmup period for PostgreSQL + pgvector after migration.

---

## Production Gotchas

### DuckDB FTS Index Doesn't Auto-Update

**The behavior:** Creating FTS index is explicit. Updates to data don't rebuild it.

```sql
-- Index creation (one-time)
PRAGMA create_fts_index('fragments', 'id', 'content');

-- After data changes, index is STALE
-- Must rebuild manually
DROP TABLE fts_main_fragments;
PRAGMA create_fts_index('fragments', 'id', 'content');
```

**Why:** DuckDB optimizes for analytical workloads (infrequent updates, fast reads). Auto-updating would slow down writes.

**Implication:** Build index rebuild into your ingest pipeline, not query path.

### VSS Extension Still Experimental

**Status (2026):** DuckDB VSS extension works but isn't production-stable.

**Use case fit:** Fine for personal knowledge bases, not for production multi-user systems.

**Migration path:** When you outgrow DuckDB, PostgreSQL + pgvector is the standard upgrade.

---

## Architecture Boundaries

### Hexagonal Architecture (Ports and Adapters)

**Why this matters for search:**

Storage and embedding technologies change. Business logic shouldn't.

| Concern | Lives In | Never In |
|---------|----------|----------|
| Embedding generation | Adapter (implements EmbeddingPort) | Domain |
| RRF fusion | Service layer | Adapter or CLI |
| Search orchestration | Service layer | Storage adapter |
| Result formatting | CLI/API | Service layer |

**The benefit:** Swap DuckDB → PostgreSQL by changing one adapter. Business logic unchanged.

### Port Design Pattern

```python
class EmbeddingPort(Protocol):
    """Abstraction for any embedding provider."""
    def embed(self, text: str) -> list[float]: ...
    def embed_batch(self, texts: list[str]) -> list[list[float]]: ...
    @property
    def dimensions(self) -> int: ...
```

**Why Protocol over ABC:** Duck typing, no inheritance burden, easier testing.

**Implementations:**
- `NomicEmbedAdapter` — Local Nomic model
- `VoyageEmbedAdapter` — API-based
- `MockEmbedAdapter` — Testing

**The test:** Can you swap implementations without changing calling code?

---

## Why These Patterns Emerged

### Hybrid Search Convergence (2023-2024)

**Timeline:**
- 2023: Elasticsearch ships RRF hybrid search
- 2024: Azure Cognitive Search adopts RRF
- 2024: OpenSearch adds RRF mode
- 2024: Pinecone launches hybrid search (RRF-based)

**Interpretation:** Independent discovery converging on the same solution = strong evidence.

### PostgreSQL Renaissance (2024-2026)

**Timeline:**
- 2023: pgvector reaches 0.5.0 (production-ready)
- 2024: Supabase/Neon popularize serverless Postgres
- 2025: pgvectorscale extension handles 50M+ vectors
- 2026: Industry consensus: PostgreSQL for <50M vectors

**Why it won:** Familiarity + reliability + no vendor lock-in beat marginal performance gains from specialized databases.

### Nomic Embed Rise (2024-2026)

**Timeline:**
- 2024: Nomic Embed v1 beats OpenAI on MTEB
- 2025: v1.5 ships with MoE architecture
- 2026: Production adoption accelerates

**Why it won:** Quality competitive with paid APIs + zero cost + local control.

---

## The Test

For every storage/search decision:

1. **Does hybrid improve recall?** (Yes: keyword + semantic catch different cases)
2. **Is RRF better than score blending?** (Yes: scale-invariant, no tuning, production-proven)
3. **Do I need >768 dimensions?** (Usually no: quality curve flattens)
4. **Is my workload OLTP or OLAP?** (Determines DuckDB vs PostgreSQL)
5. **Can I swap implementations cleanly?** (Hexagonal architecture test)

Decisions that violate these patterns should have specific evidence for the exception.

---

## The Deeper Why

Search is not about finding THE answer. It's about surfacing relevant context so humans can make informed decisions.

Single-mode search optimizes for a metric (BM25 score, cosine similarity) that doesn't map cleanly to "relevance."

Hybrid search acknowledges this: combine multiple signals, let the human decide what's relevant for their context.

That's why RRF works—it doesn't claim to know which signal is "right." It combines them and lets relevance emerge from the union.

---

See [sources.md](sources.md) for research citations and production evidence.
