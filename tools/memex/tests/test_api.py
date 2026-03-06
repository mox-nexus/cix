"""Tests for public API facade."""

import json

import pytest
from memex.api import Memex
from memex.domain.models import ConversationSummary, CorpusStats, Fragment


@pytest.fixture
def corpus_path(tmp_path):
    return tmp_path / "test.duckdb"


@pytest.fixture
def sample_export(tmp_path):
    """Create a minimal Claude export for ingestion."""
    data = [
        {
            "uuid": "conv-1",
            "chat_messages": [
                {
                    "uuid": "msg-1",
                    "sender": "human",
                    "text": "What is OAuth 2.0?",
                    "created_at": "2025-01-01T12:00:00Z",
                    "content": [],
                    "attachments": [],
                },
                {
                    "uuid": "msg-2",
                    "sender": "assistant",
                    "text": "OAuth 2.0 is an authorization framework.",
                    "created_at": "2025-01-01T12:01:00Z",
                    "content": [],
                    "attachments": [],
                },
            ],
        }
    ]
    f = tmp_path / "conversations.json"
    f.write_text(json.dumps(data))
    return f


class TestMemexContextManager:
    def test_opens_and_closes(self, corpus_path):
        with Memex(path=corpus_path, embed=False) as m:
            stats = m.stats()
            assert stats.total_fragments == 0

    def test_explicit_close(self, corpus_path):
        m = Memex(path=corpus_path, embed=False)
        m.close()


class TestMemexSearch:
    def test_search_empty_corpus(self, corpus_path):
        with Memex(path=corpus_path, embed=False) as m:
            results = m.search("anything")
            assert results == []

    def test_search_after_ingest(self, corpus_path, sample_export):
        with Memex(path=corpus_path, embed=False) as m:
            parsed, stored = m.ingest(sample_export)
            assert parsed >= 2
            assert stored >= 2

            results = m.search("OAuth")
            assert len(results) >= 1
            assert all(isinstance(r, tuple) for r in results)
            frag, score = results[0]
            assert isinstance(frag, Fragment)
            assert isinstance(score, float)


class TestMemexIngest:
    def test_ingest_returns_counts(self, corpus_path, sample_export):
        with Memex(path=corpus_path, embed=False) as m:
            parsed, stored = m.ingest(sample_export)
            assert parsed > 0
            assert stored > 0

    def test_ingest_deduplicates(self, corpus_path, sample_export):
        with Memex(path=corpus_path, embed=False) as m:
            _, first = m.ingest(sample_export)
            _, second = m.ingest(sample_export)
            assert first > 0
            assert second == 0

    def test_ingest_string_path(self, corpus_path, sample_export):
        with Memex(path=corpus_path, embed=False) as m:
            parsed, stored = m.ingest(str(sample_export))
            assert stored > 0


class TestMemexStats:
    def test_returns_typed_stats(self, corpus_path):
        with Memex(path=corpus_path, embed=False) as m:
            stats = m.stats()
            assert isinstance(stats, CorpusStats)
            assert stats.total_fragments == 0

    def test_stats_after_ingest(self, corpus_path, sample_export):
        with Memex(path=corpus_path, embed=False) as m:
            m.ingest(sample_export)
            stats = m.stats()
            assert stats.total_fragments > 0
            assert stats.conversations >= 1


class TestMemexConversations:
    def test_list_conversations(self, corpus_path, sample_export):
        with Memex(path=corpus_path, embed=False) as m:
            m.ingest(sample_export)
            convs = m.list_conversations()
            assert len(convs) >= 1
            assert isinstance(convs[0], ConversationSummary)

    def test_find_conversation(self, corpus_path, sample_export):
        with Memex(path=corpus_path, embed=False) as m:
            m.ingest(sample_export)
            convs = m.list_conversations()
            conv_id = convs[0].conversation_id

            frags = m.find_conversation(conv_id)
            assert len(frags) >= 1
            assert all(isinstance(f, Fragment) for f in frags)


class TestMemexPathOverride:
    def test_string_path(self, tmp_path):
        path = str(tmp_path / "custom.duckdb")
        with Memex(path=path, embed=False) as m:
            assert m.stats().total_fragments == 0

    def test_two_instances_different_paths(self, tmp_path):
        path_a = tmp_path / "a.duckdb"
        path_b = tmp_path / "b.duckdb"

        with Memex(path=path_a, embed=False) as a:
            with Memex(path=path_b, embed=False) as b:
                assert a.stats().total_fragments == 0
                assert b.stats().total_fragments == 0
