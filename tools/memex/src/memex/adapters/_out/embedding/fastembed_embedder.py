"""Fastembed embedding adapter using ONNX runtime.

No torch dependency. Same nomic-embed-text-v1.5 quality, ONNX backend.
Replaces both LocalEmbedder (sentence-transformers) and NomicEmbedder (GPT4All).
"""

from functools import cached_property

from memex.domain.models import EmbeddingConfig


class FastEmbedEmbedder:
    """Embedding via fastembed (ONNX).

    Uses nomic-ai/nomic-embed-text-v1.5:
    - 768 dimensions
    - ONNX runtime (no torch)
    - Same quality as nomic[local], cosine ~0.9999
    - ~12x faster inference than sentence-transformers
    """

    DEFAULT_MODEL = "nomic-ai/nomic-embed-text-v1.5"
    EMBEDDING_DIM = 768
    DEFAULT_ONNX_BATCH_SIZE = 4
    DEFAULT_ONNX_THREADS = 2

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        dimensions: int = EMBEDDING_DIM,
        onnx_batch_size: int = DEFAULT_ONNX_BATCH_SIZE,
        onnx_threads: int = DEFAULT_ONNX_THREADS,
    ):
        self._model_name = model_name
        self._dimensions = dimensions
        self._onnx_batch_size = onnx_batch_size
        self._onnx_threads = onnx_threads

    @cached_property
    def model(self):
        """Lazy load the embedding model."""
        from fastembed import TextEmbedding

        return TextEmbedding(model_name=self._model_name, threads=self._onnx_threads)

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def dimensions(self) -> int:
        return self._dimensions

    @property
    def config(self) -> EmbeddingConfig:
        return EmbeddingConfig(model_name=self.model_name, dimensions=self.dimensions)

    def embed(self, text: str) -> list[float]:
        """Embed a single text. Returns 768-dim vector."""
        embeddings = list(self.model.embed([text], batch_size=1))
        return embeddings[0].tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts. More efficient than single calls."""
        if not texts:
            return []
        embeddings = list(self.model.embed(texts, batch_size=self._onnx_batch_size))
        return [e.tolist() for e in embeddings]
