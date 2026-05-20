"""MLX embedding adapter for Apple Silicon.

Native Metal inference via mlx-embeddings. No ONNX, no CoreML shape
cache, no PyTorch. Handles dynamic input shapes natively on unified
memory. On M1 Max (32-core GPU, 64 GB), expect ~400-800 texts/sec
at batch_size=64 with the 0.6B model.

Install: uv add mlx-embeddings (pulls mlx + mlx-metal automatically)
"""

from collections.abc import Iterator
from functools import cached_property
from itertools import batched

from memex.domain.models import EmbeddingConfig

_MAX_EMBED_CHARS = 4000


class MLXEmbedder:
    """Embedding via mlx-embeddings on Apple Silicon.

    Default model: Qwen3-Embedding-0.6B-4bit-DWQ (quantized, ~300 MB).
    768-dim output, Matryoshka support (truncatable to 128/256/512).
    """

    DEFAULT_MODEL = "mlx-community/Qwen3-Embedding-0.6B-4bit-DWQ"
    DEFAULT_DIM = 768
    DEFAULT_BATCH_SIZE = 64

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL,
        dimensions: int = DEFAULT_DIM,
        batch_size: int = DEFAULT_BATCH_SIZE,
    ):
        self._model_name = model_name
        self._dimensions = dimensions
        self._batch_size = batch_size

    @cached_property
    def _model_and_tokenizer(self):
        """Lazy load model + tokenizer on first use."""
        from mlx_embeddings.utils import load

        return load(self._model_name)

    @property
    def _model(self):
        return self._model_and_tokenizer[0]

    @property
    def _tokenizer(self):
        return self._model_and_tokenizer[1]

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def dimensions(self) -> int:
        return self._dimensions

    @property
    def config(self) -> EmbeddingConfig:
        return EmbeddingConfig(model_name=self.model_name, dimensions=self.dimensions)

    def _embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of texts. Returns list of vectors."""
        import mlx.core as mx

        capped = [t[:_MAX_EMBED_CHARS] for t in texts]
        inputs = self._tokenizer.batch_encode_plus(
            capped,
            return_tensors="mlx",
            padding=True,
            truncation=True,
            max_length=1024,
        )
        outputs = self._model(
            inputs["input_ids"],
            attention_mask=inputs.get("attention_mask"),
        )
        embeddings = outputs.text_embeds
        # Truncate to requested dimensions (Matryoshka)
        if embeddings.shape[-1] > self._dimensions:
            embeddings = embeddings[:, : self._dimensions]
        # Normalize after truncation
        norms = mx.linalg.norm(embeddings, axis=-1, keepdims=True)
        embeddings = embeddings / mx.maximum(norms, 1e-12)
        mx.eval(embeddings)
        return embeddings.tolist()

    def embed(self, text: str) -> list[float]:
        """Embed a single text."""
        return self._embed_texts([text])[0]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts."""
        if not texts:
            return []
        return self._embed_texts(texts)

    def embed_stream(self, texts: Iterator[str]) -> Iterator[list[float]]:
        """Stream embeddings in chunks.

        MLX handles dynamic shapes natively — no shape-cache explosion.
        Each chunk is a single Metal kernel dispatch. Memory is released
        between chunks by Python GC on the mlx arrays.
        """
        for chunk in batched(texts, self._batch_size):
            results = self._embed_texts(list(chunk))
            yield from results
