"""Tests for domain models."""

from datetime import datetime

from memex.domain.models import (
    Completeness,
    EmbeddingConfig,
    Fragment,
    Provenance,
)


class TestFragment:
    def test_timestamp_from_provenance(self):
        ts = datetime(2025, 1, 1, 12, 0)
        frag = Fragment(
            id="f1",
            conversation_id="conv-1",
            role="user",
            content="hello",
            provenance=Provenance(
                source_kind="claude_conversations",
                source_id="msg-1",
                timestamp=ts,
            ),
        )
        assert frag.timestamp == ts

    def test_source_kind_from_provenance(self):
        frag = Fragment(
            id="f1",
            role="user",
            content="hello",
            provenance=Provenance(
                source_kind="openai",
                source_id="msg-1",
            ),
        )
        assert frag.source_kind == "openai"

    def test_optional_conversation_id(self):
        frag = Fragment(
            id="f1",
            role="user",
            content="hello",
            provenance=Provenance(source_kind="custom", source_id="x"),
        )
        assert frag.conversation_id is None

    def test_optional_timestamp(self):
        frag = Fragment(
            id="f1",
            role="user",
            content="hello",
            provenance=Provenance(source_kind="custom", source_id="x"),
        )
        assert frag.timestamp is None


class TestProvenance:
    def test_defaults(self):
        p = Provenance(source_kind="custom", source_id="x")
        assert p.retrieval_method == "export"
        assert p.completeness == Completeness.FULL
        assert p.timestamp is None


class TestEmbeddingConfig:
    def test_creation(self):
        config = EmbeddingConfig(model_name="nomic-v1.5", dimensions=768)
        assert config.model_name == "nomic-v1.5"
        assert config.dimensions == 768


class TestCompleteness:
    def test_enum_values(self):
        assert Completeness.FULL == "full"
        assert Completeness.TRUNCATED == "truncated"
        assert Completeness.PARTIAL == "partial"
