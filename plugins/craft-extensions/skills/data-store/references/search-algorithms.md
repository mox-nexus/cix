# Search Algorithms Deep Dive (2026)

## Algorithm Selection Decision Tree

```
What's your retrieval problem?
├── Exact keyword matching?
│   └── BM25 (baseline, always include)
├── Pure semantic similarity (<1B vectors)?
│   └── Dense HNSW + quantization
├── Document/long-form search?
│   └── ColBERT (late interaction)
├── High-scale (>1B vectors)?
│   └── IVF-PQ (aggressive quantization)
├── Production RAG?
│   └── HYBRID: Dense + BM25 + RRF (required 2026)
├── Real-time updates (100+ docs/sec)?
│   └── IVF (memory stable on inserts)
└── Constrained latency (<10ms)?
    └── Single dense vector, scalar quantization
```

---

## Lexical Search: BM25 vs TF-IDF

**BM25 is the industry standard.** TF-IDF is legacy.

| Aspect | BM25 | TF-IDF |
|--------|------|--------|
| Term frequency | Diminishing returns | Linear scaling |
| Doc length norm | Yes | No |
| IDF smoothing | Yes | No |
| Adoption | Elasticsearch, Solr, DuckDB FTS | Legacy only |

**When BM25 fails:**
- Synonymy ("car" ≠ "automobile")
- Paraphrasing
- Cross-lingual queries

---

## Dense Vector Search

### HNSW vs IVF Comparison

| Criterion | HNSW | IVF |
|-----------|------|-----|
| Query latency | 3x faster | Slower |
| Memory | O(n × m × d), high | O(nd), lower |
| Index build | Slower | Faster |
| Recall quality | Higher | Acceptable |
| Filtered search | Struggles | Efficient |
| Real-time updates | Memory bloat | Handles well |

### Decision Framework

| Condition | Choose |
|-----------|--------|
| <100M vectors + high accuracy | HNSW |
| 100M-1B + balanced | HNSW + quantization |
| >1B + memory constraints | IVF-PQ |
| High update volume | IVF |
| Batch/offline processing | HNSW |

### HNSW Tuning Guide

| Use Case | M | efConstruction | efSearch | Recall |
|----------|---|----------------|----------|--------|
| Real-time, low latency | 12 | 200 | 100 | ~92% |
| **Balanced (start here)** | 16-24 | 200-400 | 200 | ~95% |
| High-recall (offline) | 24-48 | 400-800 | 500-1000 | ~99% |

**Tuning steps:**
1. Start: M=16, efConstruction=200, efSearch=100
2. Recall < 95%? → Increase efSearch first (cheap)
3. Still low? → Increase M and efConstruction (expensive)

---

## Sparse Vector Retrieval

### Three Approaches

| Type | Method | Recall | Cost | When |
|------|--------|--------|------|------|
| Classical sparse | BM25 | 0.72 | Minimal | Baseline |
| Learned sparse | SPLADE | 0.85+ | Medium | Hybrid RAG |
| Dense + sparse hybrid | RRF | 0.91+ | High | Production |

### SPLADE (Learned Sparse)

**What it is:** Neural network learns term expansion and weights.

**Why it matters:**
- Stored in inverted index (efficient like BM25)
- Outperforms BM25 in IR evaluations
- Interpretable (which words matched?)

**Availability:**
- Qdrant: Built-in sparse vector support
- Elasticsearch: ELSER model
- OpenSearch: Neural sparse search

---

## Late Interaction Models (2026 Emerging)

### ColBERT / ColPali

**Paradigm shift:** Token-level embeddings, not document-level.

| Approach | Storage | Query Cost | Recall |
|----------|---------|-----------|--------|
| Single dense (bi-encoder) | 1 × 768-dim | Fast | 0.85 |
| ColBERT (late interaction) | N tokens × 128-dim | Moderate | 0.95+ |
| ColPali (vision docs) | N patches × 128-dim | Moderate | 0.97+ |

### Why ColBERT?

- Understands "auth token" ≠ "token ring topology"
- 45x latency reduction via PLAID optimization
- Handles long context better than single vectors
- Libraries: RAGatouille, PyLate

### When to Use

