"""Integration tests for ExcavationService with reranking."""

import tempfile
from pathlib import Path

import pytest
from memex.adapters._out.corpus.duckdb import DuckDBCorpus
from memex.adapters._out.reranking.fastembed_reranker import FastEmbedReranker
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
            corpus.rebuild_search_index()
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
            reranker=FastEmbedReranker(),
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
        assert name == "Xenova/ms-marco-MiniLM-L-6-v2"

    def test_reranker_model_name_none(self, service_no_reranker):
        """Service returns None when no reranker."""
        assert service_no_reranker.reranker_model_name() is None
