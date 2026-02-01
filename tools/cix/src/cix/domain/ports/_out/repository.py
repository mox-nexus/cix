"""
Repository port - fetching and reading packages from sources.

This port handles the "read" side of sources:
- Fetching/updating source content
- Listing available packages
- Reading package details

The "write" side (creating packages) is handled differently.
"""

from pathlib import Path
from typing import Protocol

from cix.domain.models import Package, Source


class SourcePort(Protocol):
    """
    Port for interacting with package sources.

    Implementations might use:
    - Git repositories - standard, versioned
    - HTTP/REST - registries, APIs
    - Filesystem - local development
    """

    def fetch(self, source: Source) -> None:
        """
        Fetch or update source content.

        For git sources, this clones or pulls.
        Raises on network/access errors.
        """
        ...

    def list_packages(self, source: Source) -> list[Package]:
        """
        List all packages in a source.

        Returns packages discovered by scanning the source.
        Call fetch() first to ensure content is current.
        """
        ...

    def get_package(self, source: Source, name: str) -> Package | None:
        """
        Get a specific package by name, or None if not found.
        """
        ...

    def get_package_path(self, source: Source, package: Package) -> Path:
        """
        Get the filesystem path to a package's content.

        This is the path where the package files can be read/copied from.
        """
        ...

    def get_commit(self, source: Source) -> str:
        """
        Get the current commit hash for a source.

        Used for pinning installations to specific versions.
        """
        ...
