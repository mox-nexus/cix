"""ConfigSource — reads raw config from a single tier.

Port contract: return a dict. No validation, no schema awareness.
Multiple ConfigSources compose via deep merge before validation.
"""

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ConfigSource(Protocol):
    """Reads config data from one tier.

    Returns raw dict. Validation happens elsewhere (Pydantic).
    Returns empty dict if the source doesn't exist.
    """

    def read(self) -> dict[str, Any]:
        """Read config from this source. Empty dict if absent."""
        ...
