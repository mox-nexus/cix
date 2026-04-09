"""Remote corpus adapter — talks to memexd over Unix socket.

Implements CorpusPort, GraphPort, and TrailPort by sending JSON-RPC
to the daemon. Used when memexd is running; falls back to direct
DuckDB when it's not.
"""

import json
import socket
from collections.abc import Callable, Iterable, Iterator
from pathlib import Path

from memex.daemon.protocol import (
    parse_annotated_fragments,
    parse_conversations,
    parse_edge_stats,
    parse_fragments,
    parse_schema,
    parse_scored_fragments,
    parse_stats,
    parse_trails,
    parse_traversal,
)
from memex.daemon.wire import recv_message, send_message
from memex.domain.models import (
    ConversationSummary,
    CorpusStats,
    EdgeTypeStats,
    EmbeddingConfig,
    Fragment,
    FragmentSchema,
    TrailSummary,
)


class RemoteCorpusAdapter:
    """Talks to memexd over Unix socket. Implements all three ports."""

    def __init__(self, socket_path: Path):
        self._socket_path = socket_path
        self._conn: socket.socket | None = None
        self._req_id = 0

    def _connect(self) -> socket.socket:
        if self._conn is None:
            self._conn = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            self._conn.settimeout(30.0)
            self._conn.connect(str(self._socket_path))
        return self._conn

    def _call(self, method: str, params: dict | None = None) -> any:
        """Send JSON-RPC request, return result or raise on error."""
        self._req_id += 1
        request = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": self._req_id,
                "method": method,
                "params": params or {},
            }
        )

        try:
            conn = self._connect()
            send_message(conn, request)
            raw = recv_message(conn)
        except (ConnectionError, OSError):
            # Invalidate dead socket so next call can reconnect
            self._conn = None
            raise

        response = json.loads(raw)

        if "error" in response:
            err = response["error"]
            raise RuntimeError(f"memexd error [{err['code']}]: {err['message']}")

        return response.get("result")

    # --- CorpusPort ---

    def store(self, fragments: Iterable[Fragment]) -> int:
        raise NotImplementedError("store() requires direct DuckDB access — use CLI ingest")

    def store_with_embeddings(
        self,
        fragments: Iterable[Fragment],
        embedder: Callable[[str], list[float]],
    ) -> int:
        raise NotImplementedError("store_with_embeddings() requires direct DuckDB access")

    def search(
        self,
        query: str,
        limit: int = 20,
        source_kind: str | None = None,
    ) -> list[Fragment]:
        data = self._call(
            "corpus.search",
            {
                "query": query,
                "limit": limit,
                "source_kind": source_kind,
            },
        )
        return parse_fragments(data)

    def semantic_search(
        self,
        query_embedding: list[float],
        limit: int = 20,
        source_kind: str | None = None,
        min_score: float = 0.0,
    ) -> list[tuple[Fragment, float]]:
        data = self._call(
            "corpus.semantic_search",
            {
                "query_embedding": query_embedding,
                "limit": limit,
                "source_kind": source_kind,
                "min_score": min_score,
            },
        )
        return parse_scored_fragments(data)

    def find_by_conversation(self, conversation_id: str) -> list[Fragment]:
        data = self._call(
            "corpus.find_by_conversation",
            {
                "conversation_id": conversation_id,
            },
        )
        return parse_fragments(data)

    def list_conversations(
        self,
        limit: int = 50,
        offset: int = 0,
        source_kind: str | None = None,
    ) -> list[ConversationSummary]:
        data = self._call(
            "corpus.list_conversations",
            {
                "limit": limit,
                "offset": offset,
                "source_kind": source_kind,
            },
        )
        return parse_conversations(data)

    def stats(self) -> CorpusStats:
        return parse_stats(self._call("corpus.stats"))

    def schema(self) -> FragmentSchema:
        return parse_schema(self._call("corpus.schema"))

    def count_without_embeddings(self) -> int:
        return self._call("corpus.count_without_embeddings")

    def has_semantic_search(self) -> bool:
        return self._call("corpus.has_semantic_search")

    def has_keyword_search(self) -> bool:
        return self._call("corpus.has_keyword_search")

    def rebuild_search_index(self) -> None:
        self._call("corpus.rebuild_search_index")

    def embedding_dimensions(self) -> int | None:
        return self._call("corpus.embedding_dimensions")

    def backfill_embeddings(
        self,
        embedder_stream: Callable[[Iterator[str]], Iterator[list[float]]],
        batch_size: int = 100,
        on_progress: Callable[[int, int], None] | None = None,
    ) -> int:
        raise NotImplementedError("backfill requires direct DuckDB + ONNX access — use CLI")

    def record_embedding_config(self, config: EmbeddingConfig) -> None:
        pass  # Embedding config is managed by the daemon's direct corpus

    def close(self) -> None:
        if self._conn:
            try:
                self._conn.close()
            except OSError:
                pass
            self._conn = None

    # --- GraphPort ---

    def find_similar(
        self,
        fragment_id: str,
        limit: int = 10,
    ) -> list[tuple[Fragment, float]]:
        data = self._call(
            "graph.find_similar",
            {
                "fragment_id": fragment_id,
                "limit": limit,
            },
        )
        return parse_scored_fragments(data)

    def build_follows_edges(self) -> int:
        return self._call("graph.build_follows_edges")

    def build_similar_edges(
        self,
        threshold: float = 0.8,
        k: int = 5,
        on_progress: Callable[[int, int], None] | None = None,
    ) -> int:
        raise NotImplementedError("build_similar_edges requires direct access — use CLI")

    def edge_stats(self) -> dict[str, EdgeTypeStats]:
        return parse_edge_stats(self._call("graph.edge_stats"))

    def traverse(
        self,
        fragment_id: str,
        max_hops: int = 2,
        edge_type: str | None = None,
        limit: int = 20,
    ) -> list[tuple[Fragment, int, str]]:
        data = self._call(
            "graph.traverse",
            {
                "fragment_id": fragment_id,
                "max_hops": max_hops,
                "edge_type": edge_type,
                "limit": limit,
            },
        )
        return parse_traversal(data)

    # --- TrailPort ---

    def create_trail(self, name: str, description: str = "") -> str:
        return self._call("trails.create_trail", {"name": name, "description": description})

    def add_to_trail(self, trail_name: str, fragment_id: str, note: str = "") -> int:
        return self._call(
            "trails.add_to_trail",
            {
                "trail_name": trail_name,
                "fragment_id": fragment_id,
                "note": note,
            },
        )

    def get_trail(self, trail_name: str) -> list[tuple[Fragment, str]]:
        data = self._call("trails.get_trail", {"trail_name": trail_name})
        return parse_annotated_fragments(data)

    def list_trails(self) -> list[TrailSummary]:
        return parse_trails(self._call("trails.list_trails"))

    def delete_trail(self, trail_name: str) -> bool:
        return self._call("trails.delete_trail", {"trail_name": trail_name})

    def search_trails(self, query: str) -> list[TrailSummary]:
        return parse_trails(self._call("trails.search_trails", {"query": query}))

    def trails_for_fragment(self, fragment_id: str) -> list[TrailSummary]:
        return parse_trails(self._call("trails.trails_for_fragment", {"fragment_id": fragment_id}))
