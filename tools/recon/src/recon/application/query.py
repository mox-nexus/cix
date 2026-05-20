"""Query an archive directory of JSONL files via DuckDB.

Pure application-layer logic: given an archive path and a SQL string, returns
columns and rows. No I/O beyond DuckDB reading JSONL. CLI formats the output.

Keeping this out of the CLI adapter means a future non-CLI frontend (MCP
server, Python API, HTTP endpoint) can reuse the same query path.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from recon.domain.exceptions import ReconError

_TABLE_NAME_SAFE = re.compile(r"[^a-zA-Z0-9_]")


def available_tables(archive_dir: Path) -> list[str]:
    """List DuckDB-style table names derivable from the archive's JSONL files."""
    return [_TABLE_NAME_SAFE.sub("_", jf.stem) for jf in sorted(archive_dir.glob("*.jsonl"))]


def execute(archive_dir: Path, sql: str) -> tuple[list[str], list[tuple[Any, ...]]]:
    """Execute SQL against every JSONL file in the archive as DuckDB views.

    Returns (columns, rows). Raises ReconError if there are no JSONL files
    or if the SQL fails. Does not print; caller decides how to present.
    """
    import duckdb  # imported lazily — CLI-only dep used only when querying

    jsonl_files = sorted(archive_dir.glob("*.jsonl"))
    if not jsonl_files:
        msg = f"No JSONL files in archive: {archive_dir}"
        raise ReconError(msg)

    conn = duckdb.connect()
    try:
        for jf in jsonl_files:
            table_name = _TABLE_NAME_SAFE.sub("_", jf.stem)
            jf_str = str(jf).replace("'", "''")
            conn.execute(
                f"CREATE VIEW \"{table_name}\" AS SELECT * FROM read_json_auto('{jf_str}')"
            )

        try:
            result = conn.execute(sql)
        except duckdb.Error as exc:
            tables = ", ".join(available_tables(archive_dir))
            msg = f"SQL error: {exc}\nAvailable tables: {tables}"
            raise ReconError(msg) from exc

        columns = [desc[0] for desc in result.description]
        rows = result.fetchall()
        return columns, rows
    finally:
        conn.close()
