"""JSON-RPC wire protocol for memexd.

Maps method names to port methods. All domain types serialize
via Pydantic (model_dump / model_validate). No raw SQL on wire.
"""

import json
import threading
from collections.abc import Callable
from typing import Any

from memex.domain.models import (
    ConversationSummary,
    CorpusStats,
    EdgeTypeStats,
    Fragment,
    FragmentSchema,
    TrailSummary,
)

# JSON-RPC 2.0 error codes
PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603

# Server-side safety limits
MAX_LIMIT = 500


def _clamp_limit(params: dict, default: int = 20) -> dict:
    """Enforce server-side limit cap."""
    if "limit" in params:
        params["limit"] = max(1, min(int(params["limit"]), MAX_LIMIT))
    if "offset" in params:
        params["offset"] = max(0, int(params["offset"]))
    return params


def _fragment_to_dict(frag: Fragment) -> dict:
    return frag.model_dump(mode="json")


def _fragment_from_dict(d: dict) -> Fragment:
    return Fragment.model_validate(d)


def _scored_fragments(results: list[tuple[Fragment, float]]) -> list[dict]:
    return [{"fragment": _fragment_to_dict(f), "score": s} for f, s in results]


def _annotated_fragments(results: list[tuple[Fragment, str]]) -> list[dict]:
    return [{"fragment": _fragment_to_dict(f), "note": n} for f, n in results]


class Dispatcher:
    """Routes JSON-RPC method calls to port methods.

    Constructed with the three ports (corpus, graph, trails).
    Each method handler validates params and serializes results.
    """

    def __init__(self, corpus, graph, trails):
        self._corpus = corpus
        self._graph = graph
        self._trails = trails
        self._lock = threading.Lock()
        self._methods: dict[str, Callable] = {
            # CorpusPort
            "corpus.search": self._corpus_search,
            "corpus.semantic_search": self._corpus_semantic_search,
            "corpus.find_by_conversation": self._corpus_find_by_conversation,
            "corpus.list_conversations": self._corpus_list_conversations,
            "corpus.stats": self._corpus_stats,
            "corpus.schema": self._corpus_schema,
            "corpus.count_without_embeddings": self._corpus_count_without_embeddings,
            "corpus.has_semantic_search": self._corpus_has_semantic_search,
            "corpus.has_keyword_search": self._corpus_has_keyword_search,
            "corpus.embedding_dimensions": self._corpus_embedding_dimensions,
            "corpus.rebuild_search_index": self._corpus_rebuild_search_index,
            # GraphPort
            "graph.find_similar": self._graph_find_similar,
            "graph.build_follows_edges": self._graph_build_follows_edges,
            "graph.edge_stats": self._graph_edge_stats,
            # TrailPort
            "trails.create_trail": self._trails_create_trail,
            "trails.add_to_trail": self._trails_add_to_trail,
            "trails.get_trail": self._trails_get_trail,
            "trails.list_trails": self._trails_list_trails,
            "trails.delete_trail": self._trails_delete_trail,
        }

    def dispatch(self, raw: str) -> str:
        """Process a JSON-RPC request, return JSON-RPC response."""
        try:
            request = json.loads(raw)
        except json.JSONDecodeError as e:
            return _error_response(None, PARSE_ERROR, f"Parse error: {e}")

        req_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        if not method or not isinstance(method, str):
            return _error_response(req_id, INVALID_REQUEST, "Missing method")

        handler = self._methods.get(method)
        if not handler:
            return _error_response(req_id, METHOD_NOT_FOUND, f"Unknown method: {method}")

        try:
            with self._lock:
                result = handler(params)
            return _success_response(req_id, result)
        except TypeError as e:
            return _error_response(req_id, INVALID_PARAMS, str(e))
        except Exception as e:
            return _error_response(req_id, INTERNAL_ERROR, str(e))

    # --- CorpusPort handlers ---

    def _corpus_search(self, p: dict) -> list[dict]:
        p = _clamp_limit(p)
        results = self._corpus.search(
            p["query"],
            p.get("limit", 20),
            p.get("source_kind"),
        )
        return [_fragment_to_dict(f) for f in results]

    def _corpus_semantic_search(self, p: dict) -> list[dict]:
        p = _clamp_limit(p)
        results = self._corpus.semantic_search(
            p["query_embedding"],
            p.get("limit", 20),
            p.get("source_kind"),
            p.get("min_score", 0.0),
        )
        return _scored_fragments(results)

    def _corpus_find_by_conversation(self, p: dict) -> list[dict]:
        results = self._corpus.find_by_conversation(p["conversation_id"])
        return [_fragment_to_dict(f) for f in results]

    def _corpus_list_conversations(self, p: dict) -> list[dict]:
        p = _clamp_limit(p)
        results = self._corpus.list_conversations(
            p.get("limit", 50),
            p.get("offset", 0),
            p.get("source_kind"),
        )
        return [c.model_dump(mode="json") for c in results]

    def _corpus_stats(self, _p: dict) -> dict:
        return self._corpus.stats().model_dump(mode="json")

    def _corpus_schema(self, _p: dict) -> dict:
        return self._corpus.schema().model_dump(mode="json")

    def _corpus_count_without_embeddings(self, _p: dict) -> int:
        return self._corpus.count_without_embeddings()

    def _corpus_has_semantic_search(self, _p: dict) -> bool:
        return self._corpus.has_semantic_search()

    def _corpus_has_keyword_search(self, _p: dict) -> bool:
        return self._corpus.has_keyword_search()

    def _corpus_embedding_dimensions(self, _p: dict) -> int | None:
        return self._corpus.embedding_dimensions()

    def _corpus_rebuild_search_index(self, _p: dict) -> None:
        self._corpus.rebuild_search_index()

    # --- GraphPort handlers ---

    def _graph_find_similar(self, p: dict) -> list[dict]:
        p = _clamp_limit(p)
        results = self._graph.find_similar(p["fragment_id"], p.get("limit", 10))
        return _scored_fragments(results)

    def _graph_build_follows_edges(self, _p: dict) -> int:
        return self._graph.build_follows_edges()

    def _graph_edge_stats(self, _p: dict) -> dict:
        stats = self._graph.edge_stats()
        return {k: v.model_dump(mode="json") for k, v in stats.items()}

    # --- TrailPort handlers ---

    def _trails_create_trail(self, p: dict) -> str:
        return self._trails.create_trail(p["name"], p.get("description", ""))

    def _trails_add_to_trail(self, p: dict) -> int:
        return self._trails.add_to_trail(
            p["trail_name"],
            p["fragment_id"],
            p.get("note", ""),
        )

    def _trails_get_trail(self, p: dict) -> list[dict]:
        results = self._trails.get_trail(p["trail_name"])
        return _annotated_fragments(results)

    def _trails_list_trails(self, _p: dict) -> list[dict]:
        results = self._trails.list_trails()
        return [t.model_dump(mode="json") for t in results]

    def _trails_delete_trail(self, p: dict) -> bool:
        return self._trails.delete_trail(p["trail_name"])

    def _trails_search_trails(self, p: dict) -> list[dict]:
        results = self._trails.search_trails(p["query"])
        return [t.model_dump(mode="json") for t in results]

    def _trails_trails_for_fragment(self, p: dict) -> list[dict]:
        results = self._trails.trails_for_fragment(p["fragment_id"])
        return [t.model_dump(mode="json") for t in results]


