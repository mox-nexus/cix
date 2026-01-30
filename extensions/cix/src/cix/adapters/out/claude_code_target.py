"""
Claude Code target adapter - installing extensions to Claude Code.

Extensions are installed to ~/.claude/plugins/<package-name>/
"""

import shutil
from pathlib import Path

from cix.domain.models import Package


class ClaudeCodeTargetAdapter:
    """
    Target implementation for Claude Code.

    Installs extensions to the Claude Code plugins directory.
    """

    def __init__(self, global_config: bool = True) -> None:
        """
        Initialize the Claude Code target.

        Args:
            global_config: If True, use ~/.claude; if False, use ./.claude
        """
        self._global = global_config

    @property
    def name(self) -> str:
        """Target identifier."""
        return "claude-code"

    def is_available(self) -> bool:
        """Check if Claude Code is available."""
        # Check if ~/.claude exists or claude CLI is available
        if self._get_config_path().exists():
            return True

        # Check for claude CLI
        return shutil.which("claude") is not None

    def install(self, package: Package, source_path: Path) -> None:
        """Install a package to Claude Code."""
        target_path = self._get_package_path(package)

        # Remove existing if present
        if target_path.exists():
            shutil.rmtree(target_path)

        # Copy package content
        shutil.copytree(source_path, target_path, dirs_exist_ok=True)

    def uninstall(self, package: Package) -> None:
        """Remove a package from Claude Code."""
        target_path = self._get_package_path(package)

        if target_path.exists():
            shutil.rmtree(target_path)

    def is_installed(self, package: Package) -> bool:
        """Check if a package is installed."""
        return self._get_package_path(package).exists()

    def get_config_path(self) -> Path:
        """Get the Claude Code configuration directory."""
        return self._get_config_path()

    # =========================================================================
    # Private Helpers
    # =========================================================================

    def _get_config_path(self) -> Path:
        """Get the config directory path."""
        if self._global:
            return Path.home() / ".claude"
        return Path.cwd() / ".claude"

    def _get_package_path(self, package: Package) -> Path:
        """Get the installation path for a package."""
        return self._get_config_path() / "plugins" / package.name
