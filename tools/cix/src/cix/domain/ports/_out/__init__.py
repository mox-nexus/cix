"""Driven ports - interfaces the domain requires (database, git, targets)."""

from cix.domain.ports._out.registry import RegistryPort
from cix.domain.ports._out.repository import SourcePort
from cix.domain.ports._out.target import TargetPort

__all__ = ["RegistryPort", "SourcePort", "TargetPort"]
