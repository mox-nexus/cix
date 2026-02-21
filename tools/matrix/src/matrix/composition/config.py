"""Config composition — 3-tier discovery, merge, validate.

Clients call load_config(MyConfigType) and get back Config[MyConfigType]
with both Matrix platform settings and their own validated section.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, TypeVar

from pydantic import BaseModel

from matrix.domain.config import Config, MatrixConfig

C = TypeVar("C", bound=BaseModel)


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Recursive dict merge. Override wins. Lists replace entirely."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def discover_sources(
    tool: str,
    project_root: Path | None = None,
) -> list[Path]:
    """3-tier config discovery for a tool. Returns paths in priority order (first = lowest).

    Tier 1: Pydantic model defaults (no file — built into the schema).
    Tier 2: User-level — ~/.{tool}/config.yaml
    Tier 3: Project-level — ./{tool}.yaml (or project_root/{tool}.yaml)

    Each tool owns its config location. Matrix provides the pattern,
    the tool provides the name.
    """
    sources: list[Path] = []

    # Tier 2: user-level
    sources.append(Path.home() / f".{tool}" / "config.yaml")

    # Tier 3: project-level
    root = project_root or Path.cwd()
    sources.append(root / f"{tool}.yaml")

    return sources


def load_config(  # noqa: UP047
    client_type: type[C],
    client_key: str,
    sources: list[Path] | None = None,
) -> Config[C]:
    """Load and validate composed config.

    Args:
        client_type: Pydantic model class for client config section.
        client_key: YAML key for the client section (e.g., "ix", "memex", "radix").
        sources: Config file paths in priority order.
            If None, uses discover_sources(client_key) for 3-tier discovery.

    Returns:
        Validated Config[C] with both matrix and client sections.
    """
    from matrix.adapters._out.config.yaml_source import YamlConfigSource

    if sources is None:
        sources = discover_sources(client_key)

    merged: dict[str, Any] = {}
    for path in sources:
        tier_data = YamlConfigSource(path).read()
        if tier_data:
            merged = deep_merge(merged, tier_data)

    matrix_data = merged.get("matrix", {})
    client_data = merged.get(client_key, {})

    matrix_config = MatrixConfig.model_validate(matrix_data)
    client_config = client_type.model_validate(client_data)

    return Config(matrix=matrix_config, client=client_config)
