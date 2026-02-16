"""Memex configuration.

Loads from (in order of precedence):
1. Environment variables (MEMEX_*)
2. Local .memex/ convention (walk up from CWD, like .git/)
3. Global config file (~/.memex/config.toml)
4. Defaults
"""

from pathlib import Path
from typing import Any

from pydantic import model_validator
from pydantic_settings import BaseSettings

# Shared key map for TOML → flat settings translation
_CONFIG_KEY_MAP = {
    ("corpus", "path"): "corpus_path",
    ("embedding", "model"): "embedding_model",
    ("embedding", "onnx_batch_size"): "onnx_batch_size",
    ("embedding", "onnx_threads"): "onnx_threads",
    ("ingest", "embed_by_default"): "embed_by_default",
    ("ingest", "batch_size"): "batch_size",
    ("search", "rerank_by_default"): "rerank_by_default",
    ("embedding", "provider"): "onnx_provider",
    ("search", "semantic_weight"): "semantic_weight",
}


def _parse_toml(path: Path) -> dict[str, Any]:
    """Parse a TOML config file into flat settings keys."""
    if not path.exists():
        return {}
    try:
        import tomllib

        with open(path, "rb") as f:
            data = tomllib.load(f)

        flat: dict[str, Any] = {}
        for section, values in data.items():
            if isinstance(values, dict):
                for key, value in values.items():
                    mapped_key = _CONFIG_KEY_MAP.get((section, key))
                    if mapped_key:
                        flat[mapped_key] = value
            else:
                flat[section] = values
        return flat
    except Exception:
        return {}


def _find_local_memex_dir() -> Path | None:
    """Walk up from CWD looking for .memex/ directory (like .git/).

    Returns the .memex/ directory path if found, None otherwise.
    Skips ~/.memex/ (the global store) to avoid false positives.
    Stops at filesystem root.

    Respects MEMEX_FORCE_GLOBAL env var — returns None immediately if set,
    forcing all resolution to the global store.
    """
    import os

    if os.environ.get("MEMEX_FORCE_GLOBAL"):
        return None
    try:
        current = Path.cwd()
    except OSError:
        return None
    global_dir = Path.home() / ".memex"
    for parent in [current, *current.parents]:
        candidate = parent / ".memex"
        if candidate.is_dir() and candidate.resolve() != global_dir.resolve():
            return candidate
    return None


def _load_global_config() -> dict[str, Any]:
    """Load global config from ~/.memex/config.toml."""
    return _parse_toml(Path.home() / ".memex" / "config.toml")


def _load_local_config() -> dict[str, Any]:
    """Load local .memex/ config if found via walk-up.

    Sets corpus_path to the local .memex/corpus.duckdb and
    merges any local config.toml overrides.
    """
    local_dir = _find_local_memex_dir()
    if not local_dir:
        return {}
    # Local .memex/ always provides its own corpus path
    result: dict[str, Any] = {"corpus_path": str(local_dir / "corpus.duckdb")}
    # Merge optional local config.toml
    local_toml = _parse_toml(local_dir / "config.toml")
    result.update(local_toml)
    return result


class Settings(BaseSettings):
    """Memex settings.

    Precedence: env vars > local .memex/ > global config > defaults

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

    # Embedding
    embedding_model: str = "nomic"  # "minilm" (384-dim) or "nomic" (768-dim)
    onnx_batch_size: int = 4  # Documents per ONNX inference call (lower = less RAM)
    onnx_threads: int = 2  # ONNX inter-op threads (lower = less RAM)
    onnx_provider: str = "auto"  # "auto", "coreml", "cuda", or "cpu"

    # Search
    rerank_by_default: bool = True
    semantic_weight: float = 0.6

    # Display
    verbose: bool = False

    model_config = {"env_prefix": "MEMEX_"}

    @model_validator(mode="before")
    @classmethod
    def load_config_file(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Layer config sources. Precedence: env vars > local > global > defaults."""
        global_config = _load_global_config()
        local_config = _load_local_config()
        return {**global_config, **local_config, **values}


_settings: Settings | None = None


def get_settings() -> Settings:
    """Get or create settings (lazy — defers construction until first access).

    This allows CLI flags (like --global) to set env vars before settings
    are constructed, respecting the precedence chain properly.
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reset_settings() -> None:
    """Reset the cached settings instance (for testing)."""
    global _settings
    _settings = None


def find_local_memex_dir() -> Path | None:
    """Find project-local .memex/ directory by walking up from CWD.

    Returns the .memex/ directory path if found, None otherwise.
    """
    return _find_local_memex_dir()


def get_active_memex_dir() -> Path:
    """Return the active memex directory (local if found, else global)."""
    local = _find_local_memex_dir()
    return local if local else Path.home() / ".memex"


def is_local_store() -> bool:
    """Check if the active store is project-local (not global)."""
    return _find_local_memex_dir() is not None


def get_global_config_path() -> Path:
    """Return the global config file path."""
    return Path.home() / ".memex" / "config.toml"


def get_global_memex_dir() -> Path:
    """Return the global memex directory path."""
    return Path.home() / ".memex"


def config_exists() -> bool:
    """Check if global config file exists."""
    return get_global_config_path().exists()


def create_default_config(corpus_path: Path | None = None) -> str:
    """Return default config file content.

    Args:
        corpus_path: Explicit corpus path. If None, uses global default.
    """
    path = str(corpus_path or Path.home() / ".memex" / "corpus.duckdb")
    return f'''# Memex Configuration
# Extended memory for you and your agents

[corpus]
path = "{path}"

[embedding]
# "minilm" (384-dim, fast) or "nomic" (768-dim, higher quality)
model = "nomic"
# ONNX execution provider: "auto" (detect GPU), "coreml", "cuda", "cpu"
# provider = "auto"
# ONNX runtime resource controls (lower = less RAM, slower)
# onnx_batch_size = 4   # docs per inference call (1-16)
# onnx_threads = 2      # inter-op parallelism (1-4)

[ingest]
embed_by_default = true
batch_size = 100

[search]
rerank_by_default = true
semantic_weight = 0.6
'''
