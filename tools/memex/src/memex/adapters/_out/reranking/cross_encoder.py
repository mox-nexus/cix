"""Cross-encoder reranker using sentence-transformers.

Provides +15-20% precision improvement over bi-encoder similarity.
Model is loaded lazily on first use to avoid startup cost.

Requires: pip install memex[rerank]
"""

from functools import cached_property

from memex.domain.models import Fragment


class CrossEncoderReranker:
    """Cross-encoder reranker using MS MARCO trained models.

    Uses sentence-transformers CrossEncoder for query-document scoring.
    The model sees both query and document together, enabling richer
    interaction modeling than bi-encoders.

    Default model: cross-encoder/ms-marco-MiniLM-L-6-v2
    - 74.30 NDCG@10 on MS MARCO
    - ~1800 docs/sec throughput
    - Good balance of speed and accuracy
    """

    DEFAULT_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

    def __init__(self, model_name: str = DEFAULT_MODEL):
        """Initialize reranker with model name.

        Model is loaded lazily on first rerank() call.

        Args:
            model_name: HuggingFace model ID for cross-encoder
        """
        self._model_name = model_name
        self._model = None

    @cached_property
    def model(self):
        """Lazy load the cross-encoder model."""
        from sentence_transformers import CrossEncoder

        return CrossEncoder(self._model_name)

    def rerank(
        self,
        query: str,
        candidates: list[Fragment],
        top_k: int = 10,
    ) -> list[tuple[Fragment, float]]:
        """Rerank candidates by relevance to query.

        Args:
            query: The search query
            candidates: Fragments to rerank
            top_k: Number of top results to return

        Returns:
            List of (Fragment, score) tuples, sorted by score descending.
        """
        if not candidates:
            return []

        # Create query-document pairs for cross-encoder
        pairs = [(query, frag.content) for frag in candidates]

        # Score all pairs in batch
        scores = self.model.predict(pairs)

        # Combine with fragments and sort
        scored = list(zip(candidates, scores))
        scored.sort(key=lambda x: x[1], reverse=True)

        return scored[:top_k]

    @property
    def model_name(self) -> str:
        """Return the model name for display/logging."""
        return self._model_name
