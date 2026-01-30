"""
Filesystem registry adapter - JSON-based state persistence.

Simple, debuggable, no external dependencies. State is stored in:
- ~/.cix/sources.json
- ~/.cix/installations.json
"""

import json
from datetime import datetime
from pathlib import Path

from cix.domain.models import Extensions, Installation, Package, Source


class FilesystemRegistryAdapter:
    """
    Registry implementation using JSON files.

    State location: ~/.cix/ (or configured directory)
    """

    def __init__(self, config_dir: Path | None = None) -> None:
        self._config_dir = config_dir or Path.home() / ".cix"
        self._config_dir.mkdir(parents=True, exist_ok=True)

        self._sources_file = self._config_dir / "sources.json"
        self._installations_file = self._config_dir / "installations.json"

    # =========================================================================
    # Source Management
    # =========================================================================

    def list_sources(self) -> list[Source]:
        """List all registered sources."""
        data = self._load_sources()
        return [Source(**s) for s in data.get("sources", [])]

    def add_source(self, source: Source) -> None:
        """Register a new source."""
        data = self._load_sources()
        sources = data.get("sources", [])

        # Check for duplicate
        for s in sources:
            if s["name"] == source.name:
                raise ValueError(f"Source '{source.name}' already exists")

        sources.append(source.model_dump())
        data["sources"] = sources
        self._save_sources(data)

    def remove_source(self, name: str) -> None:
        """Unregister a source."""
        data = self._load_sources()
        sources = data.get("sources", [])

        original_len = len(sources)
        sources = [s for s in sources if s["name"] != name]

        if len(sources) == original_len:
            raise ValueError(f"Source '{name}' not found")

        data["sources"] = sources
        self._save_sources(data)

    def get_source(self, name: str) -> Source | None:
        """Get a source by name."""
        for source in self.list_sources():
            if source.name == name:
                return source
        return None

    def get_default_source(self) -> Source | None:
        """Get the default source."""
        for source in self.list_sources():
            if source.default:
                return source
        return None

    def set_default_source(self, name: str) -> None:
        """Set a source as the default."""
        data = self._load_sources()
        sources = data.get("sources", [])

        found = False
        for s in sources:
            if s["name"] == name:
                s["default"] = True
                found = True
            else:
                s["default"] = False

        if not found:
            raise ValueError(f"Source '{name}' not found")

        data["sources"] = sources
        self._save_sources(data)

    # =========================================================================
    # Installation Management
    # =========================================================================

    def list_installations(self, target: str | None = None) -> list[Installation]:
        """List all installations, optionally filtered by target."""
        data = self._load_installations()
        installations = []

        for inst in data.get("installations", []):
            installation = self._deserialize_installation(inst)
            if target is None or installation.target == target:
                installations.append(installation)

        return installations

    def add_installation(self, installation: Installation) -> None:
        """Record a new installation."""
        data = self._load_installations()
        installations = data.get("installations", [])

        # Remove existing if present (update scenario)
        installations = [i for i in installations if i.get("id") != installation.id]

        installations.append(self._serialize_installation(installation))
        data["installations"] = installations
        self._save_installations(data)

    def remove_installation(self, installation_id: str) -> None:
        """Remove an installation record."""
        data = self._load_installations()
        installations = data.get("installations", [])

        original_len = len(installations)
        installations = [i for i in installations if i.get("id") != installation_id]

        if len(installations) == original_len:
            raise ValueError(f"Installation '{installation_id}' not found")

        data["installations"] = installations
        self._save_installations(data)

    def get_installation(self, installation_id: str) -> Installation | None:
        """Get an installation by ID."""
        for installation in self.list_installations():
            if installation.id == installation_id:
                return installation
        return None

    # =========================================================================
    # Private Helpers
    # =========================================================================

    def _load_sources(self) -> dict:
        """Load sources from file."""
        if not self._sources_file.exists():
            return {"sources": []}
        return json.loads(self._sources_file.read_text())

    def _save_sources(self, data: dict) -> None:
        """Save sources to file."""
        self._sources_file.write_text(json.dumps(data, indent=2))

    def _load_installations(self) -> dict:
        """Load installations from file."""
        if not self._installations_file.exists():
            return {"installations": []}
        return json.loads(self._installations_file.read_text())

    def _save_installations(self, data: dict) -> None:
        """Save installations to file."""
        self._installations_file.write_text(json.dumps(data, indent=2, default=str))

    def _serialize_installation(self, installation: Installation) -> dict:
        """Serialize an installation for storage."""
        return {
            "id": installation.id,
            "package": {
                "name": installation.package.name,
                "description": installation.package.description,
                "version": installation.package.version,
                "path": str(installation.package.path),
                "extensions": installation.package.extensions.model_dump(),
            },
            "source": installation.source.model_dump(),
            "installed_at": installation.installed_at.isoformat(),
            "commit": installation.commit,
            "target": installation.target,
        }

    def _deserialize_installation(self, data: dict) -> Installation:
        """Deserialize an installation from storage."""
        package_data = data["package"]
        return Installation(
            package=Package(
                name=package_data["name"],
                description=package_data["description"],
                version=package_data["version"],
                path=Path(package_data["path"]),
                extensions=Extensions(**package_data.get("extensions", {})),
            ),
            source=Source(**data["source"]),
            installed_at=datetime.fromisoformat(data["installed_at"]),
            commit=data["commit"],
            target=data["target"],
        )
