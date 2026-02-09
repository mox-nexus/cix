"""Nomic embedding adapter using GPT4All local inference.

Higher quality embeddings with 768 dimensions.
Runs locally on CPU/GPU via GPT4All backend (Metal on macOS).
Install with: uv add nomic[local]
"""

from memex.domain.models import EmbeddingConfig


class NomicEmbedder:
    """Nomic embedding using nomic-embed-text-v1.5 with local inference.

    - 768 dimensions (full Matryoshka)
    - 2048 token context window (local mode)
    - Strong retrieval performance (MTEB ~69)
    - Runs locally via GPT4All (Metal on macOS, CUDA on Linux)
    - No API costs, no network required after model download
    """

    MODEL_NAME = "nomic-embed-text-v1.5"
    EMBEDDING_DIM = 768

    @property
    def model_name(self) -> str:
        return self.MODEL_NAME

    @property
    def dimensions(self) -> int:
        return self.EMBEDDING_DIM

    @property
    def config(self) -> EmbeddingConfig:
        return EmbeddingConfig(model_name=self.model_name, dimensions=self.dimensions)

    def embed(self, text: str) -> list[float]:
        """Embed a single text. Returns 768-dim vector."""
        from nomic import embed

        output = embed.text(
            texts=[text],
            model=self.MODEL_NAME,
            task_type="search_document",
            inference_mode="local",
        )
        return output["embeddings"][0]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts in batch."""
        if not texts:
            return []

        from nomic import embed

        output = embed.text(
            texts=texts,
            model=self.MODEL_NAME,
            task_type="search_document",
            inference_mode="local",
        )
        return output["embeddings"]
