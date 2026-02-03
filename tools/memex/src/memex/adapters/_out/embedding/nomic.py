"""Nomic embedding adapter using sentence-transformers.

Higher quality embeddings with 768 dimensions.
"""

from functools import cached_property

from sentence_transformers import SentenceTransformer

from memex.domain.models import EmbeddingConfig


class NomicEmbedder:
    """Nomic embedding using nomic-embed-text-v1.5.

    - 768 dimensions
    - 8192 token context window
    - Strong retrieval performance (MTEB ~69)
    - Matryoshka embeddings (can truncate if needed)
    - Runs locally, no API costs
    """

    MODEL_NAME = "nomic-ai/nomic-embed-text-v1.5"
    EMBEDDING_DIM = 768

    def __init__(self):
        self._model: SentenceTransformer | None = None

    @property
    def model_name(self) -> str:
        return self.MODEL_NAME

    @property
    def dimensions(self) -> int:
        return self.EMBEDDING_DIM

    @property
    def config(self) -> EmbeddingConfig:
        return EmbeddingConfig(model_name=self.model_name, dimensions=self.dimensions)

    @cached_property
    def model(self) -> SentenceTransformer:
        """Lazy load model on first use."""
        return SentenceTransformer(self.MODEL_NAME, trust_remote_code=True)

    def embed(self, text: str) -> list[float]:
        """Embed a single text. Returns 768-dim vector."""
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts. More efficient than single calls."""
        if not texts:
            return []
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()
