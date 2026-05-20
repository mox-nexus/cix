"""Sentence-transformers embedding adapter using PyTorch.

Uses the GPU (MPS on Apple Silicon, CUDA on Linux/Windows) for fast
inference. Supports any sentence-transformers compatible model,
defaulting to EmbeddingGemma for on-device performance.

This adapter replaces the fastembed/ONNX path when the `gpu` extra
is installed. The key difference: PyTorch MPS handles dynamic input
shapes natively — no CoreML shape-cache explosion, no ONNX arena
grow-only behavior. On Apple Silicon, batch_size=64 is comfortable
in unified memory.
"""

from collections.abc import Iterator
from functools import cached_property
from itertools import batched

from memex.domain.models import EmbeddingConfig

# Cap input text to ~2K tokens worth of characters. EmbeddingGemma has
# a 2K token context window; nomic has 8K but we cap to 4K anyway.
# At ~4 chars/token, 4000 chars ≈ 1000 tokens. Safe for both models.
_MAX_EMBED_CHARS = 4000


class SentenceTransformerEmbedder:
    """Embedding via sentence-transformers (PyTorch).

    Auto-detects device:
    - Apple Silicon → MPS (Metal Performance Shaders)
    - NVIDIA GPU → CUDA
    - Fallback → CPU

    Default model: google/embedding-gemma-2k-v1.1 (308M params, 768-dim,
    Matryoshka, <200MB quantized, best-in-class under 500M on MTEB).
    """

    DEFAULT_MODEL = "google/embedding-gemma-2k-v1.1"
    DEFAULT_DIM = 768
    DEFAULT_BATCH_SIZE = 64

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        dimensions: int = DEFAULT_DIM,
        batch_size: int = DEFAULT_BATCH_SIZE,
        device: str | None = None,
    ):
        self._model_name = model_name
        self._dimensions = dimensions
        self._batch_size = batch_size
        self._device = device

    @cached_property
    def model(self):
        """Lazy load the model on first use."""
        from sentence_transformers import SentenceTransformer

        device = self._device or _detect_device()
        return SentenceTransformer(
            self._model_name,
            device=device,
            truncate_dim=self._dimensions,
        )

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
        """Embed a single text. Returns vector."""
        result = self.model.encode(
            [text[:_MAX_EMBED_CHARS]],
            batch_size=1,
            show_progress_bar=False,
            normalize_embeddings=True,
        )
        return result[0].tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts. Materializes all results."""
        if not texts:
            return []
        capped = [t[:_MAX_EMBED_CHARS] for t in texts]
        results = self.model.encode(
            capped,
            batch_size=self._batch_size,
            show_progress_bar=False,
            normalize_embeddings=True,
        )
        return [r.tolist() for r in results]

    def embed_stream(self, texts: Iterator[str]) -> Iterator[list[float]]:
        """Stream embeddings in chunks.

        Processes ``batch_size`` texts per encode() call. PyTorch MPS
        handles dynamic shapes natively — no shape-cache explosion.
        Each chunk's GPU memory is released after encode() returns.
        """
        for chunk in batched(texts, self._batch_size):
            capped = [t[:_MAX_EMBED_CHARS] for t in chunk]
            results = self.model.encode(
                capped,
                batch_size=self._batch_size,
                show_progress_bar=False,
                normalize_embeddings=True,
            )
            for vec in results:
                yield vec.tolist()


def _detect_device() -> str:
    """Auto-detect best available PyTorch device."""
    try:
        import torch

        if torch.backends.mps.is_available():
            return "mps"
        if torch.cuda.is_available():
            return "cuda"
    except (ImportError, AttributeError):
        pass
    return "cpu"
