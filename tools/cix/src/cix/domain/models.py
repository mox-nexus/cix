"""
Domain models for Collaborative Intelligence Extensions.

These models represent the core concepts of the cix ecosystem:
- Source: Where packages come from (extension marketplaces)
- Package: The installable unit containing extensions
- Extension: Individual cognitive extension (skill, agent, hook, mcp)
- Installation: Record of an installed package

Design principle: No external dependencies. These are pure domain objects.
"""

from datetime import datetime
from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, Field


class ExtensionKind(StrEnum):
    """
    Types of cognitive extensions.

    Each kind serves a distinct purpose in the collaborative intelligence model:
    - SKILL: Decision frameworks and methodology (teaches HOW to think)
    - AGENT: Specialized subagents for delegation (offers perspective)
    - HOOK: Event-triggered behaviors (augments workflow)
    - MCP: Model Context Protocol integrations (bridges systems)
    """

    SKILL = "skill"
    AGENT = "agent"
    HOOK = "hook"
    MCP = "mcp"


class Extension(BaseModel):
    """
    A single cognitive extension.

    Extensions are the atomic units of collaborative intelligence.
    Each extension should:
    - Have a single, clear purpose (orthogonality)
    - Enhance capability without creating dependency
    - Make reasoning transparent
    """

    name: str
    kind: ExtensionKind
    description: str = ""
    path: Path | None = None

    @property
    def display_name(self) -> str:
        """Human-readable name with kind indicator."""
        return f"{self.name} [{self.kind.value}]"


class Extensions(BaseModel):
    """
    Collection of extensions within a package.

    Packages bundle related extensions that work together
    while maintaining orthogonality - no overlapping concerns.
    """

    skills: list[str] = Field(default_factory=list)
    agents: list[str] = Field(default_factory=list)
    hooks: list[str] = Field(default_factory=list)
    mcps: list[str] = Field(default_factory=list)

    @property
    def total(self) -> int:
        """Total number of extensions."""
        return len(self.skills) + len(self.agents) + len(self.hooks) + len(self.mcps)

    @property
    def is_empty(self) -> bool:
        """Whether this package has any extensions."""
        return self.total == 0

    @property
    def summary(self) -> str:
        """Human-readable summary of extensions."""
        parts = []
        if self.skills:
            parts.append(f"{len(self.skills)} skill{'s' if len(self.skills) > 1 else ''}")
        if self.agents:
            parts.append(f"{len(self.agents)} agent{'s' if len(self.agents) > 1 else ''}")
        if self.hooks:
            parts.append(f"{len(self.hooks)} hook{'s' if len(self.hooks) > 1 else ''}")
        if self.mcps:
            parts.append(f"{len(self.mcps)} mcp{'s' if len(self.mcps) > 1 else ''}")
        return ", ".join(parts) if parts else "empty"


class Source(BaseModel):
    """
    A source of packages (extension marketplace).

    Sources are git repositories containing one or more packages.
    The default source is used when no source is specified in commands.
    """

    name: str
    url: str
    default: bool = False
    ref: str | None = None  # Git ref for pinning (branch, tag, commit)

    @property
    def is_pinned(self) -> bool:
        """Whether this source is pinned to a specific ref."""
        return self.ref is not None


class Package(BaseModel):
    """
    An installable package containing extensions.

    Packages are the unit of distribution. Each package:
    - Has a unique name within its source
    - Contains one or more extensions
    - Is versioned for reproducibility
    """

    name: str
    description: str
    version: str
    path: Path
    extensions: Extensions = Field(default_factory=Extensions)

    # Package metadata (optional)
    author: str | None = None
    license: str | None = None

    @property
    def qualified_name(self) -> str:
        """Full name including version."""
        return f"{self.name}@{self.version}"


class Installation(BaseModel):
    """
    Record of an installed package.

    Tracks what was installed, where it came from, and when.
    The commit hash enables reproducible installations.
    """

    package: Package
    source: Source
    installed_at: datetime = Field(default_factory=datetime.now)
    commit: str  # Git commit hash for reproducibility
    target: str = "claude-code"  # Installation target

    @property
    def id(self) -> str:
        """Unique identifier: source/package."""
        return f"{self.source.name}/{self.package.name}"

    @property
    def age_days(self) -> int:
        """Days since installation."""
        delta = datetime.now() - self.installed_at
        return delta.days
