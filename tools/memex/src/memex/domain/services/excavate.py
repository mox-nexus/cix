"""Excavation service - use case orchestration.

Orchestrates ingestion and search through ports.
Pass-through methods removed — callers access ports directly:
  service.corpus.stats(), service.graph.edge_stats(), service.trails.list_trails()
"""

from collections.abc import Callable
from pathlib import Path

from memex.domain.models import EmbeddingCoverage, Fragment, IngestResult
from memex.domain.ports._out.corpus import CorpusPort
from memex.domain.ports._out.embedding import EmbeddingPort
from memex.domain.ports._out.graph import GraphPort
from memex.domain.ports._out.reranker import RerankerPort
from memex.domain.ports._out.source import SourcePort
from memex.domain.ports._out.trail import TrailPort


class ExcavationService:
    """Orchestrates excavation use cases.

    Connects source adapters to corpus storage through ports.
    For direct port access: service.corpus, service.graph, service.trails.
    """

    def __init__(
        self,
        corpus: CorpusPort,
        source_adapters: list[SourcePort],
        embedder: EmbeddingPort | None = None,
        reranker: RerankerPort | None = None,
        graph: GraphPort | None = None,
        trails: TrailPort | None = None,
    ):
        self.corpus = corpus
        self.source_adapters = source_adapters
        self.embedder = embedder
        self.reranker = reranker
        # DuckDBCorpus implements all three protocols.
        # When graph/trails aren't provided separately, corpus is the backend.
        self.graph: GraphPort = graph if graph is not None else corpus  # type: ignore[assignment]
        self.trails: TrailPort = trails if trails is not None else corpus  # type: ignore[assignment]

    def ingest(self, path: Path) -> IngestResult:
        """Ingest a file into the corpus.

        Returns:
            (parsed, stored) — count of fragments parsed and newly stored.
        """
        adapter = self._find_adapter(path)
        if not adapter:
            raise ValueError(f"No adapter found for {path}")

        parsed = 0

        def counting_generator():
            nonlocal parsed
            for fragment in adapter.ingest(path):
                parsed += 1
                yield fragment

        stored = self.corpus.store(counting_generator())

        # Auto-compute FOLLOWS edges for new fragments
        if stored > 0:
            self.graph.build_follows_edges()

        return IngestResult(parsed, stored)

    def semantic_search(
        self,
        query: str,
        limit: int = 20,
        source_kind: str | None = None,
        min_score: float = 0.3,
    ) -> list[tuple[Fragment, float]]:
        """Search by semantic similarity. Orchestrates embedder + corpus."""
        if not self.embedder:
            return []

        query_embedding = self.embedder.embed(query)
        return self.corpus.semantic_search(query_embedding, limit, source_kind, min_score)

    def hybrid_search(
        self,
        query: str,
        limit: int = 20,
        source_kind: str | None = None,
        semantic_weight: float = 0.6,
        use_reranker: bool = True,
    ) -> list[tuple[Fragment, float]]:
        """Search using Reciprocal Rank Fusion (RRF).

        Combines keyword and semantic results using rank-based fusion,
        optionally applies cross-encoder reranking for improved precision.
        """
        k = 60  # RRF constant (Elasticsearch/Azure/OpenSearch standard)
        keyword_weight = 1.0 - semantic_weight

        # Retrieve more candidates if reranking (reranker refines top-k)
        retrieval_limit = limit * 3 if (self.reranker and use_reranker) else limit * 2

        # Get keyword results
        keyword_results = self.corpus.search(query, retrieval_limit, source_kind)

        # Build RRF scores and fragment lookup
        scores: dict[str, float] = {}
        fragments: dict[str, Fragment] = {}

        for rank, frag in enumerate(keyword_results):
            scores[frag.id] = keyword_weight / (rank + k)
            fragments[frag.id] = frag

        # Add semantic results if available
        if self.embedder:
            semantic_results = self.semantic_search(
                query, retrieval_limit, source_kind, min_score=0.0
            )
            for rank, (frag, _) in enumerate(semantic_results):
                scores[frag.id] = scores.get(frag.id, 0) + semantic_weight / (rank + k)
                if frag.id not in fragments:
                    fragments[frag.id] = frag

        # Sort by RRF score
        combined = [(fragments[frag_id], score) for frag_id, score in scores.items()]
        combined.sort(key=lambda x: x[1], reverse=True)

        # Apply reranking if available
        if self.reranker and use_reranker:
            rerank_candidates = [frag for frag, _ in combined[: min(50, len(combined))]]
            return self.reranker.rerank(query, rerank_candidates, limit)

        return combined[:limit]

    def backfill_embeddings(
        self,
        batch_size: int = 100,
        on_progress: Callable[[int, int], None] | None = None,
    ) -> int:
        """Backfill embeddings for existing fragments. Orchestrates embedder + corpus."""
        if not self.embedder:
            return 0
        return self.corpus.backfill_embeddings(self.embedder.embed_stream, batch_size, on_progress)

    def embedding_coverage(self) -> EmbeddingCoverage:
        """Get embedding coverage."""
        stats = self.corpus.stats()
        total = stats.total_fragments
        without = self.corpus.count_without_embeddings()
        return EmbeddingCoverage(with_embeddings=total - without, total=total)

    def has_semantic_search(self) -> bool:
        """Check if semantic search is available (embedder + corpus support)."""
        return self.embedder is not None and self.corpus.has_semantic_search()

    def has_reranker(self) -> bool:
        """Check if cross-encoder reranking is available."""
        return self.reranker is not None

    def reranker_model_name(self) -> str | None:
        """Get reranker model name for display."""
        return self.reranker.model_name if self.reranker else None

    def available_sources(self) -> list[str]:
        """List available source adapter kinds."""
        return [adapter.source_kind() for adapter in self.source_adapters]

    def close(self) -> None:
        """Release resources."""
        self.corpus.close()

    def _find_adapter(self, path: Path) -> SourcePort | None:
        for adapter in self.source_adapters:
            if adapter.can_handle(path):
                return adapter
        return None
