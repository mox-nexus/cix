"""Tests for DuckDB corpus adapter."""

import tempfile
from datetime import datetime
from pathlib import Path

import pytest
from memex.adapters._out.corpus.duckdb import DuckDBCorpus
from memex.domain.models import Fragment, Provenance


@pytest.fixture
def corpus():
    """In-memory-like corpus (temp file, auto-cleaned)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        c = DuckDBCorpus(Path(tmpdir) / "test.duckdb")
        yield c
        c.close()


@pytest.fixture
def corpus_with_embeddings():
    """Corpus with embedding column enabled."""
    with tempfile.TemporaryDirectory() as tmpdir:
        c = DuckDBCorpus(Path(tmpdir) / "test.duckdb", embedding_dim=3)
        yield c
        c.close()


def _make_fragment(
    id: str,
    content: str,
    conv_id: str = "conv-1",
    role: str = "assistant",
    source_kind: str = "claude_conversations",
    ts: datetime | None = None,
) -> Fragment:
    return Fragment(
        id=id,
        conversation_id=conv_id,
        role=role,
        content=content,
        provenance=Provenance(
            source_kind=source_kind,
            source_id=id,
            timestamp=ts or datetime(2025, 1, 1, 12, 0),
        ),
    )


class TestStore:
    def test_store_returns_count(self, corpus):
        frags = [_make_fragment("f1", "hello"), _make_fragment("f2", "world")]
        assert corpus.store(frags) == 2

    def test_store_deduplicates(self, corpus):
        frag = _make_fragment("f1", "hello")
        corpus.store([frag])
        assert corpus.store([frag]) == 0

    def test_store_empty(self, corpus):
        assert corpus.store([]) == 0


class TestSearch:
    @pytest.fixture(autouse=True)
    def _seed(self, corpus):
        self.corpus = corpus
        corpus.store(
            [
                _make_fragment("f1", "OAuth 2.0 is the recommended protocol"),
                _make_fragment("f2", "Rate limiting protects APIs from abuse"),
                _make_fragment("f3", "JWT tokens for session management", source_kind="openai"),
            ]
        )
        corpus.rebuild_search_index()

    def test_keyword_search_finds_matches(self):
        results = self.corpus.search("OAuth", limit=10)
        assert len(results) >= 1
        assert any("OAuth" in f.content for f in results)

    def test_keyword_search_empty_query(self):
        assert self.corpus.search("", limit=10) == []

    def test_keyword_search_no_matches(self):
        assert self.corpus.search("xyznonexistent", limit=10) == []

    def test_keyword_search_source_filter(self):
        results = self.corpus.search("tokens", limit=10, source_kind="openai")
        for f in results:
            assert f.source_kind == "openai"

    def test_keyword_search_respects_limit(self):
        results = self.corpus.search("the", limit=1)
        assert len(results) <= 1


class TestFindByConversation:
    def test_exact_match(self, corpus):
        corpus.store(
            [
                _make_fragment("f1", "hello", conv_id="conv-abc"),
                _make_fragment("f2", "world", conv_id="conv-xyz"),
            ]
        )
        results = corpus.find_by_conversation("conv-abc")
        assert len(results) == 1
        assert results[0].id == "f1"

    def test_prefix_match(self, corpus):
        corpus.store([_make_fragment("f1", "hello", conv_id="conv-abc-1234")])
        results = corpus.find_by_conversation("conv-abc")
        assert len(results) == 1

    def test_no_match(self, corpus):
        corpus.store([_make_fragment("f1", "hello", conv_id="conv-abc")])
        assert corpus.find_by_conversation("conv-zzz") == []


class TestListConversations:
    def test_lists_conversations(self, corpus):
        corpus.store(
            [
                _make_fragment("f1", "hello", conv_id="conv-1"),
                _make_fragment("f2", "world", conv_id="conv-1"),
                _make_fragment("f3", "other", conv_id="conv-2"),
            ]
        )
        convs = corpus.list_conversations()
        assert len(convs) == 2
        assert hasattr(convs[0], "conversation_id")
        assert hasattr(convs[0], "message_count")
        assert hasattr(convs[0], "preview")

    def test_respects_limit(self, corpus):
        for i in range(5):
            corpus.store([_make_fragment(f"f{i}", f"msg {i}", conv_id=f"conv-{i}")])
        assert len(corpus.list_conversations(limit=2)) == 2


class TestStats:
    def test_empty_corpus(self, corpus):
        stats = corpus.stats()
        assert stats.total_fragments == 0
        assert stats.conversations == 0

    def test_with_data(self, corpus):
        corpus.store(
            [
                _make_fragment("f1", "hello", conv_id="conv-1"),
                _make_fragment("f2", "world", conv_id="conv-2"),
            ]
        )
        stats = corpus.stats()
        assert stats.total_fragments == 2
        assert stats.conversations == 2


class TestSchema:
    def test_returns_schema(self, corpus):
        schema = corpus.schema()
        assert len(schema.fragments) > 0
        col_names = [c.name for c in schema.fragments]
        assert "id" in col_names
        assert "content" in col_names


class TestMeta:
    def test_set_and_get(self, corpus):
        corpus.set_meta("test_key", "test_value")
        assert corpus.get_meta("test_key") == "test_value"

    def test_get_missing(self, corpus):
        assert corpus.get_meta("nonexistent") is None

    def test_upsert(self, corpus):
        corpus.set_meta("key", "v1")
        corpus.set_meta("key", "v2")
        assert corpus.get_meta("key") == "v2"


class TestEdges:
    @pytest.fixture(autouse=True)
    def _seed(self, corpus):
        self.corpus = corpus
        corpus.store(
            [
                _make_fragment("f1", "first", conv_id="conv-1", ts=datetime(2025, 1, 1, 12, 0)),
                _make_fragment("f2", "second", conv_id="conv-1", ts=datetime(2025, 1, 1, 12, 1)),
                _make_fragment("f3", "third", conv_id="conv-1", ts=datetime(2025, 1, 1, 12, 2)),
            ]
        )

    def test_build_follows_edges(self):
        count = self.corpus.build_follows_edges()
        assert count == 2  # f1→f2, f2→f3

    def test_add_edge(self):
        self.corpus.add_edge("f1", "f3", "SIMILAR_TO", 0.9)
        edges = self.corpus.get_edges("f1", edge_type="SIMILAR_TO")
        assert len(edges) == 1
        assert edges[0]["target_id"] == "f3"

    def test_add_edges_batch(self):
        edges = [
            ("f1", "f2", "SIMILAR_TO", 0.9),
            ("f1", "f3", "SIMILAR_TO", 0.8),
        ]
        assert self.corpus.add_edges_batch(edges) == 2

    def test_edge_stats(self):
        self.corpus.build_follows_edges()
        stats = self.corpus.edge_stats()
        assert "FOLLOWS" in stats
        assert stats["FOLLOWS"].count == 2

    def test_traverse_single_hop(self):
        self.corpus.build_follows_edges()
        results = self.corpus.traverse("f1", max_hops=1)
        assert len(results) == 1
        frag, hops, edge_type = results[0]
        assert frag.id == "f2"
        assert hops == 1
        assert edge_type == "FOLLOWS"

    def test_traverse_multi_hop(self):
        self.corpus.build_follows_edges()
        results = self.corpus.traverse("f1", max_hops=2)
        ids = {r[0].id for r in results}
        assert ids == {"f2", "f3"}

    def test_traverse_with_edge_type_filter(self):
        self.corpus.build_follows_edges()
        self.corpus.add_edge("f1", "f3", "SIMILAR_TO", 0.9)
        results = self.corpus.traverse("f1", max_hops=1, edge_type="SIMILAR_TO")
        assert len(results) == 1
        assert results[0][0].id == "f3"

    def test_traverse_no_edges(self):
        results = self.corpus.traverse("f1", max_hops=2)
        assert results == []


class TestTrails:
    @pytest.fixture(autouse=True)
    def _seed(self, corpus):
        self.corpus = corpus
        corpus.store(
            [
                _make_fragment("f1", "first"),
                _make_fragment("f2", "second"),
            ]
        )

    def test_create_and_list(self):
        self.corpus.create_trail("my trail", "a test trail")
        trails = self.corpus.list_trails()
        assert len(trails) == 1
        assert trails[0].name == "my trail"

    def test_add_and_follow(self):
        self.corpus.create_trail("my trail")
        self.corpus.add_to_trail("my trail", "f1", "first note")
        self.corpus.add_to_trail("my trail", "f2", "second note")

        entries = self.corpus.get_trail("my trail")
        assert len(entries) == 2
        assert entries[0][0].id == "f1"
        assert entries[0][1] == "first note"
        assert entries[1][0].id == "f2"

    def test_delete_trail(self):
        self.corpus.create_trail("my trail")
        assert self.corpus.delete_trail("my trail") is True
        assert self.corpus.list_trails() == []

    def test_delete_nonexistent(self):
        assert self.corpus.delete_trail("nope") is False

    def test_get_nonexistent_trail(self):
        assert self.corpus.get_trail("nope") == []

    def test_add_to_nonexistent_trail_raises(self):
        with pytest.raises(ValueError, match="not found"):
            self.corpus.add_to_trail("nope", "f1")


class TestEmbeddings:
    def test_embedding_dimensions_none_without_column(self, corpus):
        assert corpus.embedding_dimensions() is None

    def test_embedding_dimensions_with_column(self, corpus_with_embeddings):
        dims = corpus_with_embeddings.embedding_dimensions()
        assert dims == 3

    def test_count_without_embeddings(self, corpus_with_embeddings):
        corpus_with_embeddings.store([_make_fragment("f1", "hello")])
        assert corpus_with_embeddings.count_without_embeddings() == 1

    def test_has_semantic_search_without_dim(self, corpus):
        assert corpus.has_semantic_search() is False

    def test_store_with_embeddings(self, corpus_with_embeddings):
        frags = [_make_fragment("f1", "hello"), _make_fragment("f2", "world")]
        stored = corpus_with_embeddings.store_with_embeddings(frags, lambda text: [0.1, 0.2, 0.3])
        assert stored == 2
        assert corpus_with_embeddings.count_without_embeddings() == 0

    def test_store_with_embeddings_requires_dim(self, corpus):
        with pytest.raises(ValueError, match="embedding support"):
            corpus.store_with_embeddings([_make_fragment("f1", "hi")], lambda t: [0.1])


class TestSql:
    def test_raw_query(self, corpus):
        corpus.store([_make_fragment("f1", "hello")])
        rows = corpus.query_sql("SELECT COUNT(*) FROM fragments")
        assert rows[0][0] == 1
