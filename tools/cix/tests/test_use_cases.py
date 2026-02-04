"""Tests for application use cases."""

from pathlib import Path

import pytest
from cix.application.use_cases import (
    Cix,
    CixError,
    PackageNotFoundError,
    SourceNotFoundError,
)
from cix.domain.models import Extensions, Installation, Package, Source
from cix.domain.ports._out.registry import RegistryPort
from cix.domain.ports._out.repository import SourcePort
from cix.domain.ports._out.target import TargetPort

# =============================================================================
# In-Memory Test Adapters
# =============================================================================


class InMemoryRegistry(RegistryPort):
    """In-memory registry for testing."""

    def __init__(self):
        self._sources: dict[str, Source] = {}
        self._installations: dict[str, Installation] = {}

    def add_source(self, source: Source) -> None:
        self._sources[source.name] = source

    def get_source(self, name: str) -> Source | None:
        return self._sources.get(name)

    def list_sources(self) -> list[Source]:
        return list(self._sources.values())

    def remove_source(self, name: str) -> None:
        self._sources.pop(name, None)

    def get_default_source(self) -> Source | None:
        for src in self._sources.values():
            if src.default:
                return src
        return None

    def add_installation(self, installation: Installation) -> None:
        self._installations[installation.id] = installation

    def get_installation(self, id: str) -> Installation | None:
        return self._installations.get(id)

    def list_installations(self, target: str | None = None) -> list[Installation]:
        installs = list(self._installations.values())
        if target:
            installs = [i for i in installs if i.target == target]
        return installs

    def remove_installation(self, id: str) -> None:
        self._installations.pop(id, None)


class InMemorySource(SourcePort):
    """In-memory source adapter for testing."""

    def __init__(self, packages: dict[str, list[Package]] | None = None):
        self._packages = packages or {}
        self._commits: dict[str, str] = {}

    def fetch(self, source: Source) -> None:
        # No-op for in-memory
        pass

    def list_packages(self, source: Source) -> list[Package]:
        return self._packages.get(source.name, [])

    def get_package(self, source: Source, name: str) -> Package | None:
        for pkg in self._packages.get(source.name, []):
            if pkg.name == name:
                return pkg
        return None

    def get_package_path(self, source: Source, package: Package) -> Path:
        return package.path

    def get_commit(self, source: Source) -> str:
        return self._commits.get(source.name, "test-commit-hash")


class InMemoryTarget(TargetPort):
    """In-memory target adapter for testing."""

    def __init__(self, available: bool = True):
        self._available = available
        self._installed: dict[str, Package] = {}

    def is_available(self) -> bool:
        return self._available

    def install(self, package: Package, source_path: Path) -> None:
        self._installed[package.name] = package

    def uninstall(self, package: Package) -> None:
        self._installed.pop(package.name, None)


# =============================================================================
# Tests
# =============================================================================


class TestSourceManagement:
    """Tests for source management operations."""

    @pytest.fixture
    def cix(self):
        """Create Cix instance with in-memory adapters."""
        return Cix(
            source_port=InMemorySource(),
            registry_port=InMemoryRegistry(),
            targets={"claude-code": InMemoryTarget()},
        )

    def test_add_source(self, cix):
        """Can add a new source."""
        src = cix.add_source("https://github.com/test/repo", name="test")
        assert src.name == "test"
        assert src.url == "https://github.com/test/repo"

    def test_add_source_derives_name(self, cix):
        """Name is derived from URL if not provided."""
        src = cix.add_source("https://github.com/owner/my-extensions")
        assert src.name == "my-extensions"

    def test_add_source_duplicate_fails(self, cix):
        """Adding duplicate source name fails."""
        cix.add_source("https://github.com/test/repo", name="test")
        with pytest.raises(CixError, match="already exists"):
            cix.add_source("https://github.com/other/repo", name="test")

    def test_add_source_as_default(self, cix):
        """Can set source as default."""
        src = cix.add_source("https://github.com/test/repo", set_default=True)
        assert src.default is True

    def test_list_sources_empty(self, cix):
        """List sources returns empty initially."""
        assert cix.list_sources() == []

    def test_list_sources_returns_all(self, cix):
        """List sources returns all registered sources."""
        cix.add_source("https://github.com/a/repo", name="a")
        cix.add_source("https://github.com/b/repo", name="b")
        sources = cix.list_sources()
        assert len(sources) == 2

    def test_remove_source(self, cix):
        """Can remove a source."""
        cix.add_source("https://github.com/test/repo", name="test")
        cix.remove_source("test")
        assert cix.list_sources() == []

    def test_remove_source_not_found(self, cix):
        """Removing non-existent source raises error."""
        with pytest.raises(SourceNotFoundError):
            cix.remove_source("nonexistent")