# --- JSON-RPC response helpers ---


def _success_response(req_id: Any, result: Any) -> str:
    return json.dumps({"jsonrpc": "2.0", "id": req_id, "result": result})


def _error_response(req_id: Any, code: int, message: str) -> str:
    return json.dumps(
        {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": code, "message": message},
        }
    )


# --- Client-side deserialization helpers ---


def parse_fragments(data: list[dict]) -> list[Fragment]:
    return [_fragment_from_dict(d) for d in data]


def parse_scored_fragments(data: list[dict]) -> list[tuple[Fragment, float]]:
    return [(_fragment_from_dict(d["fragment"]), d["score"]) for d in data]


def parse_annotated_fragments(data: list[dict]) -> list[tuple[Fragment, str]]:
    return [(_fragment_from_dict(d["fragment"]), d["note"]) for d in data]


def parse_stats(data: dict) -> CorpusStats:
    return CorpusStats.model_validate(data)


def parse_schema(data: dict) -> FragmentSchema:
    return FragmentSchema.model_validate(data)


def parse_conversations(data: list[dict]) -> list[ConversationSummary]:
    return [ConversationSummary.model_validate(d) for d in data]


def parse_edge_stats(data: dict) -> dict[str, EdgeTypeStats]:
    return {k: EdgeTypeStats.model_validate(v) for k, v in data.items()}


def parse_trails(data: list[dict]) -> list[TrailSummary]:
    return [TrailSummary.model_validate(d) for d in data]
