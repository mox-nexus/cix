"""Embedding port - interface for text vectorization.

Stream is the primitive. Single and batch are convenience methods.
Implementation details (model choice) stay in adapters.
"""

from collections.abc import Iterator
from typing import Protocol

from memex.domain.models import EmbeddingConfig


class EmbeddingPort(Protocol):
    """Protocol for text embedding.

    Converts text → vector for semantic similarity search.

    embed_stream() is the primitive: Iterator[str] → Iterator[list[float]].
    1:1 streaming transform. Texts in, vectors out. Nothing materializes
    beyond the ONNX batch boundary.

    embed() and embed_batch() are convenience methods for non-bulk paths
    (queries, small batches). They materialize results.
    """

    def embed(self, text: str) -> list[float]:
        """Embed a single text. Returns vector."""
        ...

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts. Materializes all results."""
        ...

    def embed_stream(self, texts: Iterator[str]) -> Iterator[list[float]]:
        """Stream embeddings one at a time. For bulk operations.

        Accepts an iterator of texts, yields one embedding per text.
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
