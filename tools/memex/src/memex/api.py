"""Public API for memex.

    from memex.api import Memex

    with Memex() as m:
        results = m.search("auth decisions")
        for fragment, score in results:
            print(fragment.content)

This is the stable entry point for agents and libraries.
Internal structure may change; this facade won't.
"""

from pathlib import Path

from memex.config.settings import Settings
from memex.domain.models import (
    ConversationSummary,
    CorpusStats,
    Fragment,
    IngestResult,
    TrailSummary,
)


class Memex:
    """Extended memory — search and store collaborative intelligence artifacts.

    Args:
        path: Corpus path. If None, uses settings resolution (local .memex/ or global).
        settings: Explicit settings. If None, constructs from env/config.
        embed: Enable embedding for semantic search (default True).
        rerank: Enable cross-encoder reranking (default True, auto-disabled if deps missing).
        direct: Force direct DuckDB access (skip daemon auto-detect).
    """

    def __init__(
        self,
        path: Path | str | None = None,
        settings: Settings | None = None,
        embed: bool = True,
        rerank: bool = True,
        direct: bool = False,
    ):
        if path is not None:
            # Override corpus path in settings
            s = settings or Settings()
            s = s.model_copy(update={"corpus_path": Path(path)})
        else:
            s = settings

        from memex.composition import create_service

        self._service = create_service(
            with_embedder=embed,
            with_reranker=rerank,
            settings=s,
            direct=direct,
        )

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def search(
        self,
        query: str,
        limit: int = 20,
        source_kind: str | None = None,
        semantic_weight: float = 0.6,
        rerank: bool = True,
    ) -> list[tuple[Fragment, float]]:
        """Search memory. Uses hybrid search (keyword + semantic + reranking) by default.

        Falls back gracefully: no embedder -> keyword only, no reranker -> RRF only.

        Returns:
            List of (Fragment, score) tuples, best matches first.
        """
        return self._service.hybrid_search(
            query,
            limit=limit,
            source_kind=source_kind,
            semantic_weight=semantic_weight,
            use_reranker=rerank,
        )

    def ingest(self, path: Path | str) -> IngestResult:
        """Ingest a file into the corpus.

        Supports Claude exports (.json, .zip), OpenAI exports (.zip), and
        any format with a registered source adapter.

        Returns:
            IngestResult(parsed, stored) — fragments parsed and newly stored.
        """
        return self._service.ingest(Path(path))

    def stats(self) -> CorpusStats:
        """Get corpus statistics."""
        return self._service.corpus.stats()

    def find_conversation(self, conversation_id: str) -> list[Fragment]:
        """Get all fragments in a conversation (exact or prefix match)."""
        return self._service.corpus.find_by_conversation(conversation_id)

    def list_conversations(
        self,
        limit: int = 50,
        offset: int = 0,
        source_kind: str | None = None,
    ) -> list[ConversationSummary]:
        """List conversations, most recent first."""
        return self._service.corpus.list_conversations(limit, offset, source_kind)

    def find_similar(self, fragment_id: str, limit: int = 10) -> list[tuple[Fragment, float]]:
        """Find similar fragments via graph edges."""
        return self._service.graph.find_similar(fragment_id, limit)

    def create_trail(self, name: str, description: str = "") -> str:
        """Create a named trail. Returns trail ID."""
        return self._service.trails.create_trail(name, description)

    def follow_trail(self, trail_name: str) -> list[tuple[Fragment, str]]:
        """Walk a trail — returns entries in order as (Fragment, note) tuples."""
        return self._service.trails.get_trail(trail_name)

    def list_trails(self) -> list[TrailSummary]:
        """List all trails."""
        return self._service.trails.list_trails()

    def delete_trail(self, trail_name: str) -> bool:
        """Delete a trail."""
        return self._service.trails.delete_trail(trail_name)

    def close(self) -> None:
        """Release resources."""
        self._service.close()
