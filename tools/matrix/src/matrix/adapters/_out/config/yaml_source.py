"""YamlConfigSource — reads config from a single YAML file.

One file, one read(). No discovery logic — that's the composition concern.
Satisfies ConfigSource protocol via structural typing.
"""

from pathlib import Path
from typing import Any

import yaml


class YamlConfigSource:
    """Reads a single YAML file as a config source.

    Returns empty dict if the file doesn't exist or is empty.
    """

    def __init__(self, path: Path) -> None:
        self._path = path

    def read(self) -> dict[str, Any]:
        """Read and parse YAML. Empty dict if file missing or empty."""
        if not self._path.exists():
            return {}
        with open(self._path) as f:
            data = yaml.safe_load(f)
        return data if isinstance(data, dict) else {}
