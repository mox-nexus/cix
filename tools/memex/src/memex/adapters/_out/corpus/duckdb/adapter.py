"""DuckDB corpus adapter — facade over focused adapter classes.

DuckDBCorpus is the public API. Internally delegates to:
- DuckDBConnection: shared state, schema, extensions
- DuckDBCorpusAdapter: CorpusPort (storage, search, backfill)
- DuckDBGraphAdapter: GraphPort (edges, similar)
- DuckDBTrailAdapter: TrailPort (curated paths)

All share one DuckDB connection. DuckDBCorpus owns the lifecycle.
"""

from collections.abc import Callable, Iterable, Iterator
from pathlib import Path
from typing import TYPE_CHECKING

from memex.domain.models import (
    ConversationSummary,
    CorpusStats,
    EdgeTypeStats,
    EmbeddingConfig,
    Fragment,
    FragmentSchema,
    TrailSummary,
)

from .connection import DuckDBConnection
from .corpus_adapter import DuckDBCorpusAdapter
from .graph_adapter import DuckDBGraphAdapter
from .trail_adapter import DuckDBTrailAdapter

if TYPE_CHECKING:
    from memex.domain.ports._out.graph import ProgressCallback


class DuckDBCorpus:
    """Facade over focused DuckDB adapters.

    Implements CorpusPort, GraphPort, and TrailPort by delegation.
    Backward-compatible — all existing callers work unchanged.
    """

    def __init__(self, path: Path, embedding_dim: int | None = None):
        self._connection = DuckDBConnection(path, embedding_dim)
        self._corpus = DuckDBCorpusAdapter(self._connection)
        self._graph = DuckDBGraphAdapter(self._connection)
        self._trails = DuckDBTrailAdapter(self._connection)

    # --- Expose internals for composition root ---

    @property
    def path(self) -> Path:
        return self._connection.path

    @property
    def con(self):
        """Raw DuckDB connection (for SQL escape hatch)."""
        return self._connection.con

    @property
    def connection(self) -> DuckDBConnection:
        """Access the shared connection."""
        return self._connection

    @property
    def corpus_adapter(self) -> DuckDBCorpusAdapter:
        return self._corpus

    @property
    def graph_adapter(self) -> DuckDBGraphAdapter:
        return self._graph

    @property
    def trail_adapter(self) -> DuckDBTrailAdapter:
        return self._trails

    # === CorpusPort delegation ===

    def store(self, fragments: Iterable[Fragment]) -> int:
        return self._corpus.store(fragments)

    def store_with_embeddings(
        self,
        fragments: Iterable[Fragment],
        embedder: Callable[[str], list[float]],
    ) -> int:
        return self._corpus.store_with_embeddings(fragments, embedder)

    def search(
        self,
        query: str,
        limit: int = 20,
        source_kind: str | None = None,
    ) -> list[Fragment]:
        return self._corpus.search(query, limit, source_kind)

    def has_keyword_search(self) -> bool:
        return self._corpus.has_keyword_search()

    def rebuild_search_index(self) -> None:
        self._corpus.rebuild_search_index()

    def find_by_conversation(self, conversation_id: str) -> list[Fragment]:
        return self._corpus.find_by_conversation(conversation_id)

    def list_conversations(
        self,
        limit: int = 50,
        offset: int = 0,
        source_kind: str | None = None,
    ) -> list[ConversationSummary]:
        return self._corpus.list_conversations(limit, offset, source_kind)

    def semantic_search(
        self,
        query_embedding: list[float],
        limit: int = 20,
        source_kind: str | None = None,
        min_score: float = 0.0,
    ) -> list[tuple[Fragment, float]]:
        return self._corpus.semantic_search(query_embedding, limit, source_kind, min_score)

    def has_semantic_search(self) -> bool:
        return self._corpus.has_semantic_search()

    def count_without_embeddings(self) -> int:
        return self._corpus.count_without_embeddings()

    def backfill_embeddings(
        self,
        embedder_stream: Callable[[Iterator[str]], Iterator[list[float]]],
        batch_size: int = 100,
        on_progress: Callable[[int, int], None] | None = None,
    ) -> int:
        return self._corpus.backfill_embeddings(embedder_stream, batch_size, on_progress)

    def stats(self) -> CorpusStats:
        return self._corpus.stats()

    def schema(self) -> FragmentSchema:
        return self._corpus.schema()

    def embedding_dimensions(self) -> int | None:
        return self._connection.embedding_dimensions()

    def record_embedding_config(self, config: EmbeddingConfig) -> None:
        self._connection.record_embedding_config(config)

    # === GraphPort delegation ===

    def add_edge(
        self,
        source_id: str,
        target_id: str,
        edge_type: str,
        weight: float = 1.0,
    ) -> None:
        self._graph.add_edge(source_id, target_id, edge_type, weight)

    def add_edges_batch(self, edges: list[tuple[str, str, str, float]]) -> int:
        return self._graph.add_edges_batch(edges)

    def get_edges(
        self,
        fragment_id: str,
        edge_type: str | None = None,
        direction: str = "outgoing",
    ) -> list[dict]:
        return self._graph.get_edges(fragment_id, edge_type, direction)

    def find_similar(
        self,
        fragment_id: str,
        limit: int = 10,
    ) -> list[tuple[Fragment, float]]:
        return self._graph.find_similar(fragment_id, limit)

    def build_follows_edges(self) -> int:
        return self._graph.build_follows_edges()

    def build_similar_edges(
        self,
        threshold: float = 0.8,
        k: int = 5,
        on_progress: "ProgressCallback" = None,
    ) -> int:
        return self._graph.build_similar_edges(threshold, k, on_progress)

    def edge_stats(self) -> dict[str, EdgeTypeStats]:
        return self._graph.edge_stats()

    def traverse(
        self,
        fragment_id: str,
        max_hops: int = 2,
        edge_type: str | None = None,
        limit: int = 20,
    ) -> list[tuple[Fragment, int, str]]:
        return self._graph.traverse(fragment_id, max_hops, edge_type, limit)

    # === TrailPort delegation ===

    def create_trail(self, name: str, description: str = "") -> str:
        return self._trails.create_trail(name, description)

    def add_to_trail(self, trail_name: str, fragment_id: str, note: str = "") -> int:
        return self._trails.add_to_trail(trail_name, fragment_id, note)

    def get_trail(self, trail_name: str) -> list[tuple[Fragment, str]]:
        return self._trails.get_trail(trail_name)

    def list_trails(self) -> list[TrailSummary]:
        return self._trails.list_trails()

    def delete_trail(self, trail_name: str) -> bool:
        return self._trails.delete_trail(trail_name)

    def search_trails(self, query: str) -> list[TrailSummary]:
        return self._trails.search_trails(query)

    def trails_for_fragment(self, fragment_id: str) -> list[TrailSummary]:
        return self._trails.trails_for_fragment(fragment_id)

    # === Meta / lifecycle ===

    def get_meta(self, key: str) -> str | None:
        return self._connection.get_meta(key)

    def set_meta(self, key: str, value: str) -> None:
        self._connection.set_meta(key, value)

    def close(self) -> None:
        self._connection.close()

    def query_sql(self, sql: str):
        return self._connection.query_sql(sql)
