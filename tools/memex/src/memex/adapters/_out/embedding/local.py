"""Local embedding adapter using sentence-transformers.

Free, fast, runs locally. Good enough for personal corpus search.
"""

from functools import cached_property

from sentence_transformers import SentenceTransformer

from memex.domain.models import EmbeddingConfig


class LocalEmbedder:
    """Local embedding using sentence-transformers (MiniLM).

    Uses all-MiniLM-L6-v2:
    - 384 dimensions
    - ~5ms per embedding
    - Good quality for semantic search
    - Runs locally, no API costs
    """

    MODEL_NAME = "all-MiniLM-L6-v2"
    EMBEDDING_DIM = 384

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
        return SentenceTransformer(self.MODEL_NAME)

    def embed(self, text: str) -> list[float]:
        """Embed a single text. Returns 384-dim vector."""
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts. More efficient than single calls."""
        if not texts:
            return []
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()
