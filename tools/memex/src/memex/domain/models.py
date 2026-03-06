"""Domain models for memex.

Pure Pydantic models with no infrastructure dependencies.
Fragment is THE canonical entity (Karman recommendation).
"""

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class EmbeddingConfig(BaseModel):
    """Captures the embedding contract for a corpus.

    Domain invariant: fragments stored with one embedding model
    cannot be semantically searched with another. Dimensions must match.
    """

    model_name: str
    dimensions: int


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


# --- Typed return models (Step 0: eliminate -> dict from ports) ---


class CorpusStats(BaseModel):
    """Corpus-level statistics."""

    total_fragments: int
    conversations: int
    earliest: datetime | None = None
    latest: datetime | None = None
    sources: int


class ConversationSummary(BaseModel):
    """Summary of a conversation for listing."""

    conversation_id: str
    message_count: int
    first_timestamp: datetime | None = None
    last_timestamp: datetime | None = None
    source_kind: str | None = None
    preview: str | None = None


class ColumnInfo(BaseModel):
    """Schema column metadata."""

    name: str
    type: str
    nullable: bool


class SchemaInfo(BaseModel):
    """Corpus schema for introspection."""

    fragments: list[ColumnInfo]


class EdgeTypeStats(BaseModel):
    """Statistics for a single edge type."""

    count: int
    avg_weight: float


class EmbeddingCoverage(BaseModel):
    """Embedding coverage statistics."""

    with_embeddings: int
    total: int


class TrailSummary(BaseModel):
    """Summary of a trail for listing."""

    id: str
    name: str
    description: str
    created_at: datetime | None = None
    entry_count: int
