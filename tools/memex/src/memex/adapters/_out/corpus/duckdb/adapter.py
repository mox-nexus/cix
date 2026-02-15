"""DuckDB corpus adapter.

Implements CorpusPort. SQL is implementation detail, not port contract (Karman).
Supports:
- Semantic search via VSS extension (HNSW index, cosine similarity)
- Full-text search via FTS extension (BM25 scoring)
"""

from collections.abc import Callable, Iterable, Iterator
from importlib.resources import files
from pathlib import Path
from typing import TYPE_CHECKING

import duckdb

from memex.domain.models import Fragment, Provenance

if TYPE_CHECKING:
    from memex.domain.ports._out.corpus import ProgressCallback


class DuckDBCorpus:
    """DuckDB implementation of CorpusPort with semantic and full-text search.

    Embedding dimensions are received at construction time from the composition root.
    This ensures schema matches the embedder that will populate it.
    """

    def __init__(self, path: Path, embedding_dim: int | None = None):
        """Initialize DuckDB corpus.

        Args:
            path: Path to the DuckDB database file
            embedding_dim: Embedding dimensions for semantic search schema.
                          If None, corpus operates in FTS-only mode.
        """
        self.path = path
        self._embedding_dim = embedding_dim
        path.parent.mkdir(parents=True, exist_ok=True)
        self.con = duckdb.connect(str(path))
        self.con.execute("SET memory_limit = '2GB'")
        self._init_extensions()
        self._init_schema()
        self._init_meta_schema()

    def _init_extensions(self) -> None:
        """Initialize search extensions."""
        # VSS for semantic search
        try:
            self.con.execute("INSTALL vss")
            self.con.execute("LOAD vss")
            self._vss_available = True
        except duckdb.Error:
            self._vss_available = False

        # FTS for BM25 full-text search
        try:
            self.con.execute("INSTALL fts")
            self.con.execute("LOAD fts")
            self._fts_available = True
        except duckdb.Error:
            self._fts_available = False

    def _init_schema(self) -> None:
        """Initialize database schema.

        Creates embedding column only if embedding_dim is provided.
        """
        # Base schema without embedding column
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

        # Add embedding column if dimensions specified
        if self._embedding_dim:
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

        # HNSW index for semantic search (if VSS available and embeddings enabled)
        self._create_hnsw_index()

        # Edges table — graph overlay on fragments
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
        self.con.execute("CREATE INDEX IF NOT EXISTS idx_edges_source ON edges(source_id)")
        self.con.execute("CREATE INDEX IF NOT EXISTS idx_edges_target ON edges(target_id)")
        self.con.execute("CREATE INDEX IF NOT EXISTS idx_edges_type ON edges(edge_type)")

        # Trails — associative paths through knowledge (Bush's memex)
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
        """Initialize _memex_meta table for schema versioning and provenance.

        Key-value store for corpus metadata. Extensible without schema changes.
        """
        self.con.execute("""
            CREATE TABLE IF NOT EXISTS _memex_meta (
                key VARCHAR PRIMARY KEY,
                value VARCHAR NOT NULL,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Set schema version if not present
        if self.get_meta("schema_version") is None:
            self.set_meta("schema_version", "1")

    def get_meta(self, key: str) -> str | None:
        """Get metadata value by key."""
        result = self.con.execute("SELECT value FROM _memex_meta WHERE key = ?", [key]).fetchone()
        return result[0] if result else None

    def set_meta(self, key: str, value: str) -> None:
        """Set metadata value (upsert)."""
        self.con.execute(
            """
            INSERT OR REPLACE INTO _memex_meta (key, value, updated_at)
            VALUES (?, ?, NOW())
            """,
            [key, value],
        )

    def _ensure_embedding_column(self) -> None:
        """Ensure embedding column exists with correct dimensions."""
        columns = self.con.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_name = 'fragments'"
        ).fetchall()
        column_names = {row[0] for row in columns}

        if "embedding" not in column_names:
            self.con.execute(
                f"ALTER TABLE fragments ADD COLUMN embedding FLOAT[{self._embedding_dim}]"
            )

    def _ensure_fts_index(self) -> None:
        """Create FTS index if it doesn't exist."""
        if not self._fts_available:
            return
        try:
            # Check if index exists by trying to use it
            self.con.execute(
                "SELECT * FROM fts_main_fragments.match_bm25('test', fields := 'content') LIMIT 0"
            )
        except duckdb.Error:
            # Index doesn't exist, create it
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
                # Index creation failed, fall back to ILIKE
                self._fts_available = False

    def rebuild_fts_index(self) -> None:
        """Rebuild FTS index after data changes."""
        if not self._fts_available:
            return
        try:
            self.con.execute("PRAGMA drop_fts_index('fragments')")
        except duckdb.Error:
            pass
        self._ensure_fts_index()

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
                )
            )
            if len(batch) >= batch_size:
                self._insert_batch(batch)
                batch = []

        if batch:
            self._insert_batch(batch)

        return self._fragment_count() - count_before

    def _insert_batch(self, batch: list[tuple]) -> None:
        """Insert a batch of fragment tuples using executemany."""
        self.con.executemany(
            """
            INSERT INTO fragments
                (id, conversation_id, role, content, timestamp, source_kind, source_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT (id) DO NOTHING
            """,
            batch,
        )

    def _fragment_count(self) -> int:
        """Get total fragment count."""
        result = self.con.execute("SELECT COUNT(*) FROM fragments").fetchone()
        return result[0] if result else 0

    def store_with_embeddings(
        self,
        fragments: Iterable[Fragment],
        embedder: Callable[[str], list[float]],
    ) -> int:
        """Store fragments with embeddings in batches. Returns count of new fragments."""
        if not self._embedding_dim:
            msg = "Corpus created without embedding support. Pass embedding_dim."
            raise ValueError(msg)

        batch_size = 100  # Smaller batches — embedding generation is the bottleneck
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
                    embedding,
                )
            )
            if len(batch) >= batch_size:
                self.con.executemany(
                    f"""
                    INSERT INTO fragments (
                        id, conversation_id, role, content,
                        timestamp, source_kind, source_id, embedding
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?::FLOAT[{self._embedding_dim}])
                    ON CONFLICT (id) DO NOTHING
                    """,
                    batch,
                )
                batch = []

        if batch:
            self.con.executemany(
                f"""
                INSERT INTO fragments (
                    id, conversation_id, role, content,
                    timestamp, source_kind, source_id, embedding
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?::FLOAT[{self._embedding_dim}])
                ON CONFLICT (id) DO NOTHING
                """,
                batch,
            )

        return self._fragment_count() - count_before

    def _escape_ilike(self, s: str) -> str:
        """Escape ILIKE wildcards in user input."""
        return s.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")

    def search(
        self,
        query: str,
        limit: int = 20,
        source_kind: str | None = None,
    ) -> list[Fragment]:
        """Search fragments by content using BM25 (with ILIKE fallback).

        Uses DuckDB FTS extension for proper BM25 ranking when available.
        Falls back to ILIKE matching if FTS not installed.

        Args:
            query: Search terms
            limit: Maximum results to return
            source_kind: Optional filter by source type
        """
        if not query.strip():
            return []

        # Try BM25 first, fall back to ILIKE
        if self._fts_available:
            self._ensure_fts_index()
            return self._search_bm25(query, limit, source_kind)
        else:
            return self._search_ilike(query, limit, source_kind)

    def _search_bm25(
        self,
        query: str,
        limit: int,
        source_kind: str | None,
    ) -> list[Fragment]:
        """BM25 full-text search using DuckDB FTS extension."""
        try:
            # Build query with optional source filter
            source_filter = ""
            params = [query, limit]
            if source_kind:
                source_filter = "AND f.source_kind = ?"
                params = [query, source_kind, limit]

            rows = self.con.execute(
                f"""
                SELECT f.id, f.conversation_id, f.role, f.content,
                       f.timestamp, f.source_kind, f.source_id, fts.score
                FROM fts_main_fragments.match_bm25(?, fields := 'content') AS fts
                JOIN fragments f ON f.id = fts.id
                WHERE 1=1 {source_filter}
                ORDER BY fts.score DESC
                LIMIT ?
                """,
                params,
            ).fetchall()
            return [self._row_to_fragment(row[:7]) for row in rows]
        except duckdb.Error:
            # BM25 failed, fall back to ILIKE
            return self._search_ilike(query, limit, source_kind)

    def _search_ilike(
        self,
        query: str,
        limit: int,
        source_kind: str | None,
    ) -> list[Fragment]:
        """Fallback ILIKE search (all words must match)."""
        words = query.split()
        if not words:
            return []

        # Build: content ILIKE '%word1%' AND content ILIKE '%word2%' ...
        conditions = ["content ILIKE ?" for _ in words]
        params: list = [f"%{self._escape_ilike(word)}%" for word in words]

        if source_kind:
            conditions.append("source_kind = ?")
            params.append(source_kind)

        where_clause = " AND ".join(conditions)
        params.append(limit)

        rows = self.con.execute(
            f"""
            SELECT id, conversation_id, role, content, timestamp, source_kind, source_id
            FROM fragments
            WHERE {where_clause}
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            params,
        ).fetchall()
        return [self._row_to_fragment(row) for row in rows]

    def has_keyword_search(self) -> bool:
        """Check if FTS (BM25) is available."""
        return self._fts_available

    def find_by_conversation(self, conversation_id: str) -> list[Fragment]:
        """Get all fragments in a conversation.

        Supports prefix matching — if the full ID isn't found, tries prefix.
        """
        # Try exact match first
        rows = self.con.execute(
            """
            SELECT id, conversation_id, role, content, timestamp, source_kind, source_id
            FROM fragments
            WHERE conversation_id = ?
            ORDER BY timestamp
            """,
            [conversation_id],
        ).fetchall()

        if rows:
            return [self._row_to_fragment(row) for row in rows]

        # Try prefix match (short IDs like "66e1524a")
        rows = self.con.execute(
            """
            SELECT id, conversation_id, role, content, timestamp, source_kind, source_id
            FROM fragments
            WHERE conversation_id LIKE ? || '%'
            ORDER BY timestamp
            """,
            [conversation_id],
        ).fetchall()
        return [self._row_to_fragment(row) for row in rows]

    def list_conversations(
        self,
        limit: int = 50,
        offset: int = 0,
        source_kind: str | None = None,
    ) -> list[dict]:
        """List conversations with summary info, most recent first."""
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
            {
                "conversation_id": row[0],
                "message_count": row[1],
                "first_timestamp": row[2],
                "last_timestamp": row[3],
                "source_kind": row[4],
                "preview": (row[5][:120] + "...") if row[5] and len(row[5]) > 120 else row[5],
            }
            for row in rows
        ]

    def semantic_search(
        self,
        query_embedding: list[float],
        limit: int = 20,
        source_kind: str | None = None,
        min_score: float = 0.0,
    ) -> list[tuple[Fragment, float]]:
        """Search fragments by semantic similarity using HNSW index.

        Uses array_cosine_distance() to activate the HNSW ANN index.
        When source_kind filter is provided, uses CTE to fetch candidates
        via index first, then filters — because WHERE clauses prevent
        HNSW index activation.

        Args:
            query_embedding: Query vector (same dimensions as stored embeddings)
            limit: Maximum results to return
            source_kind: Optional filter by source type
            min_score: Minimum cosine similarity threshold (0-1)

        Returns:
            List of (Fragment, score) tuples, sorted by similarity descending.
        """
        if not self._vss_available or not self._embedding_dim:
            return []

        # Convert min_score (similarity) to max_distance for filtering
        max_distance = 1.0 - min_score

        if source_kind:
            # CTE pattern: HNSW index scan first, then filter
            # Over-fetch to account for filtering reducing results
            candidate_limit = limit * 5
            rows = self.con.execute(
                f"""
                WITH candidates AS (
                    SELECT
                        id, conversation_id, role, content, timestamp,
                        source_kind, source_id,
                        array_cosine_distance(
                            embedding, ?::FLOAT[{self._embedding_dim}]
                        ) as distance
                    FROM fragments
                    ORDER BY distance ASC
                    LIMIT ?
                )
                SELECT id, conversation_id, role, content, timestamp,
                       source_kind, source_id, distance
                FROM candidates
                WHERE source_kind = ? AND distance <= ?
                ORDER BY distance ASC
                LIMIT ?
                """,
                [query_embedding, candidate_limit, source_kind, max_distance, limit],
            ).fetchall()
        else:
            # Direct HNSW index scan (no filter needed)
            rows = self.con.execute(
                f"""
                SELECT
                    id, conversation_id, role, content, timestamp,
                    source_kind, source_id,
                    array_cosine_distance(embedding, ?::FLOAT[{self._embedding_dim}]) as distance
                FROM fragments
                ORDER BY distance ASC
                LIMIT ?
                """,
                [query_embedding, limit],
            ).fetchall()

        # Convert distance back to similarity for the port contract
        results = []
        for row in rows:
            distance = row[7]
            similarity = 1.0 - distance
            if similarity >= min_score:
                fragment = self._row_to_fragment(row[:7])
                results.append((fragment, similarity))
        return results

    def count_without_embeddings(self) -> int:
        """Count fragments without embeddings (for backfill progress)."""
        result = self.con.execute(
            "SELECT COUNT(*) FROM fragments WHERE embedding IS NULL"
        ).fetchone()
        return result[0] if result else 0

    def backfill_embeddings(
        self,
        embedder_stream: Callable[[list[str]], Iterator[list[float]]],
        batch_size: int = 100,
        on_progress: Callable[[int, int], None] | None = None,
    ) -> int:
        """Backfill embeddings using streaming — write-as-you-go.

        Memory-safe pipeline:
        1. Fetch a batch of texts from DB
        2. Feed to embedder_stream (generator — yields one vector at a time)
        3. Write each vector to DB immediately (no accumulation)
        4. Checkpoint periodically to flush WAL
        5. Drop/rebuild HNSW index around the whole operation

        Peak memory: model (~1GB) + one ONNX inference batch (~1-5GB) +
        one embedding vector (~3KB). No batch-sized accumulation.
        """
        if not self._embedding_dim:
            msg = "Corpus created without embedding support. Pass embedding_dim."
            raise ValueError(msg)

        total = self.count_without_embeddings()
        if total == 0:
            return 0

        self._drop_hnsw_index()

        updated = 0
        checkpoint_interval = 1000  # Flush WAL every 1000 individual writes

        try:
            while True:
                rows = self.con.execute(
                    f"""
                    SELECT id, content
                    FROM fragments
                    WHERE embedding IS NULL
                    LIMIT {batch_size}
                    """
                ).fetchall()

                if not rows:
                    break

                ids = [row[0] for row in rows]
                contents = [row[1] for row in rows]

                # Stream: embedder yields one vector at a time,
                # we write each immediately — nothing accumulates
                for frag_id, embedding in zip(ids, embedder_stream(contents)):
                    self.con.execute(
                        f"""
                        UPDATE fragments
                        SET embedding = ?::FLOAT[{self._embedding_dim}]
                        WHERE id = ?
                        """,
                        (embedding, frag_id),
                    )
                    updated += 1

                    if updated % checkpoint_interval == 0:
                        self.con.execute("CHECKPOINT")

                    if on_progress:
                        on_progress(updated, total)

        finally:
            self.con.execute("CHECKPOINT")
            self._create_hnsw_index()

        return updated

    def _drop_hnsw_index(self) -> None:
        """Drop HNSW index for bulk write operations."""
        try:
            self.con.execute("DROP INDEX IF EXISTS idx_fragments_embedding")
        except duckdb.Error:
            pass

    def _create_hnsw_index(self) -> None:
        """Create HNSW index for semantic search."""
        if not self._vss_available or not self._embedding_dim:
            return
        try:
            self.con.execute("""
                CREATE INDEX IF NOT EXISTS idx_fragments_embedding
                ON fragments USING HNSW (embedding)
                WITH (metric = 'cosine')
            """)
        except duckdb.Error:
            pass

    def has_semantic_search(self) -> bool:
        """Check if VSS extension is available."""
        return self._vss_available and self._embedding_dim is not None

    def embedding_dimensions(self) -> int | None:
        """Return stored embedding dimensions from schema.

        Queries information_schema to get the FLOAT array dimension.
        Returns None if no embedding column exists.
        """
        try:
            result = self.con.execute("""
                SELECT data_type FROM information_schema.columns
                WHERE table_name = 'fragments' AND column_name = 'embedding'
            """).fetchone()
            if result:
                # Parse "FLOAT[768]" to extract 768
                dtype = result[0]
                if "[" in dtype and "]" in dtype:
                    dim_str = dtype[dtype.index("[") + 1 : dtype.index("]")]
                    return int(dim_str)
            return None
        except Exception:
            return None

    # --- Edge Methods ---

    def add_edge(
        self,
        source_id: str,
        target_id: str,
        edge_type: str,
        weight: float = 1.0,
    ) -> None:
        """Add or update an edge between two fragments."""
        self.con.execute(
            """
            INSERT OR REPLACE INTO edges (source_id, target_id, edge_type, weight, created_at)
            VALUES (?, ?, ?, ?, NOW())
            """,
            [source_id, target_id, edge_type, weight],
        )

    def add_edges_batch(self, edges: list[tuple[str, str, str, float]]) -> int:
        """Batch insert edges. Each tuple: (source_id, target_id, edge_type, weight).

        Returns count of edges inserted.
        """
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
        """Get edges for a fragment.

        Args:
            fragment_id: The fragment ID
            edge_type: Optional filter by type ('FOLLOWS', 'SIMILAR_TO', etc.)
            direction: 'outgoing', 'incoming', or 'both'

        Returns:
            List of dicts with: source_id, target_id, edge_type, weight
        """
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
    ) -> list[tuple["Fragment", float]]:
        """Find fragments connected by SIMILAR_TO edges.

        Returns (Fragment, weight) tuples sorted by weight descending.
        """
        rows = self.con.execute(
            """
            SELECT f.id, f.conversation_id, f.role, f.content, f.timestamp,
                   f.source_kind, f.source_id, e.weight
            FROM edges e
            JOIN fragments f ON f.id = e.target_id
            WHERE e.source_id = ? AND e.edge_type = 'SIMILAR_TO'
            ORDER BY e.weight DESC
            LIMIT ?
            """,
            [fragment_id, limit],
        ).fetchall()

        return [(self._row_to_fragment(row[:7]), row[7]) for row in rows]

    def build_follows_edges(self) -> int:
        """Materialize FOLLOWS edges from conversation ordering.

        Within each conversation, fragment N FOLLOWS fragment N-1.
        Returns count of edges created.
        """
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
        on_progress: "ProgressCallback" = None,
    ) -> int:
        """Build SIMILAR_TO edges using HNSW ANN index.

        For each fragment, queries the HNSW index for k nearest neighbors.
        O(n * log n) via ANN, not O(n²) brute force.

        Args:
            threshold: Minimum cosine similarity (0-1)
            k: Max similar neighbors per fragment
            on_progress: Callback(processed, total) for progress updates

        Returns:
            Count of edges created.
        """
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
            neighbors = self.con.execute(
                f"""
                SELECT f2.id, array_cosine_distance(f1.embedding, f2.embedding) as dist
                FROM fragments f1, fragments f2
                WHERE f1.id = ?
                  AND f2.id != f1.id
                  AND f2.embedding IS NOT NULL
                ORDER BY array_cosine_distance(f1.embedding, f2.embedding)
                LIMIT {k}
                """,
                [frag_id],
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

    def edge_stats(self) -> dict:
        """Get edge statistics by type."""
        rows = self.con.execute("""
            SELECT edge_type, COUNT(*) as count, AVG(weight) as avg_weight
            FROM edges
            GROUP BY edge_type
        """).fetchall()
        return {row[0]: {"count": row[1], "avg_weight": round(row[2], 4)} for row in rows}

    # --- Trail Methods ---

    def create_trail(self, name: str, description: str = "") -> str:
        """Create a new trail. Returns trail ID."""
        import uuid

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
        """Add a fragment to the end of a trail. Returns new position."""
        trail = self._get_trail_by_name(trail_name)
        if not trail:
            raise ValueError(f"Trail '{trail_name}' not found")

        # Get next position
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

    def get_trail(self, trail_name: str) -> list[tuple["Fragment", str]]:
        """Get all fragments in a trail, in order.

        Returns list of (Fragment, note) tuples.
        """
        trail = self._get_trail_by_name(trail_name)
        if not trail:
            return []

        rows = self.con.execute(
            """
            SELECT f.id, f.conversation_id, f.role, f.content, f.timestamp,
                   f.source_kind, f.source_id, te.note
            FROM trail_entries te
            JOIN fragments f ON f.id = te.fragment_id
            WHERE te.trail_id = ?
            ORDER BY te.position
            """,
            [trail["id"]],
        ).fetchall()

        return [(self._row_to_fragment(row[:7]), row[7] or "") for row in rows]

    def list_trails(self) -> list[dict]:
        """List all trails with entry counts."""
        rows = self.con.execute("""
            SELECT t.id, t.name, t.description, t.created_at,
                   COUNT(te.fragment_id) as entry_count
            FROM trails t
            LEFT JOIN trail_entries te ON t.id = te.trail_id
            GROUP BY t.id, t.name, t.description, t.created_at
            ORDER BY t.created_at DESC
        """).fetchall()

        return [
            {
                "id": row[0],
                "name": row[1],
                "description": row[2],
                "created_at": row[3],
                "entry_count": row[4],
            }
            for row in rows
        ]

    def delete_trail(self, trail_name: str) -> bool:
        """Delete a trail and its entries. Returns True if found."""
        trail = self._get_trail_by_name(trail_name)
        if not trail:
            return False
        self.con.execute("DELETE FROM trail_entries WHERE trail_id = ?", [trail["id"]])
        self.con.execute("DELETE FROM trails WHERE id = ?", [trail["id"]])
        return True

    def _get_trail_by_name(self, name: str) -> dict | None:
        """Get trail by name."""
        row = self.con.execute(
            "SELECT id, name, description, created_at FROM trails WHERE name = ?",
            [name],
        ).fetchone()
        if not row:
            return None
        return {"id": row[0], "name": row[1], "description": row[2], "created_at": row[3]}

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
