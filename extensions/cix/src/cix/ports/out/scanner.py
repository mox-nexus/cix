"""
Scanner port - discovering packages in directory trees.

Scanners understand the structure of extension packages:
- Where to look for extensions
- How to read package metadata
- What extension types are present

Different sources may use different package structures.
"""

from pathlib import Path
from typing import Protocol

from cix.domain.models import Package


class ScannerPort(Protocol):
    """
    Port for discovering packages in a directory tree.

    Implementations handle different package structures:
    - Claude plugin format (.claude-plugin/plugin.json)
    - Simple skill-only packages
    - Monorepo structures
    """

    def scan(self, root_path: Path) -> list[Package]:
        """
        Scan a directory tree for packages.

        Returns all packages found, with their extensions populated.
        """
        ...

    def can_scan(self, root_path: Path) -> bool:
        """
        Check if this scanner can handle the given path.

        Returns True if the path matches this scanner's expected structure.
        """
        ...
