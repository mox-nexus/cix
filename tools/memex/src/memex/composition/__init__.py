"""Composition root - wires adapters to ports.

Single location for dependency injection.
All driving adapters (CLI, API, MCP) import from here.

Architecture note (from Burner):
- Embedder declares dimensions
- Composition root extracts dimension, passes to corpus
- Corpus schema is created with embedder's dimensions
- Mismatch is impossible by construction
"""

import os
from pathlib import Path

from memex.adapters._out.corpus import DuckDBCorpus
from memex.adapters._out.sources import ClaudeConversationsAdapter, OpenAIConversationsAdapter
from memex.config.settings import Settings, get_settings
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


def detect_providers(override: str = "auto") -> list[str]:
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


_embedder: EmbeddingPort | None = None


def get_embedder(settings: Settings | None = None) -> EmbeddingPort:
    """Get or create embedder (cached after first creation).

    Uses fastembed (ONNX) with nomic-embed-text-v1.5 (768-dim).
    No torch dependency. Same quality as nomic[local], cosine ~0.9999.
    ONNX resource settings flow from Settings (env vars / config.toml).
    """
    global _embedder
    if _embedder is not None:
        return _embedder

    from memex.adapters._out.embedding.fastembed_embedder import FastEmbedEmbedder

    s = settings or get_settings()
    providers = detect_providers(s.onnx_provider)
    _embedder = FastEmbedEmbedder(
        onnx_batch_size=s.onnx_batch_size,
        onnx_threads=s.onnx_threads,
        providers=providers,
    )
    return _embedder


def reranker_available() -> bool:
    """Check if reranker dependencies are installed."""
    try:
        from fastembed.rerank.cross_encoder import TextCrossEncoder  # noqa: F401

        return True
    except ImportError:
        return False


_reranker_instance = None
_reranker_checked = False


def get_reranker(settings: Settings | None = None):
    """Get or create reranker (cached after first creation).

    Uses fastembed (ONNX) — no torch dependency.
    Returns None if fastembed not installed.
    """
    global _reranker_instance, _reranker_checked
    if _reranker_checked:
        return _reranker_instance

    if not reranker_available():
        _reranker_checked = True
        return None

    from memex.adapters._out.reranking.fastembed_reranker import FastEmbedReranker

    s = settings or get_settings()
    providers = detect_providers(s.onnx_provider)
    _reranker_instance = FastEmbedReranker(providers=providers)
    _reranker_checked = True
    return _reranker_instance


def daemon_available(settings: Settings | None = None) -> bool:
    """Check if memexd is running and connectable.

    Respects MEMEX_NO_DAEMON=1 kill switch.
    """
    if os.environ.get("MEMEX_NO_DAEMON"):
        return False

    from memex.daemon.server import default_socket_path

    sock_path = default_socket_path()
    if not sock_path.exists():
        return False

    # Try connecting to verify it's alive
    import socket

    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect(str(sock_path))
        s.close()
        return True
    except (ConnectionRefusedError, FileNotFoundError, OSError):
        return False


def create_service(
    with_embedder: bool = False,
    with_reranker: bool = False,
    settings: Settings | None = None,
    direct: bool = False,
) -> ExcavationService:
    """Wire up the excavation service with adapters.

    Args:
        with_embedder: Whether to include embedding capability
                      (adds ~1s startup for model loading)
        with_reranker: Whether to include reranking capability
                      (auto-disabled if deps not installed)
        settings: Optional settings. Constructs default if not provided.
        direct: Force direct DuckDB (skip daemon). Use for write-heavy
                operations (ingest, backfill) that need exclusive access.

    Returns:
        Fully wired ExcavationService

    Raises:
        EmbeddingDimensionMismatchError: If existing corpus has different dimensions
                                         than the embedder. Requires migration.
    """
    s = settings or get_settings()

    # Auto-detect: use daemon for read-heavy operations if available
    if not direct and daemon_available(s):
        from memex.adapters._out.corpus.remote import RemoteCorpusAdapter
        from memex.daemon.server import default_socket_path

        remote = RemoteCorpusAdapter(default_socket_path())
        adapters = [
            ClaudeConversationsAdapter(),
            OpenAIConversationsAdapter(),
        ]
        # Remote adapter implements all three ports
        # Embedder/reranker live on daemon side — search goes through wire
        return ExcavationService(
            remote,
            adapters,
            embedder=None,
            reranker=None,
            graph=remote,
            trails=remote,  # type: ignore[arg-type]
        )

    embedder = get_embedder(s) if with_embedder else None

    # Corpus dimensions flow from embedder
    embedding_dim = embedder.dimensions if embedder else None
    corpus = DuckDBCorpus(s.corpus_path, embedding_dim=embedding_dim)

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

    reranker = get_reranker(s) if with_reranker else None
    # DuckDBCorpus implements CorpusPort, GraphPort, and TrailPort
    return ExcavationService(corpus, adapters, embedder, reranker, graph=corpus, trails=corpus)


def create_corpus(
    embedding_dim: int | None = None,
    settings: Settings | None = None,
) -> DuckDBCorpus:
    """Direct corpus access (for SQL escape hatch commands).

    Args:
        embedding_dim: If provided, enables embedding column with this dimension.
                      If None, FTS-only mode.
        settings: Optional settings. Constructs default if not provided.
    """
    s = settings or get_settings()
    return DuckDBCorpus(s.corpus_path, embedding_dim=embedding_dim)


def initialize_corpus(corpus_path: Path) -> None:
    """Create an empty corpus at the given path.

    Used by init commands to bootstrap a new corpus without
    needing to know the adapter implementation.
    """
    corpus = DuckDBCorpus(corpus_path)
    corpus.close()


__all__ = [
    "daemon_available",
    "detect_providers",
    "create_service",
    "create_corpus",
    "get_embedder",
    "get_reranker",
    "initialize_corpus",
    "reranker_available",
    "EmbeddingDimensionMismatchError",
]
