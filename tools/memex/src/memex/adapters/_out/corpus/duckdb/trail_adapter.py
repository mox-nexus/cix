"""DuckDB trail adapter — implements TrailPort.

Curated paths through knowledge (Bush's memex).
"""

import uuid

from memex.domain.models import Fragment, TrailSummary

from .connection import DuckDBConnection, row_to_fragment


class DuckDBTrailAdapter:
    """TrailPort implementation backed by DuckDB.

    Receives a DuckDBConnection — does not own the connection lifecycle.
    """

    def __init__(self, conn: DuckDBConnection):
        self._conn = conn

    @property
    def con(self):
        return self._conn.con

    def create_trail(self, name: str, description: str = "") -> str:
        trail_id = str(uuid.uuid4())
        self.con.execute(
            """
            INSERT INTO trails (id, name, description, created_at)
            VALUES (?, ?, ?, NOW())
            """,
            [trail_id, name, description],
        )
        return trail_id

    def add_to_trail(self, trail_name: str, fragment_id: str, note: str = "") -> int:
        trail = self._get_trail_by_name(trail_name)
        if not trail:
            raise ValueError(f"Trail '{trail_name}' not found")

        result = self.con.execute(
            "SELECT COALESCE(MAX(position), -1) + 1 FROM trail_entries WHERE trail_id = ?",
            [trail["id"]],
        ).fetchone()
        position = result[0]

        self.con.execute(
            """
            INSERT INTO trail_entries (trail_id, fragment_id, position, note, added_at)
            VALUES (?, ?, ?, ?, NOW())
            """,
            [trail["id"], fragment_id, position, note],
        )
        return position

    def get_trail(self, trail_name: str) -> list[tuple[Fragment, str]]:
        trail = self._get_trail_by_name(trail_name)
        if not trail:
            return []

        rows = self.con.execute(
            """
            SELECT f.id, f.conversation_id, f.role, f.content, f.timestamp,
                   f.source_kind, f.source_id, f.metadata, te.note
            FROM trail_entries te
            JOIN fragments f ON f.id = te.fragment_id
            WHERE te.trail_id = ?
            ORDER BY te.position
            """,
            [trail["id"]],
        ).fetchall()

        return [(row_to_fragment(row[:8]), row[8] or "") for row in rows]

    def list_trails(self) -> list[TrailSummary]:
        rows = self.con.execute("""
            SELECT t.id, t.name, t.description, t.created_at,
                   COUNT(te.fragment_id) as entry_count
            FROM trails t
            LEFT JOIN trail_entries te ON t.id = te.trail_id
            GROUP BY t.id, t.name, t.description, t.created_at
            ORDER BY t.created_at DESC
        """).fetchall()

        return [
            TrailSummary(
                id=row[0],
                name=row[1],
                description=row[2],
                created_at=row[3],
                entry_count=row[4],
            )
            for row in rows
        ]

    def delete_trail(self, trail_name: str) -> bool:
        trail = self._get_trail_by_name(trail_name)
        if not trail:
            return False
        self.con.execute("DELETE FROM trail_entries WHERE trail_id = ?", [trail["id"]])
        self.con.execute("DELETE FROM trails WHERE id = ?", [trail["id"]])
        return True

    def _get_trail_by_name(self, name: str) -> dict | None:
        row = self.con.execute(
            "SELECT id, name, description, created_at FROM trails WHERE name = ?",
            [name],
        ).fetchone()
        if not row:
            return None
        return {"id": row[0], "name": row[1], "description": row[2], "created_at": row[3]}
