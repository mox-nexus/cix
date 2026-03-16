"""DuckDB graph adapter — implements GraphPort.

Fragment relationships: FOLLOWS edges, SIMILAR_TO edges, edge queries.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from memex.domain.models import EdgeTypeStats, Fragment

from .connection import DuckDBConnection, row_to_fragment

if TYPE_CHECKING:
    from memex.domain.ports._out.graph import ProgressCallback


class DuckDBGraphAdapter:
    """GraphPort implementation backed by DuckDB.

    Receives a DuckDBConnection — does not own the connection lifecycle.
    """

    def __init__(self, conn: DuckDBConnection):
        self._conn = conn

    @property
    def con(self):
        return self._conn.con

    def add_edge(
        self,
        source_id: str,
        target_id: str,
        edge_type: str,
        weight: float = 1.0,
    ) -> None:
        self.con.execute(
            """
            INSERT OR REPLACE INTO edges (source_id, target_id, edge_type, weight, created_at)
            VALUES (?, ?, ?, ?, NOW())
            """,
            [source_id, target_id, edge_type, weight],
        )

    def add_edges_batch(self, edges: list[tuple[str, str, str, float]]) -> int:
        if not edges:
            return 0
        self.con.executemany(
            """
            INSERT OR REPLACE INTO edges (source_id, target_id, edge_type, weight, created_at)
            VALUES (?, ?, ?, ?, NOW())
            """,
            edges,
        )
        return len(edges)

    def get_edges(
        self,
        fragment_id: str,
        edge_type: str | None = None,
        direction: str = "outgoing",
    ) -> list[dict]:
        conditions = []
        params = []

        if direction in ("outgoing", "both"):
            conditions.append("source_id = ?")
            params.append(fragment_id)
        if direction in ("incoming", "both"):
            if conditions:
                conditions = [f"({conditions[0]} OR target_id = ?)"]
                params.append(fragment_id)
            else:
                conditions.append("target_id = ?")
                params.append(fragment_id)

        if edge_type:
            conditions.append("edge_type = ?")
            params.append(edge_type)

        where = " AND ".join(conditions)
        rows = self.con.execute(
            f"""
            SELECT source_id, target_id, edge_type, weight
            FROM edges
            WHERE {where}
            ORDER BY weight DESC
            """,
            params,
        ).fetchall()

        return [
            {"source_id": r[0], "target_id": r[1], "edge_type": r[2], "weight": r[3]} for r in rows
        ]

    def find_similar(
        self,
        fragment_id: str,
        limit: int = 10,
    ) -> list[tuple[Fragment, float]]:
        rows = self.con.execute(
            """
            SELECT f.id, f.conversation_id, f.role, f.content, f.timestamp,
                   f.source_kind, f.source_id, f.metadata, e.weight
            FROM edges e
            JOIN fragments f ON f.id = e.target_id
            WHERE e.source_id = ? AND e.edge_type = 'SIMILAR_TO'
            ORDER BY e.weight DESC
            LIMIT ?
            """,
            [fragment_id, limit],
        ).fetchall()

        return [(row_to_fragment(row[:8]), row[8]) for row in rows]

    def build_follows_edges(self) -> int:
        self.con.execute("""
            INSERT OR REPLACE INTO edges (source_id, target_id, edge_type, weight, created_at)
            SELECT source_id, target_id, 'FOLLOWS', 1.0, NOW()
            FROM (
                SELECT
                    LAG(id) OVER (PARTITION BY conversation_id ORDER BY timestamp) as source_id,
                    id as target_id
                FROM fragments
                WHERE conversation_id IS NOT NULL
            )
            WHERE source_id IS NOT NULL
        """)
        count = self.con.execute(
            "SELECT COUNT(*) FROM edges WHERE edge_type = 'FOLLOWS'"
        ).fetchone()[0]
        return count

    def build_similar_edges(
        self,
        threshold: float = 0.8,
        k: int = 5,
        on_progress: ProgressCallback = None,
    ) -> int:
        max_distance = 1.0 - threshold

        fragment_ids = self.con.execute(
            "SELECT id FROM fragments WHERE embedding IS NOT NULL"
        ).fetchall()
        total = len(fragment_ids)

        if total == 0:
            return 0

        edge_count = 0
        batch: list[tuple[str, str, str, float]] = []
        batch_size = 500

        for i, (frag_id,) in enumerate(fragment_ids):
            row = self.con.execute(
                "SELECT embedding FROM fragments WHERE id = ?", [frag_id]
            ).fetchone()
            if row is None or row[0] is None:
                continue
            embedding = row[0]

            neighbors = self.con.execute(
                f"""
                SELECT id, array_cosine_distance(embedding, $1::FLOAT[{len(embedding)}]) as dist
                FROM fragments
                WHERE id != $2
                  AND embedding IS NOT NULL
                ORDER BY array_cosine_distance(embedding, $1::FLOAT[{len(embedding)}])
                LIMIT {k}
                """,
                [embedding, frag_id],
            ).fetchall()

            for neighbor_id, distance in neighbors:
                if distance <= max_distance:
                    similarity = 1.0 - distance
                    batch.append((frag_id, neighbor_id, "SIMILAR_TO", similarity))

            if len(batch) >= batch_size:
                self.add_edges_batch(batch)
                edge_count += len(batch)
                batch.clear()

            if on_progress:
                on_progress(i + 1, total)

        if batch:
            self.add_edges_batch(batch)
            edge_count += len(batch)

        return edge_count

    def edge_stats(self) -> dict[str, EdgeTypeStats]:
        rows = self.con.execute("""
            SELECT edge_type, COUNT(*) as count, AVG(weight) as avg_weight
            FROM edges
            GROUP BY edge_type
        """).fetchall()
        return {row[0]: EdgeTypeStats(count=row[1], avg_weight=round(row[2], 4)) for row in rows}
