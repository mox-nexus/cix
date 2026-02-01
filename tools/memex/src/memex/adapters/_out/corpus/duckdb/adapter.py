"""DuckDB corpus adapter.

Implements CorpusPort. SQL is implementation detail, not port contract (Karman).
"""

from collections.abc import Iterable
from importlib.resources import files
from pathlib import Path

import duckdb

from memex.domain.models import Fragment, Provenance


class DuckDBCorpus:
    """DuckDB implementation of CorpusPort."""

    def __init__(self, path: Path):
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        self.con = duckdb.connect(str(path))
        self._init_schema()

    def _init_schema(self) -> None:
        self.con.execute("""
            CREATE TABLE IF NOT EXISTS fragments (
                id VARCHAR PRIMARY KEY,
                conversation_id VARCHAR,
                role VARCHAR NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMPTZ,
                source_kind VARCHAR NOT NULL,
                source_id VARCHAR NOT NULL
            )
        """)
        self.con.execute(
            "CREATE INDEX IF NOT EXISTS idx_fragments_timestamp ON fragments(timestamp)"
        )
        self.con.execute(
            "CREATE INDEX IF NOT EXISTS idx_fragments_conversation ON fragments(conversation_id)"
        )
        self.con.execute(
            "CREATE INDEX IF NOT EXISTS idx_fragments_source ON fragments(source_kind)"
        )

    def store(self, fragments: Iterable[Fragment]) -> int:
        """Store fragments. Returns count of new fragments."""
        inserted = 0
        for frag in fragments:
            try:
                self.con.execute(
                    """
                    INSERT INTO fragments
                        (id, conversation_id, role, content, timestamp, source_kind, source_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT (id) DO NOTHING
                    """,
                    [
                        frag.id,
                        frag.conversation_id,
                        frag.role,
                        frag.content,
                        frag.timestamp,
                        frag.provenance.source_kind,
                        frag.provenance.source_id,
                    ],
                )
                inserted += 1
            except duckdb.ConstraintException:
                pass
        return inserted

    def search(self, query: str, limit: int = 20) -> list[Fragment]:
        """Search fragments by content."""
        rows = self.con.execute(
            """
            SELECT id, conversation_id, role, content, timestamp, source_kind, source_id
            FROM fragments
            WHERE content ILIKE ?
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            [f"%{query}%", limit],
        ).fetchall()
        return [self._row_to_fragment(row) for row in rows]

    def find_by_conversation(self, conversation_id: str) -> list[Fragment]:
        """Get all fragments in a conversation."""
        rows = self.con.execute(
            """
            SELECT id, conversation_id, role, content, timestamp, source_kind, source_id
            FROM fragments
            WHERE conversation_id = ?
            ORDER BY timestamp
            """,
            [conversation_id],
        ).fetchall()
        return [self._row_to_fragment(row) for row in rows]

    def stats(self) -> dict:
        """Get corpus statistics."""
        result = self.con.execute("""
            SELECT
                COUNT(*) as total_fragments,
                COUNT(DISTINCT conversation_id) as conversations,
                MIN(timestamp) as earliest,
                MAX(timestamp) as latest,
                COUNT(DISTINCT source_kind) as sources
            FROM fragments
        """).fetchone()

        return {
            "total_fragments": result[0],
            "conversations": result[1],
            "earliest": result[2],
            "latest": result[3],
            "sources": result[4],
        }

    def schema(self) -> dict:
        """Return schema information for introspection."""
        columns = self.con.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'fragments'
            ORDER BY ordinal_position
        """).fetchall()

        return {
            "fragments": [{"name": c[0], "type": c[1], "nullable": c[2] == "YES"} for c in columns]
        }

    def skill(self) -> str:
        """Return skill documentation for DuckDB corpus."""
        skill_file = files(__package__) / "skill.md"
        return skill_file.read_text()

    def close(self) -> None:
        """Close connection."""
        self.con.close()

    # --- DuckDB-specific methods (not in port contract) ---

    def query_sql(self, sql: str):
        """Execute raw SQL. DuckDB-specific, not in port."""
        return self.con.execute(sql).fetchall()

    def _row_to_fragment(self, row: tuple) -> Fragment:
        """Convert DB row to Fragment."""
        return Fragment(
            id=row[0],
            conversation_id=row[1],
            role=row[2],
            content=row[3],
            provenance=Provenance(
                source_kind=row[5],
                source_id=row[6],
                timestamp=row[4],
            ),
        )
