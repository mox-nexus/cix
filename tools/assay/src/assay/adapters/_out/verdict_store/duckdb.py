"""DuckDB verdict store — append MechanismResults and Adjudications as JSONL.

DuckDB reads JSONL natively, so we get a queryable store with no schema
migration. Each run gets its own subdirectory; the store appends to it.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path

from assay.domain.models import Adjudication, MechanismResult


class DuckdbVerdictStore:
    """Append-only JSONL store, queryable via DuckDB."""

    def __init__(self, run_dir: str) -> None:
        self._run_dir = Path(run_dir)
        self._run_dir.mkdir(parents=True, exist_ok=True)
        self._results_path = self._run_dir / "mechanism_results.jsonl"
        self._adjudications_path = self._run_dir / "adjudications.jsonl"

    def write_mechanism_result(self, result: MechanismResult) -> None:
        with self._results_path.open("a", encoding="utf-8") as f:
            f.write(result.model_dump_json() + "\n")

    def write_adjudication(self, adjudication: Adjudication) -> None:
        with self._adjudications_path.open("a", encoding="utf-8") as f:
            f.write(adjudication.model_dump_json() + "\n")

    def query(self, sql: str) -> Iterable[dict]:
        # Lazy import — only required when query() is called.
        import duckdb

        con = duckdb.connect(":memory:")
        # Register the JSONL files as views; allow the user's SQL to reference
        # them as `mechanism_results` and `adjudications`.
        if self._results_path.exists():
            con.execute(
                f"CREATE VIEW mechanism_results AS SELECT * FROM read_json_auto('{self._results_path}')"
            )
        if self._adjudications_path.exists():
            con.execute(
                f"CREATE VIEW adjudications AS SELECT * FROM read_json_auto('{self._adjudications_path}')"
            )
        # Use fetchall() + manual dict construction — avoids requiring
        # pandas/numpy as a runtime dep just to render rows.
        result = con.execute(sql)
        columns = [desc[0] for desc in result.description]
        rows = [dict(zip(columns, row, strict=False)) for row in result.fetchall()]
        return rows
