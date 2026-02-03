"""Embedding port - interface for text vectorization.

Converts text to embeddings for semantic search.
Implementation details (model choice) stay in adapters.
"""

from typing import Protocol

from memex.domain.models import EmbeddingConfig


class EmbeddingPort(Protocol):
    """Protocol for text embedding.

    Converts text → vector for semantic similarity search.
    """

    def embed(self, text: str) -> list[float]:
        """Embed a single text. Returns vector."""
        ...

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts. Returns list of vectors."""
        ...

    @property
    def model_name(self) -> str:
        """Return the model name."""
        ...

    @property
    def dimensions(self) -> int:
        """Return embedding dimensions."""
        ...

    @property
    def config(self) -> EmbeddingConfig:
        """Return embedding configuration for this embedder."""
        ...
