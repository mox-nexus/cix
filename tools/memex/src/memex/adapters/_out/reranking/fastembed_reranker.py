"""Fastembed cross-encoder reranker using ONNX runtime.

No torch dependency. Same ms-marco model quality, ~12x faster inference.
"""

from functools import cached_property

from memex.domain.models import Fragment


class FastEmbedReranker:
    """Cross-encoder reranker via fastembed (ONNX).

    Uses fastembed's TextCrossEncoder for query-document scoring.
    ONNX runtime provides fast inference without PyTorch.

    Default model: Xenova/ms-marco-MiniLM-L-6-v2
    - Same quality as sentence-transformers CrossEncoder
    - ONNX backend, no torch required
    """

    DEFAULT_MODEL = "Xenova/ms-marco-MiniLM-L-6-v2"

    def __init__(self, model_name: str = DEFAULT_MODEL):
        self._model_name = model_name

    @cached_property
    def model(self):
        """Lazy load the cross-encoder model."""
        from fastembed.rerank.cross_encoder import TextCrossEncoder

        return TextCrossEncoder(model_name=self._model_name)

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

        # fastembed 0.7+ returns floats in document order
        scores = list(self.model.rerank(query, [frag.content for frag in candidates]))
        scored = list(zip(candidates, scores))
        scored.sort(key=lambda x: x[1], reverse=True)

        return scored[:top_k]

    @property
    def model_name(self) -> str:
        """Return the model name for display/logging."""
        return self._model_name
