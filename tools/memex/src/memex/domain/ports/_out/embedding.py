"""Embedding port - interface for text vectorization.

Converts text to embeddings for semantic search.
Implementation details (model choice) stay in adapters.
"""

from collections.abc import Iterator
from typing import Protocol

from memex.domain.models import EmbeddingConfig


class EmbeddingPort(Protocol):
    """Protocol for text embedding.

    Converts text → vector for semantic similarity search.

    Three interfaces:
    - embed(): single text, returns vector (for queries)
    - embed_batch(): multiple texts, materializes all (for small batches)
    - embed_stream(): multiple texts, yields one at a time (for bulk ops)
    """

    def embed(self, text: str) -> list[float]:
        """Embed a single text. Returns vector."""
        ...

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts. Returns list of vectors."""
        ...

    def embed_stream(self, texts: list[str]) -> Iterator[list[float]]:
        """Stream embeddings one at a time. For bulk operations.

        Callers should consume and write each vector immediately
        rather than collecting them all in memory.
        """
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
