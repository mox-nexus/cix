"""Memex configuration.

Loads from (in order of precedence):
1. Environment variables (MEMEX_*)
2. Config file (~/.memex/config.toml)
3. Defaults
"""

from pathlib import Path
from typing import Any

from pydantic import model_validator
from pydantic_settings import BaseSettings


def _load_config_file() -> dict[str, Any]:
    """Load config from ~/.memex/config.toml if it exists."""
    config_path = Path.home() / ".memex" / "config.toml"
    if not config_path.exists():
        return {}

    try:
        import tomllib
        with open(config_path, "rb") as f:
            data = tomllib.load(f)

        # Map nested config keys to flat settings keys
        key_map = {
            ("corpus", "path"): "corpus_path",
            ("ingest", "embed_by_default"): "embed_by_default",
            ("ingest", "batch_size"): "batch_size",
            ("search", "rerank_by_default"): "rerank_by_default",
            ("search", "semantic_weight"): "semantic_weight",
        }

        flat = {}
        for section, values in data.items():
            if isinstance(values, dict):
                for key, value in values.items():
                    mapped_key = key_map.get((section, key))
                    if mapped_key:
                        flat[mapped_key] = value
            else:
                flat[section] = values
        return flat
    except Exception:
        return {}


class Settings(BaseSettings):
    """Memex settings.

    Precedence: env vars > config file > defaults

    Environment variables:
        MEMEX_CORPUS_PATH: Path to DuckDB corpus file
        MEMEX_EMBED_BY_DEFAULT: Embed during ingest (default: true)
        MEMEX_BATCH_SIZE: Fragments per batch for embedding
        MEMEX_RERANK_BY_DEFAULT: Enable reranking in search
        MEMEX_SEMANTIC_WEIGHT: Weight for semantic vs keyword (0-1)
    """

    # Storage
    corpus_path: Path = Path.home() / ".memex" / "corpus.duckdb"

    # Ingest
    embed_by_default: bool = True
    batch_size: int = 100

    # Search
    rerank_by_default: bool = True
    semantic_weight: float = 0.6

    # Observability (opt-in)
    otel_enabled: bool = False
    otel_endpoint: str = "http://localhost:4317"
    otel_service_name: str = "memex"

    # Display
    verbose: bool = False

    model_config = {"env_prefix": "MEMEX_"}

    @model_validator(mode="before")
    @classmethod
    def load_config_file(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Load config file values as defaults (env vars take precedence)."""
        file_config = _load_config_file()
        # File config provides defaults, passed values (env vars) override
        return {**file_config, **values}


settings = Settings()


def get_config_path() -> Path:
    """Return the config file path."""
    return Path.home() / ".memex" / "config.toml"


def get_memex_dir() -> Path:
    """Return the memex directory path."""
    return Path.home() / ".memex"


def config_exists() -> bool:
    """Check if config file exists."""
    return get_config_path().exists()


def create_default_config() -> str:
    """Return default config file content."""
    corpus_path = str(Path.home() / ".memex" / "corpus.duckdb")
    return f'''# Memex Configuration
# Extended memory for you and your agents

[corpus]
path = "{corpus_path}"

[ingest]
embed_by_default = true
batch_size = 100

[search]
rerank_by_default = true
semantic_weight = 0.6
'''
