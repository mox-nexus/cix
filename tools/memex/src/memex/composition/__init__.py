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

from memex.adapters._out.corpus import DuckDBCorpus
from memex.adapters._out.sources import ClaudeConversationsAdapter, OpenAIConversationsAdapter
from memex.config.settings import settings
from memex.domain.ports._out.embedding import EmbeddingPort
from memex.domain.services import ExcavationService


class EmbeddingDimensionMismatchError(Exception):
    """Raised when corpus dimensions don't match embedder dimensions."""

    pass


@lru_cache(maxsize=1)
def get_embedder() -> EmbeddingPort:
    """Get or create embedder (cached, lazy load).

    Selection driven by settings.embedding_model:
    - "minilm": MiniLM-L6-v2 (384-dim) via sentence-transformers
    - "nomic": Nomic v1.5 (768-dim) via GPT4All local inference
    """
    if settings.embedding_model == "nomic":
        from memex.adapters._out.embedding.nomic import NomicEmbedder

        return NomicEmbedder()

    from memex.adapters._out.embedding import LocalEmbedder

    return LocalEmbedder()


def reranker_available() -> bool:
    """Check if reranker dependencies are installed."""
    try:
        from sentence_transformers import CrossEncoder  # noqa: F401

        return True
    except ImportError:
        return False


@lru_cache(maxsize=1)
def get_reranker():
    """Get or create reranker (cached, lazy load).

    Returns None if reranker dependencies not installed.
    Install with: uv add sentence-transformers
    """
    if not reranker_available():
        return None

    from memex.adapters._out.reranking.cross_encoder import CrossEncoderReranker

    return CrossEncoderReranker()


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
    corpus = DuckDBCorpus(settings.corpus_path, embedding_dim=embedding_dim)

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
    return DuckDBCorpus(settings.corpus_path, embedding_dim=embedding_dim)


__all__ = [
    "create_service",
    "create_corpus",
    "get_embedder",
    "get_reranker",
    "reranker_available",
    "EmbeddingDimensionMismatchError",
]
