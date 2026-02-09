---
name: data-store
description: "Data storage and retrieval patterns. Use when: choosing databases, implementing search, designing hybrid retrieval, selecting embedding models, building RAG systems."
version: 0.1.0
---

# Data Store

> Production patterns for storage and retrieval: backends, search, embeddings, RAG

## When to Use

- Implementing search in applications
- Choosing storage backend for vectors/search
- Selecting between keyword/semantic/hybrid search
- Selecting embedding models
- Building RAG retrieval layers
- Personal corpus/knowledge base systems

---

## Storage Backend Selection

```
What's your scale?
├── <100K docs → DuckDB, SQLite, LanceDB (embedded)
├── 100K-50M → PostgreSQL + pgvector ← MOST APPS
├── 50M-1B → Qdrant, Weaviate (dedicated VDBs)
└── >1B → Milvus, ClickHouse (distributed)
```

| Scale | Backend | Why |
|-------|---------|-----|
| Personal KB | DuckDB | Free, zero-ops, analytical queries |
| Startup/Team | PostgreSQL + pgvector | Hybrid search, ACID, known tooling |
| Enterprise | Qdrant/Weaviate | Complex filtering, sub-50ms latency |

**2026 consensus:** PostgreSQL + pgvector won <50M vectors. Specialized VDBs for >50M.

---

## Search Mode Selection

| Query Type | Best Mode | Why |
|------------|-----------|-----|
| Exact terms ("OAuth", "Kubernetes") | Keyword (BM25) | Literal match needed |
| Conceptual ("where did I decide on auth?") | Semantic | Intent > exact words |
| Mixed intent | **Hybrid (RRF)** | Both signals compound |

**Default: Hybrid with RRF** — recall improves 0.72 → 0.91 over BM25 alone.

### Hybrid Search: Use RRF, Not Score Blending

```python
# ❌ WRONG - score scales differ (BM25: 0-100+, cosine: 0-1)
score = 0.7 * bm25_score + 0.3 * cosine_similarity

# ✅ RIGHT - rank-based, scale-invariant
k = 60  # Production constant (Elasticsearch, Azure, OpenSearch)
score = 1/(bm25_rank + k) + 1/(semantic_rank + k)
```

**Why RRF:**
- Avoids normalization headaches
- Production consensus (all major search engines use it)
- Simple, no tuning required

### Embedding Model Selection

| Use Case | Model | Dimensions | Why |
|----------|-------|------------|-----|
| Personal corpus | Nomic Embed v1.5 | 768 | Local, free, quality |
| Speed-critical | all-MiniLM-L6-v2 | 384 | 5x faster, good enough |
| Best accuracy | Voyage-4-Large (API) | 1024 | 14% better than OpenAI |

**Dimension sweet spot: 768** — Quality flattens above this, storage doubles.

### Index Type Selection

| Condition | Index | Why |
|-----------|-------|-----|
| <100M, read-heavy | HNSW | Fast queries, high recall |
| >100M, high updates | IVF | Memory stable on inserts |
| Heavy filtering (>50% eliminated) | IVF | HNSW struggles with filters |
| Mobile/edge | Binary quantization | 32x compression |

**HNSW start:** M=16, efConstruction=200, efSearch=100 → tune from there.

### DuckDB Capabilities (2026)

| Extension | Status | Use For |
|-----------|--------|---------|
| FTS (BM25) | Stable | Keyword search — replace naive ILIKE |
| VSS (vectors) | Experimental | Semantic search — OK for <50K docs |
| Hybrid | Pattern | Combine FTS + VSS with RRF in SQL |

**Gotcha:** FTS index doesn't auto-update. Rebuild after data changes.

---

## Implementation Patterns

### 1. BM25 with DuckDB FTS

```sql
-- Create index
PRAGMA create_fts_index('fragments', 'id', 'content');

-- Search
SELECT *, fts_main_fragments.match_bm25(id, 'auth token') AS score
FROM fragments
WHERE score IS NOT NULL
ORDER BY score DESC
LIMIT 20;
```

### 2. Semantic Search with VSS

```sql
-- Create HNSW index
CREATE INDEX idx_embedding ON fragments
  USING HNSW (embedding) WITH (metric = 'cosine');

-- Search
SELECT *, array_cosine_similarity(embedding, ?::FLOAT[768]) as score
FROM fragments
WHERE embedding IS NOT NULL
ORDER BY score DESC
LIMIT 20;
```

### 3. Hybrid with RRF

```python
def hybrid_search(query: str, limit: int = 20) -> list[Fragment]:
    k = 60

    # Get both result sets
    keyword_results = bm25_search(query, limit * 2)
    semantic_results = semantic_search(embed(query), limit * 2)

    # RRF fusion
    scores = {}
    for rank, frag in enumerate(keyword_results):
        scores[frag.id] = 1 / (rank + k)
    for rank, frag in enumerate(semantic_results):
        scores[frag.id] = scores.get(frag.id, 0) + 1 / (rank + k)

    # Return top-k by combined score
    return sorted(all_fragments, key=lambda f: scores[f.id], reverse=True)[:limit]
```

---

## Architecture Boundaries

### Where Logic Lives (Hexagonal)

| Concern | Location | Never In |
|---------|----------|----------|
| Embedding generation | EmbeddingPort adapter | Domain |
| Search orchestration | Service layer | CLI |
| RRF fusion | Service layer | Adapter |
| Output formatting | CLI formatters | Service |
| Wiring/DI | Composition root | Adapters |

### Port Design

```python
# EmbeddingPort - text → vector
class EmbeddingPort(Protocol):
    def embed(self, text: str) -> list[float]: ...
    def embed_batch(self, texts: list[str]) -> list[list[float]]: ...
    @property
    def dimensions(self) -> int: ...

# CorpusPort - includes search methods
class CorpusPort(Protocol):
    def search(self, query: str, limit: int) -> list[Fragment]: ...
    def semantic_search(self, embedding: list[float], limit: int) -> list[tuple[Fragment, float]]: ...
```

---

## Anti-Patterns

| ❌ Don't | ✅ Do Instead |
|---------|--------------|
| Naive ILIKE '%word%' | BM25 with FTS extension |
| Blend scores directly | Use RRF (rank-based) |
| 1024+ dims for personal corpus | 768 dims (sweet spot) |
| Cross-encoder in MVP | Direct ranking, add later |
| Search logic in CLI | Service layer orchestration |

---

## Production Checklist

Before shipping:
- [ ] Hybrid search (RRF) as default, not pure methods
- [ ] Embedding model versioned in schema
- [ ] Index rebuild strategy for FTS (doesn't auto-update)
- [ ] Cold cache warmup plan for migrations
- [ ] Filter-aware index selection (HNSW vs IVF)
- [ ] Batch embedding for ingest, lazy model loading

---

## References

Load for details:
- `references/storage-backends.md` — Backend selection, scaling, migrations
- `references/search-algorithms.md` — HNSW, IVF, BM25, SPLADE, ColBERT
- `references/embedding-models.md` — Model comparison data
- `references/hybrid-patterns.md` — RRF, re-ranking, architecture
- `references/rag-architecture.md` — Chunking, CRAG, Self-RAG, RAPTOR, caching
- `references/duckdb-search.md` — DuckDB FTS/VSS specifics
