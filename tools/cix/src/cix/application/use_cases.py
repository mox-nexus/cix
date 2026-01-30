"""
Use cases for cix - orchestrating domain operations through ports.

The Cix class is the application facade, providing high-level operations
that coordinate between domain models and port implementations.

Design principle: This layer knows about ports (interfaces) but not
about specific adapters (implementations). Dependency injection
enables testing and flexibility.
"""

from datetime import datetime

from cix.domain.models import Installation, Package, Source
from cix.ports.out.registry import RegistryPort
from cix.ports.out.repository import SourcePort
from cix.ports.out.target import TargetPort


class CixError(Exception):
    """Base exception for cix operations."""

    pass


class SourceNotFoundError(CixError):
    """Raised when a referenced source doesn't exist."""

    pass


class PackageNotFoundError(CixError):
    """Raised when a referenced package doesn't exist."""

    pass


class InstallationError(CixError):
    """Raised when installation fails."""

    pass


class Cix:
    """
    Application facade for Collaborative Intelligence Extensions.

    Orchestrates all cix operations through port interfaces.
    Instantiate with specific adapters via composition root.
    """

    def __init__(
        self,
        source_port: SourcePort,
        registry_port: RegistryPort,
        targets: dict[str, TargetPort],
    ) -> None:
        self._source = source_port
        self._registry = registry_port
        self._targets = targets

    # =========================================================================
    # Source Management
    # =========================================================================

    def add_source(
        self,
        url: str,
        name: str | None = None,
        set_default: bool = False,
    ) -> Source:
        """
        Register a new source (extension marketplace).

        Args:
            url: Git repository URL
            name: Source name (derived from URL if not provided)
            set_default: Whether to make this the default source

        Returns:
            The created Source

        Raises:
            CixError: If name already exists or URL is invalid
        """
        # Derive name from URL if not provided
        if name is None:
            # Extract repo name from URL
            name = url.rstrip("/").split("/")[-1]
            if name.endswith(".git"):
                name = name[:-4]

        # Check for duplicates
        if self._registry.get_source(name) is not None:
            raise CixError(f"Source '{name}' already exists")

        # Create and register
        source = Source(name=name, url=url, default=set_default)

        # If setting as default, unset any existing default
        if set_default:
            for existing in self._registry.list_sources():
                if existing.default:
                    self._registry.remove_source(existing.name)
                    self._registry.add_source(
                        Source(name=existing.name, url=existing.url, default=False)
                    )

        self._registry.add_source(source)

        # Fetch initial content
        self._source.fetch(source)

        return source

    def remove_source(self, name: str) -> None:
        """
        Unregister a source.

        Args:
            name: Source name to remove

        Raises:
            SourceNotFoundError: If source doesn't exist
        """
        if self._registry.get_source(name) is None:
            raise SourceNotFoundError(f"Source '{name}' not found")

        self._registry.remove_source(name)

    def list_sources(self) -> list[Source]:
        """List all registered sources."""
        return self._registry.list_sources()

    def refresh_source(self, name: str | None = None) -> list[Source]:
        """
        Fetch latest content from source(s).

        Args:
            name: Specific source to refresh, or all if None

        Returns:
            List of refreshed sources
        """
        if name is not None:
            source = self._registry.get_source(name)
            if source is None:
                raise SourceNotFoundError(f"Source '{name}' not found")
            sources = [source]
        else:
            sources = self._registry.list_sources()

        for source in sources:
            self._source.fetch(source)

        return sources

    # =========================================================================
    # Package Discovery
    # =========================================================================

    def list_packages(self, source_name: str | None = None) -> list[Package]:
        """
        List available packages from source(s).

        Args:
            source_name: Specific source, or default/all if None

        Returns:
            List of available packages
        """
        if source_name is not None:
            source = self._registry.get_source(source_name)
            if source is None:
                raise SourceNotFoundError(f"Source '{source_name}' not found")
            sources = [source]
        else:
            # Use default source if set, otherwise all sources
            default = self._registry.get_default_source()
            sources = [default] if default else self._registry.list_sources()

        packages = []
        for source in sources:
            packages.extend(self._source.list_packages(source))

        return packages

    def get_package(self, package_ref: str) -> tuple[Package, Source]:
        """
        Get a specific package by reference.

        Args:
            package_ref: Either "package" (uses default source) or "source/package"

        Returns:
            Tuple of (Package, Source)

        Raises:
            PackageNotFoundError: If package doesn't exist
        """
        source, package_name = self._parse_package_ref(package_ref)
        package = self._source.get_package(source, package_name)

        if package is None:
            raise PackageNotFoundError(
                f"Package '{package_name}' not found in source '{source.name}'"
            )

        return package, source

    # =========================================================================
    # Installation Management
    # =========================================================================

    def install(
        self,
        package_ref: str,
        target: str = "claude-code",
        pin_commit: bool = True,
    ) -> Installation:
        """
        Install a package to a target.

        Args:
            package_ref: Package reference (name or source/name)
            target: Installation target (e.g., 'claude-code')
            pin_commit: Whether to pin to current commit

        Returns:
            Installation record

        Raises:
            InstallationError: If installation fails
        """
        if target not in self._targets:
            raise InstallationError(f"Unknown target: {target}")

        target_port = self._targets[target]
        if not target_port.is_available():
            raise InstallationError(f"Target '{target}' is not available on this system")

        # Get package and source
        package, source = self.get_package(package_ref)

        # Get source path and commit
        source_path = self._source.get_package_path(source, package)
        commit = self._source.get_commit(source) if pin_commit else ""

        # Install to target
        target_port.install(package, source_path)

        # Record installation
        installation = Installation(
            package=package,
            source=source,
            installed_at=datetime.now(),
            commit=commit,
            target=target,
        )
        self._registry.add_installation(installation)

        return installation

    def uninstall(self, package_ref: str) -> None:
        """
        Remove an installed package.

        Args:
            package_ref: Package reference (name or source/name)

        Raises:
            PackageNotFoundError: If not installed
        """
        # Find installation
        installation = self._find_installation(package_ref)
        if installation is None:
            raise PackageNotFoundError(f"Package '{package_ref}' is not installed")

        # Uninstall from target
        target_port = self._targets.get(installation.target)
        if target_port:
            target_port.uninstall(installation.package)

        # Remove record
        self._registry.remove_installation(installation.id)

    def update(self, package_ref: str | None = None) -> list[Installation]:
        """
        Update installed package(s) to latest version.

        Args:
            package_ref: Specific package, or all if None

        Returns:
            List of updated installations
        """
        if package_ref is not None:
            installation = self._find_installation(package_ref)
            if installation is None:
                raise PackageNotFoundError(f"Package '{package_ref}' is not installed")
            installations = [installation]
        else:
            installations = self._registry.list_installations()

        updated = []
        for installation in installations:
            # Refresh source
            self._source.fetch(installation.source)

            # Reinstall
            target_port = self._targets.get(installation.target)
            if target_port:
                source_path = self._source.get_package_path(
                    installation.source, installation.package
                )
                target_port.install(installation.package, source_path)

                # Update installation record with new commit
                new_commit = self._source.get_commit(installation.source)
                new_installation = Installation(
                    package=installation.package,
                    source=installation.source,
                    installed_at=datetime.now(),
                    commit=new_commit,
                    target=installation.target,
                )
                self._registry.remove_installation(installation.id)
                self._registry.add_installation(new_installation)
                updated.append(new_installation)

        return updated

    def list_installed(self, target: str | None = None) -> list[Installation]:
        """List installed packages, optionally filtered by target."""
        return self._registry.list_installations(target)

    # =========================================================================
    # Introspection
    # =========================================================================

    def get_targets(self) -> dict[str, bool]:
        """Get available targets and their availability status."""
        return {name: target.is_available() for name, target in self._targets.items()}

    # =========================================================================
    # Private Helpers
    # =========================================================================

    def _parse_package_ref(self, package_ref: str) -> tuple[Source, str]:
        """
        Parse a package reference into (source, package_name).

        Handles:
        - "package" -> uses default source
        - "source/package" -> uses specified source
        """
        if "/" in package_ref:
            source_name, package_name = package_ref.split("/", 1)
            source = self._registry.get_source(source_name)
            if source is None:
                raise SourceNotFoundError(f"Source '{source_name}' not found")
        else:
            package_name = package_ref
            source = self._registry.get_default_source()
            if source is None:
                sources = self._registry.list_sources()
                if not sources:
                    msg = "No sources registered. Add one with 'cix source add'"
                    raise SourceNotFoundError(msg)
                source = sources[0]  # Use first source if no default

        return source, package_name

    def _find_installation(self, package_ref: str) -> Installation | None:
        """Find an installation by package reference."""
        # Try direct ID match
        if "/" in package_ref:
            return self._registry.get_installation(package_ref)

        # Search by package name
        for installation in self._registry.list_installations():
            if installation.package.name == package_ref:
                return installation

        return None
