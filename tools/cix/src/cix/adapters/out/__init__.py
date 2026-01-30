"""Driven adapters - implementations of port interfaces."""

from cix.adapters.out.claude_code_target import ClaudeCodeTargetAdapter
from cix.adapters.out.filesystem_registry import FilesystemRegistryAdapter
from cix.adapters.out.git_repository import GitSourceAdapter

__all__ = [
    "FilesystemRegistryAdapter",
    "GitSourceAdapter",
    "ClaudeCodeTargetAdapter",
]
