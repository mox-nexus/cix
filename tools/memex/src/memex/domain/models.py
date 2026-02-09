"""Domain models for memex.

Pure Pydantic models with no infrastructure dependencies.
Fragment is THE canonical entity (Karman recommendation).
"""

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel

# SourceKind as string type for extensibility (Ace recommendation)
# Third-party adapters can use any string, not limited to enum
SourceKind = str


class EmbeddingConfig(BaseModel):
    """Captures the embedding contract for a corpus.

    Domain invariant: fragments stored with one embedding model
    cannot be semantically searched with another. Dimensions must match.
    """

    model_name: str
    dimensions: int

    def is_compatible_with(self, other: "EmbeddingConfig") -> bool:
        """Check if two embedding configs are compatible."""
        return self.dimensions == other.dimensions


# Common source kinds (not exhaustive)
SOURCE_CLAUDE_CONVERSATIONS = "claude_conversations"
SOURCE_OPENAI = "openai"
SOURCE_GEMINI = "gemini"
SOURCE_CUSTOM = "custom"


class Completeness(StrEnum):
    """Fragment completeness."""

    FULL = "full"
    TRUNCATED = "truncated"
    PARTIAL = "partial"


class Provenance(BaseModel):
    """Source-agnostic origin tracking."""

    source_kind: str  # Extensible string, not enum
    source_id: str
    timestamp: datetime | None = None
    retrieval_method: str = "export"
    completeness: Completeness = Completeness.FULL


class Fragment(BaseModel):
    """A recovered unit of collaborative intelligence.

    This is THE canonical domain entity (Karman).
    All adapters produce Fragments, not DataFrames.
    """

    id: str
    conversation_id: str | None = None
    role: str
    content: str
    provenance: Provenance

    @property
    def timestamp(self) -> datetime | None:
        return self.provenance.timestamp

    @property
    def source_kind(self) -> str:
        return self.provenance.source_kind