class TestPackageDiscovery:
    """Tests for package discovery operations."""

    @pytest.fixture
    def packages(self, tmp_path):
        """Sample packages."""
        pkg1 = Package(
            name="pkg1",
            description="Package 1",
            version="1.0.0",
            path=tmp_path / "pkg1",
            extensions=Extensions(skills=["skill1"]),
        )
        pkg2 = Package(
            name="pkg2",
            description="Package 2",
            version="2.0.0",
            path=tmp_path / "pkg2",
            extensions=Extensions(agents=["agent1"]),
        )
        return [pkg1, pkg2]

    @pytest.fixture
    def cix(self, packages):
        """Cix with pre-loaded packages."""
        source = InMemorySource(packages={"test-source": packages})
        registry = InMemoryRegistry()
        registry.add_source(Source(name="test-source", url="https://example.com", default=True))
        return Cix(
            source_port=source,
            registry_port=registry,
            targets={"claude-code": InMemoryTarget()},
        )

    def test_list_packages(self, cix, packages):
        """List packages returns all from default source."""
        result = cix.list_packages()
        assert len(result) == 2

    def test_list_packages_specific_source(self, cix, packages):
        """List packages from specific source."""
        result = cix.list_packages("test-source")
        assert len(result) == 2

    def test_list_packages_source_not_found(self, cix):
        """List packages from non-existent source raises error."""
        with pytest.raises(SourceNotFoundError):
            cix.list_packages("nonexistent")

    def test_get_package(self, cix):
        """Get specific package by name."""
        pkg, src = cix.get_package("pkg1")
        assert pkg.name == "pkg1"
        assert src.name == "test-source"

    def test_get_package_not_found(self, cix):
        """Get non-existent package raises error."""
        with pytest.raises(PackageNotFoundError):
            cix.get_package("nonexistent")


class TestInstallation:
    """Tests for package installation."""

    @pytest.fixture
    def packages(self, tmp_path):
        """Sample package."""
        pkg = Package(
            name="test-pkg",
            description="Test package",
            version="1.0.0",
            path=tmp_path / "test-pkg",
            extensions=Extensions(skills=["skill1"]),
        )
        (tmp_path / "test-pkg").mkdir()
        return [pkg]

    @pytest.fixture
    def cix(self, packages):
        """Cix with pre-loaded packages."""
        source = InMemorySource(packages={"test-source": packages})
        registry = InMemoryRegistry()
        registry.add_source(Source(name="test-source", url="https://example.com", default=True))
        return Cix(
            source_port=source,
            registry_port=registry,
            targets={"claude-code": InMemoryTarget()},
        )

    def test_install(self, cix):
        """Can install a package."""
        installation = cix.install("test-pkg")
        assert installation.package.name == "test-pkg"
        assert installation.target == "claude-code"
        assert installation.commit == "test-commit-hash"

    def test_install_from_specific_source(self, cix):
        """Can install using source/package format."""
        installation = cix.install("test-source/test-pkg")
        assert installation.package.name == "test-pkg"
        assert installation.source.name == "test-source"

    def test_list_installed(self, cix):
        """List installed packages."""
        cix.install("test-pkg")
        installed = cix.list_installed()
        assert len(installed) == 1
        assert installed[0].package.name == "test-pkg"

    def test_uninstall(self, cix):
        """Can uninstall a package."""
        cix.install("test-pkg")
        cix.uninstall("test-pkg")
        assert cix.list_installed() == []

    def test_uninstall_not_installed(self, cix):
        """Uninstalling non-installed package raises error."""
        with pytest.raises(PackageNotFoundError):
            cix.uninstall("nonexistent")


class TestTargets:
    """Tests for target management."""

    def test_get_targets(self):
        """Get available targets."""
        cix = Cix(
            source_port=InMemorySource(),
            registry_port=InMemoryRegistry(),
            targets={
                "claude-code": InMemoryTarget(available=True),
                "cursor": InMemoryTarget(available=False),
            },
        )
        targets = cix.get_targets()
        assert targets == {"claude-code": True, "cursor": False}
