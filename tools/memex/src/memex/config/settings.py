"""Memex configuration.

All paths and settings configurable via environment variables.
"""

from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Memex settings with env var support.

    Environment variables:
        MEMEX_CORPUS_PATH: Path to DuckDB corpus file
        MEMEX_OTEL_ENABLED: Enable OpenTelemetry tracing
        MEMEX_OTEL_ENDPOINT: OTLP endpoint (default: localhost:4317)
        MEMEX_VERBOSE: Verbose output
    """

    # Storage
    corpus_path: Path = Path.home() / ".memex" / "corpus.duckdb"

    # Observability (opt-in)
    otel_enabled: bool = False
    otel_endpoint: str = "http://localhost:4317"
    otel_service_name: str = "memex"

    # Display
    verbose: bool = False

    class Config:
        env_prefix = "MEMEX_"


settings = Settings()
