"""
Git repository adapter - fetching packages from git sources.

Uses GitPython to clone/fetch repositories and scan for packages.
"""

import json
from pathlib import Path

from git import Repo
from git.exc import GitCommandError

from cix.domain.models import Extensions, Package, Source


class GitSourceAdapter:
    """
    Source implementation using git repositories.

    Repositories are cloned to a cache directory and updated on fetch.
    """

    def __init__(self, cache_dir: Path | None = None) -> None:
        self._cache_dir = cache_dir or Path.home() / ".cix" / "cache"
        self._cache_dir.mkdir(parents=True, exist_ok=True)

    def fetch(self, source: Source) -> None:
        """Clone or update a source repository."""
        repo_path = self._get_repo_path(source)

        if repo_path.exists():
            # Update existing repo
            try:
                repo = Repo(repo_path)
                origin = repo.remote("origin")
                origin.fetch()

                # Checkout specific ref or pull latest
                if source.ref:
                    repo.git.checkout(source.ref)
                else:
                    # Pull the current branch
                    if repo.head.is_detached:
                        repo.git.checkout("main")
                    origin.pull()
            except GitCommandError as e:
                raise RuntimeError(f"Failed to update source '{source.name}': {e}")
        else:
            # Clone new repo
            try:
                repo = Repo.clone_from(source.url, repo_path)
                if source.ref:
                    repo.git.checkout(source.ref)
            except GitCommandError as e:
                raise RuntimeError(f"Failed to clone source '{source.name}': {e}")

    def list_packages(self, source: Source) -> list[Package]:
        """List all packages in a source repository."""
        repo_path = self._get_repo_path(source)

        if not repo_path.exists():
            return []

        packages = []

        # Scan for packages (look for plugin.json or package markers)
        for item in repo_path.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                package = self._scan_package(item)
                if package:
                    packages.append(package)

        # Also check for packages in a 'packages' or 'extensions' subdirectory
        for subdir_name in ["packages", "extensions", "plugins"]:
            subdir = repo_path / subdir_name
            if subdir.exists():
                for item in subdir.iterdir():
                    if item.is_dir() and not item.name.startswith("."):
                        package = self._scan_package(item)
                        if package:
                            packages.append(package)

        return packages

    def get_package(self, source: Source, name: str) -> Package | None:
        """Get a specific package by name."""
        for package in self.list_packages(source):
            if package.name == name:
                return package
        return None

    def get_package_path(self, source: Source, package: Package) -> Path:
        """Get the filesystem path to a package's content."""
        return package.path

    def get_commit(self, source: Source) -> str:
        """Get the current commit hash for a source."""
        repo_path = self._get_repo_path(source)
        if not repo_path.exists():
            return ""

        repo = Repo(repo_path)
        return repo.head.commit.hexsha

    # =========================================================================
    # Private Helpers
    # =========================================================================

    def _get_repo_path(self, source: Source) -> Path:
        """Get the cache path for a source repository."""
        return self._cache_dir / source.name

    def _scan_package(self, path: Path) -> Package | None:
        """
        Scan a directory for package content.

        Looks for:
        - .claude-plugin/plugin.json (Claude plugin format)
        - package.json with cix fields
        - Skills/agents/hooks directories
        """
        # Check for Claude plugin format
        plugin_json = path / ".claude-plugin" / "plugin.json"
        if plugin_json.exists():
            return self._parse_claude_plugin(path, plugin_json)

        # Check for direct extension directories (skill-only packages)
        extensions = self._scan_extensions(path)
        if not extensions.is_empty:
            return Package(
                name=path.name,
                description=f"Extension package: {extensions.summary}",
                version="0.0.0",
                path=path,
                extensions=extensions,
            )

        return None

    def _parse_claude_plugin(self, path: Path, plugin_json: Path) -> Package:
        """Parse a Claude plugin format package."""
        data = json.loads(plugin_json.read_text())

        extensions = self._scan_extensions(path)

        return Package(
            name=data.get("name", path.name),
            description=data.get("description", ""),
            version=data.get("version", "0.0.0"),
            path=path,
            extensions=extensions,
            author=data.get("author", {}).get("name"),
            license=data.get("license"),
        )

    def _scan_extensions(self, path: Path) -> Extensions:
        """Scan a directory for extension content."""
        skills = []
        agents = []
        hooks = []
        mcps = []

        # Scan skills directory
        skills_dir = path / "skills"
        if skills_dir.exists():
            for item in skills_dir.iterdir():
                if item.is_dir() or (item.is_file() and item.suffix == ".md"):
                    skills.append(item.stem if item.is_file() else item.name)

        # Scan agents directory
        agents_dir = path / "agents"
        if agents_dir.exists():
            for item in agents_dir.iterdir():
                if item.suffix == ".md":
                    agents.append(item.stem)

        # Scan hooks
        hooks_json = path / "hooks" / "hooks.json"
        if hooks_json.exists():
            hooks_data = json.loads(hooks_json.read_text())
            if isinstance(hooks_data, list):
                hooks = [h.get("name", f"hook-{i}") for i, h in enumerate(hooks_data)]

        # Scan MCP configs
        mcp_json = path / ".mcp.json"
        if mcp_json.exists():
            mcp_data = json.loads(mcp_json.read_text())
            if "mcpServers" in mcp_data:
                mcps = list(mcp_data["mcpServers"].keys())

        return Extensions(skills=skills, agents=agents, hooks=hooks, mcps=mcps)
