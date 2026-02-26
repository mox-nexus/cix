# Hybrid Search Architecture Patterns

## Why Hybrid Beats Pure Approaches

| Method | Strength | Weakness |
|--------|----------|----------|
| Keyword (BM25) | Exact matches, rare terms | Misses synonyms |
| Semantic | Conceptual understanding | Can be "too loose" |
| **Hybrid** | Both signals compound | Slight complexity |

**Production evidence:** 8-15% accuracy improvement over pure methods.

---

## Reciprocal Rank Fusion (RRF)

### The Production Standard

Used by: Elasticsearch, Azure AI Search, OpenSearch, Pinecone

```python
def rrf_score(rank: int, k: int = 60) -> float:
    """RRF score for a single rank."""
    return 1.0 / (rank + k)

def hybrid_rrf(
    keyword_results: list[Fragment],
    semantic_results: list[Fragment],
    k: int = 60
) -> list[tuple[Fragment, float]]:
    """Combine results using RRF."""
    scores: dict[str, float] = {}
    fragments: dict[str, Fragment] = {}

    for rank, frag in enumerate(keyword_results):
        scores[frag.id] = rrf_score(rank, k)
        fragments[frag.id] = frag

    for rank, frag in enumerate(semantic_results):
        scores[frag.id] = scores.get(frag.id, 0) + rrf_score(rank, k)
        if frag.id not in fragments:
            fragments[frag.id] = frag

    return sorted(
        [(fragments[id], score) for id, score in scores.items()],
        key=lambda x: x[1],
        reverse=True
    )
```

### Why k=60?

Empirically derived constant from Elasticsearch/Azure testing.

- **k=60** — Standard default, balanced contribution
- **k=20** — Top ranks matter more (prefer precision)
- **k=100** — Smoother distribution (prefer recall)

### Weighted RRF

```python
def weighted_rrf(
    keyword_results: list[Fragment],
    semantic_results: list[Fragment],
    keyword_weight: float = 0.4,
    semantic_weight: float = 0.6,
    k: int = 60
) -> list[tuple[Fragment, float]]:
    """RRF with per-method weighting."""
    scores: dict[str, float] = {}

    for rank, frag in enumerate(keyword_results):
        scores[frag.id] = keyword_weight * rrf_score(rank, k)

    for rank, frag in enumerate(semantic_results):
        scores[frag.id] = scores.get(frag.id, 0) + semantic_weight * rrf_score(rank, k)

    # ... return sorted
```

**Typical weights:**
- General search: 0.6 semantic, 0.4 keyword
- Code search: 0.3 semantic, 0.7 keyword
- Decision archaeology: 0.7 semantic, 0.3 keyword

---

## Re-Ranking Approaches

### When to Add Re-Ranking

| Corpus Size | Re-Ranking | Why |
|-------------|------------|-----|
| <10K docs | Skip | RRF sufficient |
| 10K-100K | Consider ColBERT | Marginal improvement |
| >100K | Recommend | Filters "looks relevant but wrong" |

### ColBERT (Late Interaction)

**What it is:** Token-level embedding comparison, not document-level.

**Advantage:** Understands "auth token" ≠ "token ring topology"

```python
# Conceptual - actual impl uses RAGatouille or similar
from colbert import ColBERT

reranker = ColBERT.load("colbertv2.0")

# Rerank top-k results
reranked = reranker.rerank(query, top_k_fragments)
```

**Performance:**
- 2 orders of magnitude faster than cross-encoders
- Precomputed doc embeddings
- ~50-100ms for top-20 rerank

### Cross-Encoders

**What it is:** Process (query, document) pair through transformer together.

```python
from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# Score each pair
scores = reranker.predict([
    (query, frag.content) for frag in top_k_fragments
])
```

**When to use:**
- Final polish for important queries
- Small result sets (<50)
- Quality > latency

**Performance:**
- ~100-300ms per query
- Can't precompute — must run at query time

### LLM Re-Ranking

**Ultimate quality, highest cost:**

