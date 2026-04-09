"""DuckDB corpus adapter."""

from memex.adapters._out.corpus.duckdb.adapter import DuckDBCorpus
from memex.adapters._out.corpus.duckdb.connection import DuckDBConnection
from memex.adapters._out.corpus.duckdb.corpus_adapter import DuckDBCorpusAdapter
from memex.adapters._out.corpus.duckdb.graph_adapter import DuckDBGraphAdapter
from memex.adapters._out.corpus.duckdb.trail_adapter import DuckDBTrailAdapter

__all__ = [
    "DuckDBConnection",
    "DuckDBCorpus",
    "DuckDBCorpusAdapter",
    "DuckDBGraphAdapter",
    "DuckDBTrailAdapter",
]
