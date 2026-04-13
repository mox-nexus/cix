# Vector Storage, Hybrid Retrieval, Embeddings, Temporal Search (2025-2026)

**Source type:** Web research synthesis
**Collected:** 2026-04-13
**Coverage:** LanceDB, vector DB comparison, hybrid search, embedding models, temporal retrieval

---

## 1. LanceDB Current State

LanceDB is an embedded, in-process vector database built on the Lance v2 columnar format.

- **Lance v2.2 format**: Blob V2, nested schema evolution, native Map type, additional compression. Claims 100x faster than Parquet for queries and 1.5M IOPS on disk reads.
- **Zero-copy versioning**: Each insert creates a new version tracked via manifest metadata. Git-style branching, tagging, and shallow clone on top of multi-base architecture.
- **Native hybrid search**: Built-in FTS via Tantivy (`create_fts_index()`), `query_type="hybrid"`, with built-in rerankers (linear combination, RRF, Cohere, ColBERT).
- **Lance-native SQL** via DuckDB (2026), native support on Hugging Face Hub, Arrow-native geospatial with R-Tree indexing.
- **Local-first**: Runs entirely in-process, no server. Python and Rust SDKs. Apache 2.0.

For a personal memory system with <1M vectors, LanceDB's embedded model eliminates operational overhead. The versioning story is uniquely strong — no other local vector DB offers automatic, zero-copy dataset versioning.

Sources:
- https://docs.lancedb.com
- https://lancedb.com/docs/overview/lance/
- https://docs.lancedb.com/search/full-text-search

## 2. Vector DB Comparison for Local Personal Use (<1M vectors)

| System | Deployment | Hybrid Search | Key Trade-off |
|--------|-----------|---------------|---------------|
| **LanceDB** | Embedded, in-process | Native (BM25+vector, RRF/linear) | Best for local-first; versioning is unique; youngest ecosystem |
| **Chroma** | Embedded, in-process | No native hybrid | Simplest API; 2025 Rust rewrite (4x perf); no FTS built-in |
| **Qdrant** | Server (can run local) | Native (sparse+dense fusion) | Best filtered search; richer query API; heavier footprint |
| **pgvector** | PostgreSQL extension | Via pg_trgm/ParadeDB | Zero new infra if already running Postgres; maxes out ~10M vectors |
| **Weaviate** | Server | Native (BM25+vector, built-in) | Best hybrid search UX; overbuilt for personal use |
| **Milvus** | Server | Native (sparse+dense) | Built for billions; overkill for <1M; has temporal decay rankers |

**Verdict for local-first personal memory**: LanceDB or Chroma. LanceDB wins on hybrid search (native BM25+vector), versioning, and multimodal columnar storage. Multiple sources note that the vector DB choice accounts for roughly 5-10% of RAG quality — chunking, embedding model, and retrieval pipeline matter far more.

Sources:
- https://4xxi.com/articles/vector-database-comparison/
- https://encore.dev/articles/best-vector-databases

## 3. Hybrid Search Best Practices

**RRF (Reciprocal Rank Fusion)** remains the default production choice:
- Operates on rank positions only, no score normalization needed. Robust, parameter-light.
- Typical pattern: BM25 retrieves top-k sparse, HNSW retrieves top-k dense, RRF merges, optional cross-encoder reranks top-10.

**Convex/linear combination** outperforms RRF in benchmarks (ACM TOIS study) when tuned, but requires labeled data and is domain-sensitive. RRF is the better zero-shot default.

**For conversational memory**: BM25 catches exact names, terms, and phrases that embeddings miss. Dense catches semantic similarity across paraphrases. Hybrid is not optional — conversations contain both precise references ("the React hook we discussed") and fuzzy concepts ("that architecture pattern for decoupling").

Sources:
- https://weaviate.io/blog/hybrid-search-explained
- https://opensearch.org/blog/introducing-reciprocal-rank-fusion-hybrid-search/

## 4. Embedding Models for Conversational Content

**MTEB leaderboard (March 2026)**:
- **Top overall**: Gemini Embedding 001 (68.32 avg), Qwen3-Embedding-8B (70.58 multilingual), NVIDIA Llama-Embed-Nemotron-8B.
- Top 5 by raw score are now all free/open-weight or very cheap.

**For local deployment**:
- **Snowflake Arctic Embed v2.0** (334M params): 55.9 avg retrieval on MTEB. Matryoshka support (128-dim to full). Apache 2.0.
- **Nomic Embed Text v1.5** (~137M): Good retrieval, 8192 context, Matryoshka, open-weight.
- **all-MiniLM-L6-v2** (22M): Only useful for prototyping.

**Conversational content gap**: No MTEB task specifically benchmarks dialogue/conversation retrieval. Models are evaluated on document retrieval, STS, and classification. Conversational content has unique properties (turn-taking, coreference, implicit context) that standard benchmarks don't capture.

Sources:
- https://huggingface.co/spaces/mteb/leaderboard
- https://blog.premai.io/best-embedding-models-for-rag-2026-ranked-by-mteb-score-cost-and-self-hosting/

## 5. Temporal Retrieval

**Milvus** is the only vector DB with first-class temporal decay rankers: exponential, linear, and Gaussian decay functions. Configurable origin, scale, offset, decay rate.

**Everyone else** does temporal ranking at the application layer: filter by time range, then boost by recency in a post-retrieval reranker.

**Research frontier**: Re3 (arxiv 2509.01306) proposes learnable, query-aware gating to adaptively balance semantic relevance and temporal information — some queries are time-sensitive ("what did I discuss yesterday?"), others are not ("what's the architecture pattern for X?"). Fixed decay functions can't distinguish these.

**For memex**: Temporal scoring is implementable at the application layer with LanceDB. Store timestamps as metadata, retrieve top-k by hybrid search, apply exponential decay in the reranking step.

Sources:
- https://milvus.io/docs/decay-ranker-overview.md
- https://arxiv.org/html/2509.01306v1
