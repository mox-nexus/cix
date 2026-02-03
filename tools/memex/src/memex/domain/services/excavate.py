"""Excavation service - use case orchestration.

Orchestrates ingestion and search through ports (Burner).
Uses domain types only, no infrastructure leakage.
"""

from collections.abc import Callable
from pathlib import Path

from memex.domain.models import Fragment
from memex.domain.ports._out.corpus import CorpusPort
from memex.domain.ports._out.embedding import EmbeddingPort
from memex.domain.ports._out.reranker import RerankerPort
from memex.domain.ports._out.source import SourceAdapterPort


class ExcavationService:
    """Orchestrates excavation use cases.

    Connects source adapters to corpus storage through ports.
    Supports semantic search when embedder is provided.
    Supports cross-encoder reranking when reranker is provided.
    """

    def __init__(
        self,
        corpus: CorpusPort,
        source_adapters: list[SourceAdapterPort],
        embedder: EmbeddingPort | None = None,
        reranker: RerankerPort | None = None,
    ):
        self.corpus = corpus
        self.source_adapters = source_adapters
        self.embedder = embedder
        self.reranker = reranker

    def ingest(
        self,
        path: Path,
        on_progress: Callable[[int], None] | None = None,
    ) -> int:
        """Ingest a file into the corpus.

        Returns count of fragments stored.
        """
        adapter = self._find_adapter(path)
        if not adapter:
            raise ValueError(f"No adapter found for {path}")

        # Count fragments for progress reporting
        fragment_count = 0

        def counting_generator():
            nonlocal fragment_count
            for fragment in adapter.ingest(path):
                fragment_count += 1
                yield fragment

        # Store fragments (adapter yields Iterator[Fragment])
        stored = self.corpus.store(counting_generator())

        if on_progress:
            on_progress(fragment_count)

        return stored

    def search(
        self,
        query: str,
        limit: int = 20,
        source_kind: str | None = None,
    ) -> list[Fragment]:
        """Search the corpus (keyword-based).

        Args:
            query: Search terms (space-separated, all must match)
            limit: Maximum results
            source_kind: Optional filter by source type
        """
        return self.corpus.search(query, limit, source_kind)

    def semantic_search(
        self,
        query: str,
        limit: int = 20,
        source_kind: str | None = None,
        min_score: float = 0.3,
    ) -> list[tuple[Fragment, float]]:
        """Search the corpus by semantic similarity.

        Args:
            query: Natural language query
            limit: Maximum results
            source_kind: Optional filter by source type
            min_score: Minimum similarity threshold (0-1)

        Returns:
            List of (Fragment, score) tuples.
            Empty list if embedder not available.
        """
        if not self.embedder:
            return []

        query_embedding = self.embedder.embed(query)
        return self.corpus.semantic_search(
            query_embedding, limit, source_kind, min_score
        )

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
        avoiding score normalization issues. Optionally applies cross-encoder
        reranking for improved precision.

        Args:
            query: Search query
            limit: Maximum results
            source_kind: Optional filter by source type
            semantic_weight: Weight for semantic ranks (0-1)
            use_reranker: Whether to apply reranking if available

        Returns:
            List of (Fragment, score) tuples sorted by RRF/reranker score.
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
        combined = [
            (fragments[frag_id], score)
            for frag_id, score in scores.items()
        ]
        combined.sort(key=lambda x: x[1], reverse=True)

        # Apply reranking if available
        if self.reranker and use_reranker:
            # Take top candidates for reranking (50-100 is typical)
            rerank_candidates = [frag for frag, _ in combined[:min(50, len(combined))]]
            return self.reranker.rerank(query, rerank_candidates, limit)

        return combined[:limit]

    def find_conversation(self, conversation_id: str) -> list[Fragment]:
        """Get all fragments in a conversation."""
        return self.corpus.find_by_conversation(conversation_id)

    def stats(self) -> dict:
        """Get corpus statistics."""
        return self.corpus.stats()

    def schema(self) -> dict:
        """Get corpus schema."""
        return self.corpus.schema()

    def available_sources(self) -> list[str]:
        """List available source adapters."""
        return [adapter.source_kind() for adapter in self.source_adapters]

    def get_source_skill(self, source_kind: str) -> str | None:
        """Get skill documentation for a source adapter."""
        for adapter in self.source_adapters:
            if adapter.source_kind() == source_kind:
                return adapter.skill()
        return None

    def get_corpus_skill(self) -> str:
        """Get skill documentation for the corpus."""
        return self.corpus.skill()

    def backfill_embeddings(
        self,
        batch_size: int = 100,
        on_progress: Callable[[int, int], None] | None = None,
    ) -> int:
        """Backfill embeddings for existing fragments.

        Args:
            batch_size: Fragments per batch
            on_progress: Callback(processed, total)

        Returns:
            Number of fragments updated.
        """
        if not self.embedder:
            return 0
        return self.corpus.backfill_embeddings(
            self.embedder.embed_batch, batch_size, on_progress
        )

    def embedding_coverage(self) -> tuple[int, int]:
        """Get embedding coverage stats.

        Returns:
            (fragments_with_embeddings, total_fragments)
        """
        stats = self.corpus.stats()
        total = stats.get("total_fragments", 0)
        without = self.corpus.count_without_embeddings()
        return (total - without, total)

    def has_semantic_search(self) -> bool:
        """Check if semantic search is available."""
        return self.embedder is not None and self.corpus.has_vss()

    def has_reranker(self) -> bool:
        """Check if cross-encoder reranking is available."""
        return self.reranker is not None

    def reranker_model_name(self) -> str | None:
        """Get reranker model name for display."""
        if self.reranker:
            return self.reranker.model_name
        return None

    def _find_adapter(self, path: Path) -> SourceAdapterPort | None:
        for adapter in self.source_adapters:
            if adapter.can_handle(path):
                return adapter
        return None
