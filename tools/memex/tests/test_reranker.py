"""Tests for cross-encoder reranker."""

import numpy as np
import pytest
from memex.adapters._out.reranking.cross_encoder import CrossEncoderReranker
from memex.domain.models import Fragment


class TestCrossEncoderReranker:
    """Unit tests for CrossEncoderReranker."""

    @pytest.fixture
    def reranker(self):
        """Create reranker instance (model loaded lazily)."""
        return CrossEncoderReranker()

    def test_model_name_default(self, reranker):
        """Should use default MS MARCO model."""
        assert reranker.model_name == "cross-encoder/ms-marco-MiniLM-L-6-v2"

    def test_model_name_custom(self):
        """Should allow custom model name."""
        custom = CrossEncoderReranker("custom/model-name")
        assert custom.model_name == "custom/model-name"

    def test_rerank_empty_candidates(self, reranker):
        """Should return empty list for empty candidates."""
        result = reranker.rerank("query", [])
        assert result == []

    def test_rerank_returns_scored_fragments(self, reranker, sample_fragments):
        """Should return list of (Fragment, score) tuples."""
        result = reranker.rerank("authentication", sample_fragments)

        assert len(result) > 0
        for frag, score in result:
            assert isinstance(frag, Fragment)
            assert isinstance(score, (int, float, np.floating))

    def test_rerank_respects_top_k(self, reranker, sample_fragments):
        """Should return at most top_k results."""
        result = reranker.rerank("auth", sample_fragments, top_k=2)
        assert len(result) <= 2

    def test_rerank_sorted_descending(self, reranker, sample_fragments):
        """Should return results sorted by score descending."""
        result = reranker.rerank("authentication", sample_fragments, top_k=5)

        scores = [score for _, score in result]
        assert scores == sorted(scores, reverse=True)

    def test_rerank_relevance_ordering(self, reranker, sample_fragments):
        """Authentication query should rank auth-related content higher."""
        result = reranker.rerank("OAuth authentication tokens", sample_fragments)

        # Top results should be about authentication, not rate limiting
        top_contents = [frag.content.lower() for frag, _ in result[:2]]
        assert any("auth" in c or "oauth" in c or "token" in c for c in top_contents)

    def test_model_lazy_loading(self):
        """Model should not load until first rerank call."""
        reranker = CrossEncoderReranker()

        # Before use, cached_property hasn't populated __dict__
        assert "model" not in reranker.__dict__

        # After access, cached_property stores in __dict__
        _ = reranker.model
        assert "model" in reranker.__dict__
