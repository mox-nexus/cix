"""Embedding adapters."""

from memex.adapters._out.embedding.local import LocalEmbedder
from memex.adapters._out.embedding.nomic import NomicEmbedder

__all__ = ["LocalEmbedder", "NomicEmbedder"]
