"""
Registry port - persistence of sources and installations.

The registry tracks:
- Registered sources (extension marketplaces)
- Installed packages (what's been installed where)

This is the "memory" of cix - where state lives between invocations.
"""

from typing import Protocol

from cix.domain.models import Installation, Source


class RegistryPort(Protocol):
    """
    Port for managing cix state (sources and installations).

    Implementations might use:
    - Filesystem (JSON files) - simple, debuggable
    - SQLite - queryable, ACID
    - Remote service - shared state
    """

    # Source management
    def list_sources(self) -> list[Source]:
        """List all registered sources."""
        ...

    def add_source(self, source: Source) -> None:
        """Register a new source. Raises if name already exists."""
        ...

    def remove_source(self, name: str) -> None:
        """Unregister a source. Raises if not found."""
        ...

    def get_source(self, name: str) -> Source | None:
        """Get a source by name, or None if not found."""
        ...

    def get_default_source(self) -> Source | None:
        """Get the default source, or None if none set."""
        ...

    def set_default_source(self, name: str) -> None:
        """Set a source as the default. Raises if not found."""
        ...

    # Installation management
    def list_installations(self, target: str | None = None) -> list[Installation]:
        """List all installations, optionally filtered by target."""
        ...

    def add_installation(self, installation: Installation) -> None:
        """Record a new installation."""
        ...

    def remove_installation(self, installation_id: str) -> None:
        """Remove an installation record. Raises if not found."""
        ...

    def get_installation(self, installation_id: str) -> Installation | None:
        """Get an installation by ID (source/package), or None if not found."""
        ...
