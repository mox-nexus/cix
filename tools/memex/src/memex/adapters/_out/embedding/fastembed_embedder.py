"""Fastembed embedding adapter using ONNX runtime.

No torch dependency. Same nomic-embed-text-v1.5 quality, ONNX backend.
Replaces both LocalEmbedder (sentence-transformers) and NomicEmbedder (GPT4All).

Memory model: fastembed's embed() returns a generator. We preserve that
generator through embed_stream() so callers can write-as-you-go without
materializing all embeddings at once. embed() and embed_batch() materialize
for convenience in non-bulk paths (single queries, small batches).
"""

from collections.abc import Iterator
from functools import cached_property
from itertools import batched

from memex.adapters._out.onnx_quiet import suppress_native_stderr
from memex.domain.models import EmbeddingConfig

# Hard cap on characters fed to the embedder. nomic-embed-text-v1.5 supports
# 8192 tokens but ~1000 tokens (~4000 chars) captures the semantic content of
# real Claude fragments without runaway attention memory. Attention is
# O(batch * seq_len²) — halving seq_len quarters per-call working set.
_MAX_EMBED_CHARS = 4000


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
        providers: list[str] | None = None,
    ):
        self._model_name = model_name
        self._dimensions = dimensions
        self._onnx_batch_size = onnx_batch_size
        self._onnx_threads = onnx_threads
        self._providers = providers

    @cached_property
    def model(self):
        """Lazy load the embedding model."""
        from fastembed import TextEmbedding

        with suppress_native_stderr():
            return TextEmbedding(
                model_name=self._model_name,
                threads=self._onnx_threads,
                providers=self._providers,
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
        """Embed a single text. Returns 768-dim vector."""
        return next(self.embed_stream(iter([text])))

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts. Materializes all results.

        Use embed_stream() for bulk operations to avoid holding
        all embeddings in memory at once.
        """
        if not texts:
            return []
        return list(self.embed_stream(iter(texts)))

    def embed_stream(self, texts: Iterator[str]) -> Iterator[list[float]]:
        """Stream embeddings one at a time from fastembed's generator.

        Each input text is capped to ``_MAX_EMBED_CHARS`` and chunked into
        ``onnx_batch_size``-sized lists, one list per ``model.embed`` call.
        This is the shape the reference pattern in the data-store skill
        prescribes, and it matters for ORT memory behavior: passing a
        large iterator through a single ``embed`` call keeps ORT's per-
        session scratch allocated for the whole iteration, which under
        length-sorted input ratchets the arena watermark across the run.
        Per-call chunking lets each ``embed`` call release its scratch
        between calls.

        Only the embedding input is clipped — fragment text stored in the
        corpus is untouched, so keyword search sees full content.
        """
        capped = (t[:_MAX_EMBED_CHARS] for t in texts)
        with suppress_native_stderr():
            for chunk in batched(capped, self._onnx_batch_size):
                chunk_list = list(chunk)
                for embedding in self.model.embed(
                    chunk_list, batch_size=self._onnx_batch_size
                ):
                    yield embedding.tolist()
