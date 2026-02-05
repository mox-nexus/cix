# data-store

Production patterns for storage and retrieval: backends, search, embeddings, RAG.

## When to Use

- Choosing storage backend for vectors/search
- Implementing hybrid search (keyword + semantic)
- Selecting embedding models
- Building RAG retrieval layers
- Personal corpus/knowledge base systems

## Quick Guidance

**Backend selection:**
- <100K docs → DuckDB, SQLite, LanceDB (embedded)
- 100K-50M → PostgreSQL + pgvector ← Most apps
- 50M-1B → Qdrant, Weaviate
- >1B → Milvus, ClickHouse

**Search mode:**
- Default to **hybrid (RRF)** — recall improves 0.72 → 0.91 over BM25 alone
- Use RRF (rank-based), not score blending

**Embedding models:**
- Personal corpus: Nomic Embed v1.5 (768 dims)
- Speed-critical: all-MiniLM-L6-v2 (384 dims)
- Best accuracy: Voyage-4-Large API (1024 dims)

## Skills

| Skill | Use When |
|-------|----------|
| `data-store` | Storage selection, search implementation, embedding choices |

## References

- `storage-backends.md` — Backend selection, scaling
- `search-algorithms.md` — HNSW, IVF, BM25, SPLADE
- `embedding-models.md` — Model comparison
- `hybrid-patterns.md` — RRF, re-ranking
- `rag-architecture.md` — Chunking, CRAG, Self-RAG
- `duckdb-search.md` — DuckDB FTS/VSS specifics
