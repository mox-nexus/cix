"""Shared DuckDB connection and schema management.

Owns the connection lifecycle, schema initialization, extensions,
metadata operations, and fragment deserialization. Adapter classes
receive a connection instance via constructor injection.
"""

import json
import logging
from pathlib import Path

import duckdb

from memex.domain.models import (
    EmbeddingConfig,
    Fragment,
    Provenance,
)

logger = logging.getLogger(__name__)


def row_to_fragment(row: tuple) -> Fragment:
    """Convert DB row to Fragment.

    Module-level function shared by all adapters.
    Expected column order: id, conversation_id, role, content,
    timestamp, source_kind, source_id, metadata.
    """
    meta_raw = row[7] if len(row) > 7 else None
    metadata = json.loads(meta_raw) if isinstance(meta_raw, str) else meta_raw
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
        metadata=metadata if metadata else None,
    )


class DuckDBConnection:
    """Shared DuckDB connection with schema management.

    Owns:
    - Connection lifecycle (open, close, checkpoint)
    - Schema initialization (all tables: fragments, edges, trails, _memex_meta)
    - Extension management (VSS, FTS)
    - HNSW index management
    - FTS index management
    - Metadata operations (get_meta, set_meta)
    - Embedding config recording
    """

    def __init__(self, path: Path, embedding_dim: int | None = None):
        self.path = path
        self.embedding_dim = embedding_dim
        path.parent.mkdir(parents=True, exist_ok=True)
        self.con = duckdb.connect(str(path))
        self.con.execute("SET memory_limit = '2GB'")
        self._init_extensions()
        self._init_schema()
        self._init_meta_schema()

    # --- Extensions ---

    def _init_extensions(self) -> None:
        """Initialize search extensions."""
        try:
            self.con.execute("INSTALL vss")
            self.con.execute("LOAD vss")
            self.vss_available = True
        except duckdb.Error:
            self.vss_available = False

        try:
            self.con.execute("INSTALL fts")
            self.con.execute("LOAD fts")
            self.fts_available = True
        except duckdb.Error:
            self.fts_available = False

    # --- Schema ---

    def _init_schema(self) -> None:
        """Initialize all database tables."""
        # Fragments
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

        self._ensure_column("fragments", "metadata", "JSON")

        if self.embedding_dim:
            self._ensure_embedding_column()

        self.con.execute(
            "CREATE INDEX IF NOT EXISTS idx_fragments_timestamp ON fragments(timestamp)"
        )
        self.con.execute(
            "CREATE INDEX IF NOT EXISTS idx_fragments_conversation ON fragments(conversation_id)"
        )
        self.con.execute(
            "CREATE INDEX IF NOT EXISTS idx_fragments_source ON fragments(source_kind)"
        )

        self.create_hnsw_index()

        # Edges
        self.con.execute("""
            CREATE TABLE IF NOT EXISTS edges (
                source_id VARCHAR NOT NULL,
                target_id VARCHAR NOT NULL,
                edge_type VARCHAR NOT NULL,
                weight FLOAT DEFAULT 1.0,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (source_id, target_id, edge_type)
            )
        """)
        self._ensure_column("edges", "metadata", "JSON")
        self.con.execute("CREATE INDEX IF NOT EXISTS idx_edges_source ON edges(source_id)")
        self.con.execute("CREATE INDEX IF NOT EXISTS idx_edges_target ON edges(target_id)")
        self.con.execute("CREATE INDEX IF NOT EXISTS idx_edges_type ON edges(edge_type)")

        # Trails
        self.con.execute("""
            CREATE TABLE IF NOT EXISTS trails (
                id VARCHAR PRIMARY KEY,
                name VARCHAR NOT NULL UNIQUE,
                description VARCHAR DEFAULT '',
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.con.execute("""
            CREATE TABLE IF NOT EXISTS trail_entries (
                trail_id VARCHAR NOT NULL REFERENCES trails(id),
                fragment_id VARCHAR NOT NULL REFERENCES fragments(id),
                position INTEGER NOT NULL,
                note VARCHAR DEFAULT '',
                added_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (trail_id, position)
            )
        """)
        self.con.execute(
            "CREATE INDEX IF NOT EXISTS idx_trail_entries_trail ON trail_entries(trail_id)"
        )

    def _init_meta_schema(self) -> None:
        """Initialize _memex_meta table."""
        self.con.execute("""
            CREATE TABLE IF NOT EXISTS _memex_meta (
                key VARCHAR PRIMARY KEY,
                value VARCHAR NOT NULL,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            )
        """)
        if self.get_meta("schema_version") is None:
            self.set_meta("schema_version", "2")
        elif self.get_meta("schema_version") == "1":
            self.set_meta("schema_version", "2")

    def _ensure_column(self, table: str, column: str, dtype: str) -> None:
        """Add column if it doesn't exist (schema migration)."""
        columns = self.con.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_name = ?",
            [table],
        ).fetchall()
        if column not in {row[0] for row in columns}:
            self.con.execute(f"ALTER TABLE {table} ADD COLUMN {column} {dtype}")

    def _ensure_embedding_column(self) -> None:
        """Ensure embedding column exists with correct dimensions."""
        self._ensure_column("fragments", "embedding", f"FLOAT[{self.embedding_dim}]")

    # --- Meta ---

    def get_meta(self, key: str) -> str | None:
        result = self.con.execute("SELECT value FROM _memex_meta WHERE key = ?", [key]).fetchone()
        return result[0] if result else None

    def set_meta(self, key: str, value: str) -> None:
        self.con.execute(
            """
            INSERT OR REPLACE INTO _memex_meta (key, value, updated_at)
            VALUES (?, ?, NOW())
            """,
            [key, value],
        )

    # --- HNSW Index ---

    def drop_hnsw_index(self) -> None:
        """Drop HNSW index for bulk write operations."""
        try:
            self.con.execute("DROP INDEX IF EXISTS idx_fragments_embedding")
        except duckdb.Error as e:
            logger.debug("Failed to drop HNSW index: %s", e)

    def create_hnsw_index(self) -> None:
        """Create HNSW index for semantic search.

        Temporarily lifts memory_limit for index construction.
        """
        if not self.vss_available or not self.embedding_dim:
            return
        try:
            self.con.execute("SET memory_limit = '8GB'")
            self.con.execute("""
                CREATE INDEX IF NOT EXISTS idx_fragments_embedding
                ON fragments USING HNSW (embedding)
                WITH (metric = 'cosine')
            """)
        except duckdb.Error as e:
            logger.debug("Failed to create HNSW index: %s", e)
        finally:
            self.con.execute("SET memory_limit = '2GB'")

    # --- FTS Index ---

    def ensure_fts_index(self) -> None:
        """Create FTS index if it doesn't exist."""
        if not self.fts_available:
            return
        try:
            self.con.execute(
                "SELECT * FROM fts_main_fragments.match_bm25('test', fields := 'content') LIMIT 0"
            )
        except duckdb.Error:
            try:
                self.con.execute("""
                    PRAGMA create_fts_index(
                        'fragments', 'id', 'content',
                        stemmer = 'english',
                        stopwords = 'english',
                        ignore = '[^a-zA-Z0-9]',
                        strip_accents = 1,
                        lower = 1
                    )
                """)
            except duckdb.Error:
                self.fts_available = False

    # --- Embedding Config ---

    def embedding_dimensions(self) -> int | None:
        """Return stored embedding dimensions from schema."""
        try:
            result = self.con.execute("""
                SELECT data_type FROM information_schema.columns
                WHERE table_name = 'fragments' AND column_name = 'embedding'
            """).fetchone()
            if result:
                dtype = result[0]
                if "[" in dtype and "]" in dtype:
                    dim_str = dtype[dtype.index("[") + 1 : dtype.index("]")]
                    return int(dim_str)
            return None
        except Exception:
            return None

    def record_embedding_config(self, config: EmbeddingConfig) -> None:
        """Record the embedding model used for this corpus."""
        self.set_meta("embedding_model", config.model_name)
        self.set_meta("embedding_dimensions", str(config.dimensions))

    # --- Lifecycle ---

    def checkpoint(self) -> None:
        """Flush WAL to disk."""
        self.con.execute("CHECKPOINT")

    def close(self) -> None:
        """Close connection."""
        self.con.close()

    def query_sql(self, sql: str):
        """Execute raw SQL. DuckDB-specific, not in port."""
        return self.con.execute(sql).fetchall()