```python
prompt = f"""
Given query: "{query}"

Rank these fragments by relevance (most relevant first):
{formatted_fragments}

Return fragment IDs in order.
"""
# Use Claude/GPT to rerank
```

**When to use:**
- User explicitly asks for "best" results
- Critical search where accuracy matters most
- Async/batch reranking

---

## Architecture Decision Tree

```
Is corpus < 10K documents?
├── Yes → Use RRF hybrid, skip re-ranking
└── No → Is latency critical (<100ms)?
    ├── Yes → RRF + ColBERT (precomputed)
    └── No → Is accuracy critical?
        ├── Yes → RRF + Cross-encoder or LLM rerank
        └── No → RRF + ColBERT
```

---

## Implementation in Hexagonal Architecture

### Where Logic Lives

```
ExcavationService (domain/services/)
├── search()          → delegates to CorpusPort.search()
├── semantic_search() → delegates to CorpusPort.semantic_search()
├── hybrid_search()   → orchestrates RRF fusion ← HERE
└── rerank()          → optional, uses RerankerPort
```

### Port Design

```python
class CorpusPort(Protocol):
    def search(self, query: str, limit: int) -> list[Fragment]: ...
    def semantic_search(
        self, embedding: list[float], limit: int
    ) -> list[tuple[Fragment, float]]: ...

class RerankerPort(Protocol):  # Optional
    def rerank(
        self, query: str, fragments: list[Fragment], limit: int
    ) -> list[tuple[Fragment, float]]: ...
```

### Service Implementation

```python
class ExcavationService:
    def __init__(
        self,
        corpus: CorpusPort,
        embedder: EmbeddingPort | None = None,
        reranker: RerankerPort | None = None,
    ):
        self.corpus = corpus
        self.embedder = embedder
        self.reranker = reranker

    def hybrid_search(
        self,
        query: str,
        limit: int = 20,
        rerank: bool = False,
    ) -> list[tuple[Fragment, float]]:
        # Get both result sets
        keyword_results = self.corpus.search(query, limit * 2)
        semantic_results = []
        if self.embedder:
            embedding = self.embedder.embed(query)
            semantic_results = self.corpus.semantic_search(embedding, limit * 2)

        # RRF fusion
        combined = self._rrf_fusion(keyword_results, semantic_results)

        # Optional reranking
        if rerank and self.reranker:
            fragments = [f for f, _ in combined[:limit * 2]]
            combined = self.reranker.rerank(query, fragments, limit)

        return combined[:limit]
```

---

## Precision vs Recall Tradeoffs

### High Recall (cast wide net)

- Legal discovery, compliance search
- "Don't miss anything relevant"
- Use: Lower min_score, higher limit, semantic-heavy

### High Precision (minimize noise)

- E-commerce product search
- "Only show highly relevant"
- Use: Higher min_score, keyword-heavy, strict filters

### Balanced (personal corpus)

- Exploratory search
- "Find relevant but also surprise me"
- Use: RRF default, moderate limits

---

## Sources

- [Introducing RRF for hybrid search - OpenSearch](https://opensearch.org/blog/introducing-reciprocal-rank-fusion-hybrid-search/)
- [Hybrid Search Scoring - Azure AI Search](https://learn.microsoft.com/en-us/azure/search/hybrid-search-ranking)
- [Making RRF smarter with weights - Elasticsearch](https://www.elastic.co/search-labs/blog/weighted-reciprocal-rank-fusion-rrf)
- [ColBERT: Efficient and Effective Passage Search](https://github.com/stanford-futuredata/ColBERT)
- [Production RAG: Hybrid + Re-Ranking](https://machine-mind-ml.medium.com/production-rag-that-works-hybrid-search-re-ranking-colbert-splade-e5-bge-624e9703fa2b)
- [Cross-Encoders, ColBERT, and LLM Re-Rankers](https://medium.com/@aimichael/cross-encoders-colbert-and-llm-based-re-rankers-a-practical-guide-a23570d88548)
