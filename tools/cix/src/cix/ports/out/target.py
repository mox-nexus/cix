"""
Target port - where extensions get installed.

Targets are the systems that consume extensions:
- Claude Code (primary)
- Cursor (future)
- Other AI-assisted development environments

Each target has its own conventions for extension location and format.
"""

from pathlib import Path
from typing import Protocol

from cix.domain.models import Package


class TargetPort(Protocol):
    """
    Port for installing packages to a target system.

    Implementations handle the specifics of each target:
    - Where extensions are stored
    - What format is expected
    - How to detect if target is available
    """

    @property
    def name(self) -> str:
        """Target identifier (e.g., 'claude-code')."""
        ...

    def is_available(self) -> bool:
        """
        Check if this target is available on the current system.

        Returns True if the target is installed and configured.
        """
        ...

    def install(self, package: Package, source_path: Path) -> None:
        """
        Install a package to this target.

        Copies/links extension files to the target's extension directory.
        Raises on permission or path errors.
        """
        ...

    def uninstall(self, package: Package) -> None:
        """
        Remove a package from this target.

        Removes extension files from the target's extension directory.
        """
        ...

    def is_installed(self, package: Package) -> bool:
        """Check if a package is currently installed to this target."""
        ...

    def get_config_path(self) -> Path:
        """
        Get the path to the target's configuration directory.

        This is where extensions are stored.
        """
        ...
