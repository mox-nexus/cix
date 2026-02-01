"""Driven adapters - implementations of outbound ports (git, filesystem, targets)."""

from cix.adapters._out.claude_code_target import ClaudeCodeTargetAdapter
from cix.adapters._out.filesystem_registry import FilesystemRegistryAdapter
from cix.adapters._out.git_repository import GitSourceAdapter

__all__ = ["ClaudeCodeTargetAdapter", "FilesystemRegistryAdapter", "GitSourceAdapter"]
