# RAG Architecture Patterns (2026)

## Chunking Strategy Decision Tree

```
What's your query pattern?
├── Factual lookups ("What is X?")
│   └── 64-128 tokens, fixed-size
├── Multi-hop reasoning ("How does X relate to Y?")
│   └── 512-1024 tokens, semantic chunking
├── Code/technical docs
│   └── AST-aware, function boundaries
└── Mixed content (PDFs, tables)
    └── Multi-modal chunking (MAHA)
```

### Chunk Size Guidance

| Content Type | Tokens | Strategy |
|--------------|--------|----------|
| Factual Q&A | 64-128 | Fixed-size |
| **General (default)** | 256-512 | RecursiveCharacterTextSplitter |
| Narrative/reasoning | 512-1024 | Semantic chunking |
| Complex reasoning | 1024+ | RAPTOR (hierarchical) |

**Evidence:** Semantic chunking with 256-512 tokens achieves **85-90% recall** with 9% improvement over fixed-size.

**Overlap:** 10-20% of chunk size. 500-token chunk = 50-100 token overlap.

---

## Production Architecture Stack

```
┌─────────────────────────────────────────────────┐
│  INPUT: Query Intent Classification             │
│  (Route simple queries to metadata lookup)      │
└────────────┬────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────┐
│  RETRIEVAL: Hybrid (BM25 + Vector)              │
│  + Reranking (cross-encoder or LLM)             │
│  + Query expansion/decomposition                │
└────────────┬────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────┐
│  VALIDATION: Corrective RAG (CRAG)              │
│  Evaluate docs: Correct / Ambiguous / Incorrect │
│  Re-retrieve if needed                          │
└────────────┬────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────┐
│  GENERATION: Self-RAG                           │
│  Reflect on response, reformulate if unsupported│
└─────────────────────────────────────────────────┘
```

---

## Retrieval Performance

| Method | Top-10 Relevance |
|--------|------------------|
| BM25 alone | 62% |
| Vector alone | 71% |
| **BM25 + Vector + Rerank** | **87%** |

**+15-30% improvement** from hybrid + reranking.

---

## Reranking Decision Tree

```
Need reranking?
├── Simple lookup queries
│   └── Skip reranking
├── Production accuracy critical
│   ├── Time budget <500ms
│   │   └── Cross-encoder (ms-marco-MiniLM)
│   └── Time budget >1s
│       └── LLM reranker or hybrid
└── Cost-constrained
    └── Cross-encoder on top-20 only
```

### Reranking Methods

| Method | Speed | Accuracy | Best For |
|--------|-------|----------|----------|
| **Cross-encoder** | Fast (ms) | High | Default production |
| LLM Pointwise | Slow (500ms-2s) | Highest | Accuracy critical |
| LLM Listwise | Slower | Highest | Complex ranking |

**Production default:** Retrieve 50 → rerank to 10 with cross-encoder.

---

## Advanced Patterns

### Corrective RAG (CRAG)

1. Retrieve documents
2. Evaluate: Correct / Incorrect / Ambiguous
3. If incorrect/ambiguous: expand query + re-retrieve
4. If still insufficient: web search fallback

**Impact:** 18-25% hallucination reduction.

### Self-RAG

LLM reflects on response:
- Check if retrieved docs support claims
- Reformulate if unsupported
- Iterate until confident

**Complementary to CRAG:** CRAG fixes retrieval, Self-RAG fixes generation.

### RAPTOR (Hierarchical)

Tree of abstractions:
- Bottom: Raw chunks
- Middle: Cluster summaries
- Top: Document-level summaries

**When to use:** Long documents, multi-hop reasoning.
**Impact:** 20% absolute accuracy improvement on QuALITY benchmark.

### Agentic RAG

LLM agents autonomously:
- Decompose complex tasks
- Search multiple sources
- Verify intermediate results
- Adjust strategy if retrieval insufficient

