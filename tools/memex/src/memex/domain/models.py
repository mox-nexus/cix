"""Domain models for memex.

Pure Pydantic models with no infrastructure dependencies.
Fragment is THE canonical entity (Karman recommendation).
"""

from datetime import datetime
from enum import StrEnum
from typing import Any, NamedTuple

from pydantic import BaseModel


class IngestResult(NamedTuple):
    """Result of ingesting a file into the corpus."""

    parsed: int
    stored: int


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
SOURCE_PLAINTEXT = "plaintext"
SOURCE_GEMINI = "gemini"
SOURCE_CUSTOM = "custom"


class Completeness(StrEnum):
    """Fragment completeness.

    FULL: Complete content as exported.
    TRUNCATED: Content was cut by export/API limits (e.g., max tokens).
    PARTIAL: Content was intentionally sampled or summarized.
    """

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
    metadata: dict[str, Any] | None = None

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


class FieldInfo(BaseModel):
    """Fragment field metadata."""

    name: str
    type: str
    nullable: bool


class FragmentSchema(BaseModel):
    """Fragment schema for introspection."""

    fragments: list[FieldInfo]


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
