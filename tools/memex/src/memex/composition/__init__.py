"""Composition root - wires adapters to ports.

Single location for dependency injection.
All driving adapters (CLI, API, MCP) import from here.

Architecture note (from Burner):
- Embedder declares dimensions
- Composition root extracts dimension, passes to corpus
- Corpus schema is created with embedder's dimensions
- Mismatch is impossible by construction
"""

from functools import lru_cache
from pathlib import Path

from memex.adapters._out.corpus import DuckDBCorpus
from memex.adapters._out.sources import ClaudeConversationsAdapter, OpenAIConversationsAdapter
from memex.config.settings import get_settings
from memex.domain.ports._out.embedding import EmbeddingPort
from memex.domain.services import ExcavationService


class EmbeddingDimensionMismatchError(Exception):
    """Raised when corpus dimensions don't match embedder dimensions."""

    pass


# Shorthand → ONNX Runtime provider name
_PROVIDER_MAP = {
    "coreml": "CoreMLExecutionProvider",
    "cuda": "CUDAExecutionProvider",
    "cpu": "CPUExecutionProvider",
}


def _detect_providers(override: str = "auto") -> list[str]:
    """Resolve ONNX execution providers.

    Args:
        override: "auto" for hardware detection, or explicit shorthand
                  ("coreml", "cuda", "cpu").

    Returns:
        Ordered provider list for ONNX Runtime (tries in order, CPU always last).

    Raises:
        ValueError: If override is not a recognized provider name.
    """
    if override != "auto":
        key = override.lower()
        if key not in _PROVIDER_MAP:
            valid = ", ".join(sorted(_PROVIDER_MAP))
            raise ValueError(f"Unknown ONNX provider '{override}'. Valid values: auto, {valid}")
        providers = [_PROVIDER_MAP[key]]
        if key != "cpu":
            providers.append("CPUExecutionProvider")
        return providers

    # Auto-detect: prefer CoreML > CUDA > CPU
    try:
        import onnxruntime

        available = onnxruntime.get_available_providers()
    except ImportError:
        return ["CPUExecutionProvider"]

    for preferred in ["CoreMLExecutionProvider", "CUDAExecutionProvider"]:
        if preferred in available:
            return [preferred, "CPUExecutionProvider"]

    return ["CPUExecutionProvider"]


@lru_cache(maxsize=1)
def get_embedder() -> EmbeddingPort:
    """Get or create embedder (cached, lazy load).

    Uses fastembed (ONNX) with nomic-embed-text-v1.5 (768-dim).
    No torch dependency. Same quality as nomic[local], cosine ~0.9999.
    ONNX resource settings flow from Settings (env vars / config.toml).
    """
    from memex.adapters._out.embedding.fastembed_embedder import FastEmbedEmbedder

    s = get_settings()
    providers = _detect_providers(s.onnx_provider)
    return FastEmbedEmbedder(
        onnx_batch_size=s.onnx_batch_size,
        onnx_threads=s.onnx_threads,
        providers=providers,
    )


def reranker_available() -> bool:
    """Check if reranker dependencies are installed."""
    try:
        from fastembed.rerank.cross_encoder import TextCrossEncoder  # noqa: F401

        return True
    except ImportError:
        return False


@lru_cache(maxsize=1)
def get_reranker():
    """Get or create reranker (cached, lazy load).

    Uses fastembed (ONNX) — no torch dependency.
    Returns None if fastembed not installed.
    """
    if not reranker_available():
        return None

    from memex.adapters._out.reranking.fastembed_reranker import FastEmbedReranker

    s = get_settings()
    providers = _detect_providers(s.onnx_provider)
    return FastEmbedReranker(providers=providers)


def create_service(
    with_embedder: bool = False,
    with_reranker: bool = False,
) -> ExcavationService:
    """Wire up the excavation service with adapters.

    Args:
        with_embedder: Whether to include embedding capability
                      (adds ~1s startup for model loading)
        with_reranker: Whether to include reranking capability
                      (auto-disabled if deps not installed)

    Returns:
        Fully wired ExcavationService

    Raises:
        EmbeddingDimensionMismatchError: If existing corpus has different dimensions
                                         than the embedder. Requires migration.
    """
    embedder = get_embedder() if with_embedder else None

    # Corpus dimensions flow from embedder
    embedding_dim = embedder.dimensions if embedder else None
    corpus = DuckDBCorpus(get_settings().corpus_path, embedding_dim=embedding_dim)

    # Fail-fast: validate existing corpus dimensions match embedder
    if embedder:
        corpus_dims = corpus.embedding_dimensions()
        if corpus_dims and corpus_dims != embedder.dimensions:
            corpus.close()
            raise EmbeddingDimensionMismatchError(
                f"Corpus has {corpus_dims}-dim embeddings but embedder produces "
                f"{embedder.dimensions}-dim vectors. "
                f"Run 'memex reset' to clear corpus and re-ingest with new model."
            )
        # Record embedding provenance in meta
        corpus.set_meta("embedding_model", embedder.model_name)
        corpus.set_meta("embedding_dimensions", str(embedder.dimensions))

    adapters = [
        ClaudeConversationsAdapter(),
        OpenAIConversationsAdapter(),
    ]

    reranker = get_reranker() if with_reranker else None
    return ExcavationService(corpus, adapters, embedder, reranker)


def create_corpus(embedding_dim: int | None = None) -> DuckDBCorpus:
    """Direct corpus access (for SQL escape hatch commands).

    Args:
        embedding_dim: If provided, enables embedding column with this dimension.
                      If None, FTS-only mode.
    """
    return DuckDBCorpus(get_settings().corpus_path, embedding_dim=embedding_dim)


def initialize_corpus(corpus_path: Path) -> None:
    """Create an empty corpus at the given path.

    Used by init commands to bootstrap a new corpus without
    needing to know the adapter implementation.
    """
    corpus = DuckDBCorpus(corpus_path)
    corpus.close()


__all__ = [
    "_detect_providers",
    "create_service",
    "create_corpus",
    "get_embedder",
    "get_reranker",
    "initialize_corpus",
    "reranker_available",
    "EmbeddingDimensionMismatchError",
]
