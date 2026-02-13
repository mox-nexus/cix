# Sources

Research and technical foundations behind memex.

---

## Research Synthesis

The path from Vannevar Bush's associative trails to computational hybrid search required five converging advances: full-text indexing (BM25, 1994), dense retrieval (DPR, 2020), efficient vector storage (HNSW/DuckDB-VSS), cross-encoder reranking (MiniLM, 2020), and rank fusion (RRF, 2009). Memex combines all five into a single local-first tool because no single retrieval method handles the range of queries humans actually ask about their own work.

---

## Foundational Vision

**Bush, V. (1945). "As We May Think." The Atlantic Monthly, 176(1), 101-108.**

The original memex concept: a device for storing, linking, and retrieving personal knowledge via associative trails. Bush argued that human memory is associative, not indexed -- and that retrieval tools should match this cognitive pattern.

**Relevance to memex:** The `dig` command implements associative retrieval. FOLLOWS edges between fragments implement trails. The entire tool is named after Bush's vision.

---

## Search and Retrieval

**Robertson, S.E., & Zaragoza, H. (2009). "The Probabilistic Relevance Framework: BM25 and Beyond." Foundations and Trends in Information Retrieval, 3(4), 333-389.**

The foundational probabilistic retrieval model. BM25 remains the dominant keyword search algorithm after decades because it handles term frequency saturation and document length normalization correctly.

**Relevance to memex:** BM25 powers the keyword search channel in hybrid search, via DuckDB's full-text search extension.

---

**Karpukhin, V., et al. (2020). "Dense Passage Retrieval for Open-Domain Question Answering." EMNLP 2020.**

Demonstrated that dense (embedding-based) retrieval can outperform BM25 for question-answering tasks where semantic matching matters more than exact keyword overlap.

**Relevance to memex:** Motivates the semantic search channel. When users search for "authentication decisions" they want fragments about auth even if the exact word "authentication" doesn't appear.

---

**Cormack, G.V., Clarke, C.L.A., & Buettcher, S. (2009). "Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods." SIGIR 2009.**

RRF is a simple, parameter-free method for combining multiple ranked lists. With k=60, it consistently outperforms more complex learned fusion methods.

**Relevance to memex:** RRF fuses BM25 and semantic search results. Its parameter-free nature is critical -- there's no representative training corpus for personal knowledge retrieval.

---

**Nogueira, R., & Cho, K. (2019). "Passage Re-ranking with BERT." arXiv:1901.04085.**

Cross-encoder reranking -- feeding query-document pairs through a transformer -- achieves higher relevance accuracy than bi-encoder retrieval alone. The tradeoff is computational cost (quadratic in candidates).

**Relevance to memex:** The cross-encoder reranker (MS MARCO MiniLM-L-6-v2) runs on the top-N fused results, not the full corpus. This makes it practical for local use.

---

## Embedding Models

**Nussbaum, Z., Morris, J., Duderstadt, B., & Mulyar, A. (2024). "Nomic Embed: Training a Reproducible Long Context Text Embedder." Nomic AI Technical Report.**

nomic-embed-text-v1.5 produces 768-dimensional embeddings with Matryoshka support (can truncate to 256/512 dims). Fully open-source weights and training data.

**Relevance to memex:** Default embedding model. Runs locally via fastembed (ONNX runtime), no GPU required. Chosen for: open weights, reproducibility, long-context support (8192 tokens), and local inference.

---

## Storage

**Raasveldt, M., & Muhleisen, H. (2019). "DuckDB: An Embeddable Analytical Database." SIGMOD 2019.**

DuckDB is an in-process analytical database optimized for OLAP workloads. Embeddable (no server), column-oriented, with extensions for full-text search (FTS) and vector similarity search (VSS).

**Relevance to memex:** Single-file corpus (`corpus.duckdb`) with both BM25 (FTS extension) and HNSW vector index (VSS extension). No external services needed. The embeddable nature enables the local-first, convention-over-config design.

---

## Hexagonal Architecture

**Cockburn, A. (2005). "Hexagonal Architecture (Ports and Adapters)." alistair.cockburn.us.**

The original articulation of ports and adapters: domain logic depends on abstract interfaces (ports), with concrete implementations (adapters) injected at composition time.

**Relevance to memex:** The architecture enables testing without infrastructure (in-memory adapters) and component swapping without domain changes (new embedding model = one adapter).

---

## Protocol-Based Ports

**Python Enhancement Proposal 544. "Protocols: Structural subtyping (static duck typing)." Python 3.8+.**

`typing.Protocol` enables structural subtyping -- any class implementing the right methods satisfies the protocol without inheritance. Combined with `@runtime_checkable`, provides interface enforcement without coupling.

**Relevance to memex:** All four driven ports (CorpusPort, EmbeddingPort, RerankerPort, SourceAdapterPort) use Protocol. This was a deliberate arch-guild decision: Protocol over ABC for hexagonal ports in Python.

---

## Cross-Encoder Reranking

**Wang, W., Wei, F., Dong, L., Bao, H., Yang, N., & Zhou, M. (2020). "MiniLM: Deep Self-Attention Distillation for Task-Agnostic Compression of Pre-Trained Transformers." NeurIPS 2020.**

Knowledge distillation from large transformers to compact models. MiniLM-L-6-v2 retains most of BERT-base's effectiveness at a fraction of the size.

**Relevance to memex:** The cross-encoder reranker uses MS MARCO fine-tuned MiniLM-L-6-v2. Small enough for local inference, effective enough for reranking.

---

## Collaborative Intelligence Context

**Hemmer, P., Schemmer, M., Riefle, L., Vossing, M., & Kuehl, N. (2024). "Complementarity in Human-AI Collaboration." European Journal of Information Systems.**

Complementary AI design -- where human and AI capabilities combine to exceed either alone -- requires that the human remain actively engaged. Substitutive designs (AI does the work) produce dependency.

**Relevance to memex:** Memex is a retrieval tool, not a synthesis tool. It surfaces fragments for the human to interpret, connect, and act on. The human does the thinking; memex does the finding.