**Cost:** 3-5x more expensive than simple RAG.
**When:** Complex reasoning over disparate sources.

---

## Cost Optimization

### Semantic Caching

- Store embeddings of queries + responses
- Serve cached response for semantically similar queries
- **60-80% cache hit rates** in production (Notion, Intercom)
- Latency: 150ms → 20ms

### Right-Sizing Embeddings

| Model | Dimensions | Speed | Accuracy |
|-------|-----------|-------|----------|
| Large | 1536 | Baseline | 100% |
| Medium | 768 | 2x faster | 95-98% |
| **Small** | 384 | 4x faster | 90-95% |

**Start with 384-dim** (all-MiniLM-L6-v2) and only upgrade if needed.

### Optimization Impact

Teams implementing caching + right-sizing + metadata pre-filtering: **70-80% cost reduction**.

---

## Top 10 Failure Modes

| Failure | Symptom | Fix |
|---------|---------|-----|
| Missing content | Hallucination | Add source documents |
| Missed top-ranked | Right docs not ranked first | Improve reranking |
| Context window miss | Relevant docs not in context | Rerank before assembly |
| Bad chunking | Info split across chunks | Semantic chunking |
| Stale indexes | Outdated info | Refresh schedule |
| Context overload | LLM loses signal | Aggressive filtering |
| No intent routing | Full RAG for simple queries | Route metadata lookups |
| Hallucination when missing | Speculative answers | Explicit "I don't know" |

---

## Evaluation Metrics

### Retrieval Quality

| Metric | Purpose |
|--------|---------|
| **NDCG@5** | Primary ranking metric (correlates with satisfaction) |
| Precision@k | % of top-k that are relevant |
| Recall@k | % of all relevant in top-k |
| MRR | Reciprocal rank of first relevant |

### Generation Quality

| Metric | Purpose |
|--------|---------|
| Faithfulness | Does answer follow from docs? |
| Hallucination rate | Info not in sources? |
| Citation coverage | Claims traceable to sources? |

**Tools:** RAGAS, ARES, LangSmith, Bedrock evaluation.

---

## Production Checklist

Before shipping:

**Retrieval:**
- [ ] Hybrid retrieval (BM25 + Vector)
- [ ] Reranking A/B tested
- [ ] Chunk size optimized for query patterns

**Quality:**
- [ ] CRAG for doc validation
- [ ] Hallucination detection active
- [ ] Off-topic query handling

**Observability:**
- [ ] NDCG@5 tracked
- [ ] Hallucination rate monitored
- [ ] Latency SLOs (p95, p99)
- [ ] Cost/query tracked

**Caching:**
- [ ] Semantic caching for common queries
- [ ] Right-sized embeddings (start 384-dim)

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Context stuffing | LLM hedges in token bloat | Filter to <10K tokens |
| Complexity without eval | No measurement of improvement | Always A/B test |
| No intent routing | Full RAG for "what's my billing date?" | Route simple queries |
| Binary trust | Accept/reject without inspection | Human review loop |
| Single retrieval method | Fragile to query types | Use hybrid |

---

## Sources

- [RAG Survey 2026](https://arxiv.org/html/2506.00054v1)
- [Weaviate: Chunking Strategies](https://weaviate.io/blog/chunking-strategies-for-rag)
- [RAPTOR Paper](https://arxiv.org/html/2401.18059v1)
- [Corrective RAG](https://www.kore.ai/blog/corrective-rag-crag)
- [Agentic RAG Survey](https://arxiv.org/html/2501.09136v1)
- [ZeroEntropy Reranking Guide](https://www.zeroentropy.dev/articles/ultimate-guide-to-choosing-the-best-reranking-model-in-2025)
- [RAG Failure Modes](https://dev.to/kuldeep_paul/ten-failure-modes-of-rag-nobody-talks-about-and-how-to-detect-them-systematically-7i4)
