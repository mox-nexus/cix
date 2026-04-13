# Cognee: Architecture Reference

**Source:** github.com/topoteretes/cognee, docs.cognee.ai, cognee.ai/blog
**As of:** April 2026

---

## What It Is

A knowledge-graph-first memory engine. The entire API is three operations: `add()`, `cognify()`, `search()`. Unstructured data goes in; a queryable knowledge graph comes out. The graph is the primary data structure, not an add-on.

## The Pipeline

```
┌─────────────────────────────────────────────────────────┐
│  add(source)                                            │
│  Accepts 30+ types: PDFs, CSVs, audio, images, S3,     │
│  Slack, code files, API responses                       │
│  → Registered and stored. No transformation yet.        │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│  cognify()  — The Core ETL (6 steps, ordered)           │
│                                                         │
│  1. Classify documents     (algorithmic)                │
│  2. Check permissions      (algorithmic)                │
│  3. Extract chunks         (algorithmic)                │
│     chunk_size = min(embedding_max, llm_max // 2)       │
│                                                         │
│  4. Extract graph          (LLM — the critical step)    │
│     LLM + Instructor/BAML → Pydantic KnowledgeGraph    │
│     typed Node and Edge objects                         │
│     e.g., Node("Alice", type="Person")                  │
│           Edge("Alice", "works_at", "Acme")             │
│                                                         │
│  5. Summarize text         (LLM)                        │
│     hierarchical summaries per chunk                    │
│                                                         │
│  6. Add data points        (algorithmic)                │
│     → embed nodes + summaries → vector store            │
│     → write entities + edges → graph DB                 │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│  search(query, type)                                    │
│                                                         │
│  CHUNKS     → vector similarity on chunk embeddings     │
│  SUMMARIES  → vector similarity on summary embeddings   │
│  GRAPH_COMPLETION → vector search finds entities,       │
│                     graph traversal extracts relations   │
│                     → structured triples                │
│  INSIGHTS   → LLM routes query to best search type      │
└─────────────────────────────────────────────────────────┘
```

## What the LLM Decides vs What Is Algorithmic

| Step | LLM | Algorithmic |
|------|-----|-------------|
| Document classification | | x |
| Permission check | | x |
| Chunking | | x |
| **Entity + relationship extraction** | **x** | |
| Summarization | x | |
| Embedding computation | | x |
| Graph storage / vector indexing | | x |
| Graph traversal at query time | | x |
| Query routing (INSIGHTS mode only) | x | |

The LLM's output is **constrained via Instructor or BAML** — it must produce typed Pydantic objects (Node, Edge), not freeform text. The schema enforcement is the critical design choice: the LLM extracts structure, but the structure is machine-defined.

## Storage: Three Parallel Stores

| Layer | Default (zero-config) | Production |
|-------|----------------------|------------|
| Graph (entities, edges, traversal) | **Kuzu** (embedded, file-based) | Neo4j, Memgraph, FalkorDB |
| Vector (embeddings, similarity) | **LanceDB** (embedded, file-based) | Qdrant, Weaviate, Milvus, pgvector |
| Relational (provenance, metadata) | **SQLite** | Postgres |

All defaults are file-based. `pip install cognee` + an LLM key = running system. No Docker, no infrastructure.

## Ontology Validation (Optional)

An OWL ontology validation layer sits between LLM extraction and storage. Entity types are fuzzy-matched to OWL Classes (80% cutoff). This constrains the graph to a controlled vocabulary. Without it, the LLM invents whatever types it wants.

## Search Types Explained

- **CHUNKS:** Pure vector similarity on chunk embeddings. Fastest. No graph, no LLM at query time.
- **SUMMARIES:** Vector similarity on pre-computed summary nodes. Fast overviews.
- **GRAPH_COMPLETION:** Vector search finds relevant entities → graph traversal extracts relationships → returns structured triples. This is the multi-hop capability. "Alice works at Acme" + "Acme is in Berlin" → "Where does Alice work?" requires traversing two edges.
- **INSIGHTS:** Meta-search. LLM analyzes query, routes to best type.

The hybrid pattern: vectors find relevant nodes fast, graph traversal grounds them in structure. Vectors answer "what is similar?"; graph answers "how does it connect?"

## Performance

- HotPotQA benchmark (multi-hop QA): 0.93 human-like correctness
- Mem0 comparison: Mem0's entities end up in disconnected clusters with no inter-entity links even when relationships are stated in input. Cognee maintains the full graph.

## The "Memify" Pipeline

Runs post-deployment to maintain graph quality: clean stale nodes, strengthen associations, reweight facts. Avoids full rebuilds for incremental updates.

## What Cognee Does NOT Do

- No temporal validity model (no valid_at/invalid_at — unlike Zep)
- No concept of solidification or memory consolidation
- No trail or associative path
- No conversation-native storage (conversations are chunked like documents)
- No context-dependent retrieval (vector + graph, but all content-based)
- Requires LLM for ingestion (cognify step) — no offline extraction

## What Cognee Gets Right

- **Graph is the primary structure, not an add-on.** Graph features are open-source, not paywalled (contrast with Mem0).
- **Schema-constrained LLM extraction.** Pydantic types + Instructor enforcement means the LLM fills structured slots, not freeform text.
- **All defaults are embedded/file-based.** Kuzu + LanceDB + SQLite = zero infrastructure.
- **LanceDB as vector backend.** Same storage choice as memex.

## Sources

- https://github.com/topoteretes/cognee
- https://docs.cognee.ai
- https://www.cognee.ai/blog/deep-dives/ai-memory-tools-evaluation
- https://www.lancedb.com/blog/case-study-cognee
