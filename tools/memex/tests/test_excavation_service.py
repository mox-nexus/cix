"""Integration tests for ExcavationService with reranking."""

import tempfile
from pathlib import Path

import pytest
from memex.adapters._out.corpus.duckdb import DuckDBCorpus
from memex.adapters._out.reranking.cross_encoder import CrossEncoderReranker
from memex.domain.models import Fragment
from memex.domain.services import ExcavationService


class TestExcavationServiceReranking:
    """Integration tests for hybrid search with reranking."""

    @pytest.fixture
    def temp_corpus(self, sample_fragments):
        """Create a temporary corpus with sample data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            corpus_path = Path(tmpdir) / "test.duckdb"
            corpus = DuckDBCorpus(corpus_path)
            corpus.store(sample_fragments)
            corpus.rebuild_fts_index()
            yield corpus
            corpus.close()

    @pytest.fixture
    def service_no_reranker(self, temp_corpus):
        """Service without reranker."""
        return ExcavationService(
            corpus=temp_corpus,
            source_adapters=[],
            embedder=None,
            reranker=None,
        )

    @pytest.fixture
    def service_with_reranker(self, temp_corpus):
        """Service with reranker."""
        return ExcavationService(
            corpus=temp_corpus,
            source_adapters=[],
            embedder=None,
            reranker=CrossEncoderReranker(),
        )

    def test_hybrid_search_without_reranker(self, service_no_reranker):
        """Hybrid search without reranker returns RRF-scored results."""
        results = service_no_reranker.hybrid_search("authentication")

        assert len(results) > 0
        for frag, score in results:
            assert isinstance(frag, Fragment)
            assert isinstance(score, float)

    def test_hybrid_search_with_reranker(self, service_with_reranker):
        """Hybrid search with reranker applies cross-encoder scoring."""
        results = service_with_reranker.hybrid_search("authentication")

        assert len(results) > 0
        # Reranker should boost auth-related content
        top_frag = results[0][0]
        assert "auth" in top_frag.content.lower() or "oauth" in top_frag.content.lower()

    def test_hybrid_search_reranker_disabled(self, service_with_reranker):
        """Can disable reranker with use_reranker=False."""
        results = service_with_reranker.hybrid_search(
            "authentication",
            use_reranker=False,
        )

        assert len(results) > 0
        # Still returns results, just without reranking

    def test_has_reranker_true(self, service_with_reranker):
        """Service reports reranker availability."""
        assert service_with_reranker.has_reranker() is True

    def test_has_reranker_false(self, service_no_reranker):
        """Service reports reranker not available."""
        assert service_no_reranker.has_reranker() is False

    def test_reranker_model_name(self, service_with_reranker):
        """Service exposes reranker model name."""
        name = service_with_reranker.reranker_model_name()
        assert name == "cross-encoder/ms-marco-MiniLM-L-6-v2"

    def test_reranker_model_name_none(self, service_no_reranker):
        """Service returns None when no reranker."""
        assert service_no_reranker.reranker_model_name() is None


class TestExcavationServiceKeywordSearch:
    """Tests for keyword search (baseline without embeddings)."""

    @pytest.fixture
    def temp_corpus(self, sample_fragments):
        """Create a temporary corpus with sample data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            corpus_path = Path(tmpdir) / "test.duckdb"
            corpus = DuckDBCorpus(corpus_path)
            corpus.store(sample_fragments)
            # Rebuild FTS index after store
            corpus.rebuild_fts_index()
            yield corpus
            corpus.close()

    @pytest.fixture
    def service(self, temp_corpus):
        """Service for keyword search."""
        return ExcavationService(
            corpus=temp_corpus,
            source_adapters=[],
        )

    def test_keyword_search_finds_matches(self, service):
        """Keyword search finds fragments containing query terms."""
        results = service.keyword_search("authentication")

        assert len(results) > 0
        for frag in results:
            assert isinstance(frag, Fragment)

    def test_keyword_search_no_matches(self, service):
        """Keyword search returns empty for no matches."""
        results = service.keyword_search("xyznonexistentterm")
        assert results == []

    def test_keyword_search_respects_limit(self, service):
        """Keyword search respects limit parameter."""
        results = service.keyword_search("the", limit=2)
        assert len(results) <= 2

    def test_keyword_search_source_filter(self, service):
        """Keyword search filters by source_kind."""
        results = service.keyword_search("API", source_kind="openai")

        for frag in results:
            assert frag.source_kind == "openai"
