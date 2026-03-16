"""DuckDB corpus adapter — implements CorpusPort.

Storage, search (BM25 + semantic), backfill embeddings.
"""

import json
import logging
from collections.abc import Callable, Iterable, Iterator
from itertools import batched, chain, count
from typing import TYPE_CHECKING

import duckdb

from memex.domain.models import (
    ConversationSummary,
    CorpusStats,
    EmbeddingConfig,
    FieldInfo,
    Fragment,
    FragmentSchema,
)
from memex.domain.streaming import tap, tap_every

from .connection import DuckDBConnection, row_to_fragment

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    pass


class DuckDBCorpusAdapter:
    """CorpusPort implementation backed by DuckDB.

    Receives a DuckDBConnection — does not own the connection lifecycle.
    """

    def __init__(self, conn: DuckDBConnection):
        self._conn = conn

    @property
    def con(self):
        return self._conn.con

    # --- Store ---

    def store(self, fragments: Iterable[Fragment]) -> int:
        """Store fragments in batches. Returns count of new fragments."""
        batch_size = 1000
        count_before = self._fragment_count()

        batch: list[tuple] = []
        for frag in fragments:
            batch.append(
                (
                    frag.id,
                    frag.conversation_id,
                    frag.role,
                    frag.content,
                    frag.timestamp,
                    frag.provenance.source_kind,
                    frag.provenance.source_id,
                    json.dumps(frag.metadata) if frag.metadata else None,
                )
            )
            if len(batch) >= batch_size:
                self._insert_batch(batch)
                batch = []

        if batch:
            self._insert_batch(batch)

        return self._fragment_count() - count_before

    def _insert_batch(self, batch: list[tuple]) -> None:
        self.con.executemany(
            """
            INSERT INTO fragments
                (id, conversation_id, role, content, timestamp, source_kind, source_id, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?::JSON)
            ON CONFLICT (id) DO NOTHING
            """,
            batch,
        )

    def _fragment_count(self) -> int:
        result = self.con.execute("SELECT COUNT(*) FROM fragments").fetchone()
        return result[0] if result else 0

    def store_with_embeddings(
        self,
        fragments: Iterable[Fragment],
        embedder: Callable[[str], list[float]],
    ) -> int:
        """Store fragments with embeddings in batches."""
        if not self._conn.embedding_dim:
            msg = "Corpus created without embedding support. Pass embedding_dim."
            raise ValueError(msg)

        batch_size = 100
        count_before = self._fragment_count()

        batch: list[tuple] = []
        for frag in fragments:
            embedding = embedder(frag.content)
            batch.append(
                (
                    frag.id,
                    frag.conversation_id,
                    frag.role,
                    frag.content,
                    frag.timestamp,
                    frag.provenance.source_kind,
                    frag.provenance.source_id,
                    json.dumps(frag.metadata) if frag.metadata else None,
                    embedding,
                )
            )
            if len(batch) >= batch_size:
                self._insert_embedding_batch(batch)
                batch = []

        if batch:
            self._insert_embedding_batch(batch)

        return self._fragment_count() - count_before

    def _insert_embedding_batch(self, batch: list[tuple]) -> None:
        self.con.executemany(
            f"""
            INSERT INTO fragments (
                id, conversation_id, role, content,
                timestamp, source_kind, source_id, metadata, embedding
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?::JSON, ?::FLOAT[{self._conn.embedding_dim}])
            ON CONFLICT (id) DO NOTHING
            """,
            batch,
        )

    # --- Search ---

    def search(
        self,
        query: str,
        limit: int = 20,
        source_kind: str | None = None,
    ) -> list[Fragment]:
        """Search fragments using BM25 (with ILIKE fallback)."""
        if not query.strip():
            return []

        if self._conn.fts_available:
            self._conn.ensure_fts_index()
            return self._search_bm25(query, limit, source_kind)
        else:
            return self._search_ilike(query, limit, source_kind)

    def _search_bm25(
        self,
        query: str,
        limit: int,
        source_kind: str | None,
    ) -> list[Fragment]:
        try:
            source_filter = ""
            params = [query, limit]
            if source_kind:
                source_filter = "AND f.source_kind = ?"
                params = [query, source_kind, limit]

            rows = self.con.execute(
                f"""
                SELECT f.id, f.conversation_id, f.role, f.content,
                       f.timestamp, f.source_kind, f.source_id, f.metadata, fts.score
                FROM fts_main_fragments.match_bm25(?, fields := 'content') AS fts
                JOIN fragments f ON f.id = fts.id
                WHERE 1=1 {source_filter}
                ORDER BY fts.score DESC
                LIMIT ?
                """,
                params,
            ).fetchall()
            return [row_to_fragment(row[:8]) for row in rows]
        except duckdb.Error:
            return self._search_ilike(query, limit, source_kind)

    def _search_ilike(
        self,
        query: str,
        limit: int,
        source_kind: str | None,
    ) -> list[Fragment]:
        words = query.split()
        if not words:
            return []

        conditions = ["content ILIKE ?" for _ in words]
        params: list = [f"%{self._escape_ilike(word)}%" for word in words]

        if source_kind:
            conditions.append("source_kind = ?")
            params.append(source_kind)

        where_clause = " AND ".join(conditions)
        params.append(limit)

        rows = self.con.execute(
            f"""
            SELECT id, conversation_id, role, content, timestamp, source_kind, source_id, metadata
            FROM fragments
            WHERE {where_clause}
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            params,
        ).fetchall()
        return [row_to_fragment(row) for row in rows]

    @staticmethod
    def _escape_ilike(s: str) -> str:
        return s.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")

    def has_keyword_search(self) -> bool:
        return self._conn.fts_available

    def rebuild_search_index(self) -> None:
        """Rebuild FTS index after data changes."""
        if not self._conn.fts_available:
            return
        try:
            self.con.execute("PRAGMA drop_fts_index('fragments')")
        except duckdb.Error:
            pass
        self._conn.ensure_fts_index()

    # --- Conversation browsing ---

    def find_by_conversation(self, conversation_id: str) -> list[Fragment]:
        """Get all fragments in a conversation (supports prefix matching)."""
        rows = self.con.execute(
            """
            SELECT id, conversation_id, role, content, timestamp, source_kind, source_id, metadata
            FROM fragments
            WHERE conversation_id = ?
            ORDER BY timestamp
            """,
            [conversation_id],
        ).fetchall()

        if rows:
            return [row_to_fragment(row) for row in rows]

        rows = self.con.execute(
            """
            SELECT id, conversation_id, role, content, timestamp, source_kind, source_id, metadata
            FROM fragments
            WHERE conversation_id LIKE ? || '%'
            ORDER BY timestamp
            """,
            [conversation_id],
        ).fetchall()
        return [row_to_fragment(row) for row in rows]

    def list_conversations(
        self,
        limit: int = 50,
        offset: int = 0,
        source_kind: str | None = None,
    ) -> list[ConversationSummary]:
        source_filter = "AND source_kind = ?" if source_kind else ""
        params = [source_kind] if source_kind else []

        rows = self.con.execute(
            f"""
            SELECT
                conversation_id,
                COUNT(*) as message_count,
                MIN(timestamp) as first_ts,
                MAX(timestamp) as last_ts,
                source_kind,
                MIN(CASE WHEN role = 'user' THEN content END) as preview
            FROM fragments
            WHERE conversation_id IS NOT NULL {source_filter}
            GROUP BY conversation_id, source_kind
            ORDER BY MAX(timestamp) DESC
            LIMIT ? OFFSET ?
            """,
            [*params, limit, offset],
        ).fetchall()

        return [
            ConversationSummary(
                conversation_id=row[0],
                message_count=row[1],
                first_timestamp=row[2],
                last_timestamp=row[3],
                source_kind=row[4],
                preview=(row[5][:120] + "...") if row[5] and len(row[5]) > 120 else row[5],
            )
            for row in rows
        ]

    # --- Semantic search ---

    def semantic_search(
        self,
        query_embedding: list[float],
        limit: int = 20,
        source_kind: str | None = None,
        min_score: float = 0.0,
    ) -> list[tuple[Fragment, float]]:
        """Search by semantic similarity using HNSW index."""
        if not self._conn.vss_available or not self._conn.embedding_dim:
            return []

        max_distance = 1.0 - min_score
        dim = self._conn.embedding_dim

        if source_kind:
            candidate_limit = limit * 5
            rows = self.con.execute(
                f"""
                WITH candidates AS (
                    SELECT
                        id, conversation_id, role, content, timestamp,
                        source_kind, source_id, metadata,
                        array_cosine_distance(
                            embedding, ?::FLOAT[{dim}]
                        ) as distance
                    FROM fragments
                    ORDER BY distance ASC
                    LIMIT ?
                )
                SELECT id, conversation_id, role, content, timestamp,
                       source_kind, source_id, metadata, distance
                FROM candidates
                WHERE source_kind = ? AND distance <= ?
                ORDER BY distance ASC
                LIMIT ?
                """,
                [query_embedding, candidate_limit, source_kind, max_distance, limit],
            ).fetchall()
        else:
            rows = self.con.execute(
                f"""
                SELECT
                    id, conversation_id, role, content, timestamp,
                    source_kind, source_id, metadata,
                    array_cosine_distance(embedding, ?::FLOAT[{dim}]) as distance
                FROM fragments
                ORDER BY distance ASC
                LIMIT ?
                """,
                [query_embedding, limit],
            ).fetchall()

        results = []
        for row in rows:
            distance = row[8]
            similarity = 1.0 - distance
            if similarity >= min_score:
                fragment = row_to_fragment(row[:8])
                results.append((fragment, similarity))
        return results

    def has_semantic_search(self) -> bool:
        return self._conn.vss_available and self._conn.embedding_dim is not None

    # --- Backfill ---

    def count_without_embeddings(self) -> int:
        result = self.con.execute(
            "SELECT COUNT(*) FROM fragments WHERE embedding IS NULL"
        ).fetchone()
        return result[0] if result else 0

    def _unembedded_ids_by_length(self) -> list[str]:
        return [
            row[0]
            for row in self.con.execute(
                "SELECT id FROM fragments WHERE embedding IS NULL ORDER BY LENGTH(content)"
            ).fetchall()
        ]

    def _fetch_content_batch(self, ids: tuple[str, ...]) -> list[tuple[str, str]]:
        placeholders = ",".join("?" * len(ids))
        return self.con.execute(
            f"SELECT id, content FROM fragments WHERE id IN ({placeholders})",
            list(ids),
        ).fetchall()

    def _write_embedding(self, frag_id: str, embedding: list[float]) -> None:
        self.con.execute(
            f"""
            UPDATE fragments
            SET embedding = ?::FLOAT[{self._conn.embedding_dim}]
            WHERE id = ?
            """,
            (embedding, frag_id),
        )

    def _write_one(self, pair: tuple[str, list[float]]) -> tuple[str, list[float]]:
        frag_id, embedding = pair
        self._write_embedding(frag_id, embedding)
        return pair

    def _embed_rows(
        self,
        rows: Iterator[tuple[str, str]],
        embedder_stream: Callable[[Iterator[str]], Iterator[list[float]]],
        batch_size: int,
    ) -> Iterator[tuple[str, list[float]]]:
        for batch in batched(rows, batch_size):
            ids, contents = zip(*batch)
            yield from zip(ids, embedder_stream(iter(contents)))

    def backfill_embeddings(
        self,
        embedder_stream: Callable[[Iterator[str]], Iterator[list[float]]],
        batch_size: int = 100,
        on_progress: Callable[[int, int], None] | None = None,
    ) -> int:
        """Backfill embeddings — streaming FP pipeline, no accumulation."""
        if not self._conn.embedding_dim:
            msg = "Corpus created without embedding support. Pass embedding_dim."
            raise ValueError(msg)

        total = self.count_without_embeddings()
        if total == 0:
            return 0

        self._conn.drop_hnsw_index()

        try:
            unembedded_ids = self._unembedded_ids_by_length()
            rows = chain.from_iterable(
                self._fetch_content_batch(id_batch)
                for id_batch in batched(unembedded_ids, batch_size)
            )

            embedded = self._embed_rows(rows, embedder_stream, batch_size)
            pipeline: Iterator = map(self._write_one, embedded)
            pipeline = tap_every(pipeline, 1000, lambda _: self._conn.checkpoint())

            if on_progress:
                c = count(1)
                pipeline = tap(pipeline, lambda _: on_progress(next(c), total))

            return sum(1 for _ in pipeline)
        finally:
            self._conn.checkpoint()
            self._conn.create_hnsw_index()

    # --- Stats ---

    def stats(self) -> CorpusStats:
        result = self.con.execute("""
            SELECT
                COUNT(*) as total_fragments,
                COUNT(DISTINCT conversation_id) as conversations,
                MIN(timestamp) as earliest,
                MAX(timestamp) as latest,
                COUNT(DISTINCT source_kind) as sources
            FROM fragments
        """).fetchone()

        return CorpusStats(
            total_fragments=result[0],
            conversations=result[1],
            earliest=result[2],
            latest=result[3],
            sources=result[4],
        )

    def schema(self) -> FragmentSchema:
        columns = self.con.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'fragments'
            ORDER BY ordinal_position
        """).fetchall()

        return FragmentSchema(
            fragments=[FieldInfo(name=c[0], type=c[1], nullable=c[2] == "YES") for c in columns]
        )

    # --- Delegated to connection ---

    def embedding_dimensions(self) -> int | None:
        return self._conn.embedding_dimensions()

    def record_embedding_config(self, config: EmbeddingConfig) -> None:
        self._conn.record_embedding_config(config)