| Corpus Size | Approach |
|-------------|----------|
| <10K docs | RRF hybrid, skip re-ranking |
| 10K-100K | Consider ColBERT |
| >100K | Recommend ColBERT |

---

## Quantization Strategies

| Technique | Compression | Speed | Accuracy Loss |
|-----------|-------------|-------|---------------|
| Scalar (int8) | 4x | 2x faster | 1-2% |
| Product (PQ) | 32-64x | 0.5-1x | 5-10% |
| Binary | 32x | 8x+ | ~5% |

### When to Apply

| Scenario | Quantization |
|----------|-------------|
| <10M vectors | None needed |
| 10M-100M | Scalar (int8) |
| >100M | Scalar required |
| >1B | Product (PQ) |
| Mobile/edge | Binary |

---

## Hybrid Search with RRF

### The Production Standard (2026)

"Pure dense" is no longer acceptable in production RAG.

**Typical improvements:**
| Method | Recall | Precision |
|--------|--------|-----------|
| BM25 alone | 0.72 | 0.68 |
| Dense alone | 0.85 | 0.80 |
| **Hybrid (RRF)** | **0.91** | **0.87** |

### RRF Formula

```python
def rrf_score(rank: int, k: int = 60) -> float:
    return 1.0 / (rank + k)
```

**Why k=60?**
- Empirically derived (Elasticsearch, Azure, OpenSearch)
- k=60: balanced contribution
- k=20: top ranks matter more
- k=100: smoother distribution

### Multi-Stream RRF

Add SPLADE as third retriever:

```python
final_score = (
    w1 * rrf_dense +
    w2 * rrf_sparse +
    w3 * rrf_keyword
)
# Typical: [0.4, 0.3, 0.3]
```

---

## Multi-Stage Retrieval (Production)

### The Pattern

```
Stage 1: FAST RETRIEVAL (5-30ms P95)
  └─ Pull 500-5,000 candidates
  └─ Uses: ANN (HNSW or IVF)
  └─ Goal: High recall, low latency

Stage 2: EXPENSIVE RERANKING (50-150ms P95)
  └─ Score 200-1,000 candidates
  └─ Uses: Cross-encoder, ColBERT, or LLM
  └─ Goal: Precision, ranking quality

Total: <200ms P95, 10,000+ QPS per region
```

### Who Uses What

- **Spotify**: HNSW via Voyager, GPU embeddings, batch indexing
- **Airbnb**: IVF (real-time pricing updates), contrastive learning

---

## Implementation Gotchas

### HNSW

- efConstruction must match expected ef_search
- Memory bloats on every insert (Airbnb's reason for IVF)
- Best for batch indexing, struggles with real-time

### IVF-PQ

- Requires k-means clustering upfront (expensive one-time)
- Sensitive to cluster count—miscalibration kills recall
- Quantization error compounds—validate on test queries

### Hybrid (RRF)

- k=60 is robust but test on your domain
- Both retrievers need sufficient candidates (min 100 each)
- Score normalization alternatives (min-max, L2) don't work

### Late Interaction (ColBERT)

- 10-100x storage vs single vectors
- PLAID requires batch processing
- Embedding dims smaller (128) = better storage

---

## Sources

- [BM25 vs TF-IDF (Medium)](https://medium.com/mlworks/why-bm25-algorithm-over-tf-idf-67bc009d20de)
- [HNSW vs IVF (MyScale)](https://www.myscale.com/blog/hnsw-vs-ivf-explained-powerful-comparison/)
- [OpenSearch: RRF for Hybrid Search](https://opensearch.org/blog/introducing-reciprocal-rank-fusion-hybrid-search/)
- [Weaviate: Late Interaction Overview](https://weaviate.io/blog/late-interaction-overview)
- [Spotify: Voyager ANN Library](https://engineering.atspotify.com/2023/10/introducing-voyager-spotifys-new-nearest-neighbor-search-library/)
- [Airbnb: Embedding-Based Retrieval](https://airbnb.tech/uncategorized/embedding-based-retrieval-for-airbnb-search/)
- [Pinecone: SPLADE Explained](https://www.pinecone.io/learn/splade/)
- [ColBERT GitHub](https://github.com/stanford-futuredata/ColBERT)
