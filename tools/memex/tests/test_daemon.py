"""Tests for memexd daemon — protocol, server, and remote adapter."""

import json
import tempfile
import threading
import time
from pathlib import Path

import pytest
from memex.adapters._out.corpus.duckdb import DuckDBCorpus
from memex.adapters._out.corpus.remote import RemoteCorpusAdapter
from memex.daemon.protocol import (
    Dispatcher,
    parse_fragments,
)
from memex.daemon.server import Server
from memex.domain.models import Fragment


class TestProtocol:
    """Test JSON-RPC dispatch without network."""

    @pytest.fixture
    def corpus_and_dispatcher(self, sample_fragments):
        with tempfile.TemporaryDirectory() as tmpdir:
            corpus_path = Path(tmpdir) / "test.duckdb"
            corpus = DuckDBCorpus(corpus_path)
            corpus.store(sample_fragments)
            corpus.rebuild_search_index()
            dispatcher = Dispatcher(corpus=corpus, graph=corpus, trails=corpus)
            yield corpus, dispatcher
            corpus.close()

    def test_corpus_stats(self, corpus_and_dispatcher):
        corpus, dispatcher = corpus_and_dispatcher
        request = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "corpus.stats",
            }
        )
        response = json.loads(dispatcher.dispatch(request))
        assert "result" in response
        assert response["result"]["total_fragments"] > 0

    def test_corpus_search(self, corpus_and_dispatcher):
        corpus, dispatcher = corpus_and_dispatcher
        request = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "corpus.search",
                "params": {"query": "authentication", "limit": 5},
            }
        )
        response = json.loads(dispatcher.dispatch(request))
        assert "result" in response
        fragments = parse_fragments(response["result"])
        assert len(fragments) > 0
        assert all(isinstance(f, Fragment) for f in fragments)

    def test_unknown_method(self, corpus_and_dispatcher):
        _, dispatcher = corpus_and_dispatcher
        request = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "nonexistent.method",
            }
        )
        response = json.loads(dispatcher.dispatch(request))
        assert "error" in response
        assert response["error"]["code"] == -32601

    def test_parse_error(self, corpus_and_dispatcher):
        _, dispatcher = corpus_and_dispatcher
        response = json.loads(dispatcher.dispatch("not json"))
        assert "error" in response
        assert response["error"]["code"] == -32700

    def test_edge_stats(self, corpus_and_dispatcher):
        _, dispatcher = corpus_and_dispatcher
        request = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "graph.edge_stats",
            }
        )
        response = json.loads(dispatcher.dispatch(request))
        assert "result" in response

    def test_trails_crud(self, corpus_and_dispatcher):
        _, dispatcher = corpus_and_dispatcher

        # Create trail
        req = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 10,
                "method": "trails.create_trail",
                "params": {"name": "test trail", "description": "a test"},
            }
        )
        resp = json.loads(dispatcher.dispatch(req))
        assert "result" in resp

        # List trails
        req = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 11,
                "method": "trails.list_trails",
            }
        )
        resp = json.loads(dispatcher.dispatch(req))
        assert len(resp["result"]) == 1
        assert resp["result"][0]["name"] == "test trail"

        # Delete trail
        req = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 12,
                "method": "trails.delete_trail",
                "params": {"trail_name": "test trail"},
            }
        )
        resp = json.loads(dispatcher.dispatch(req))
        assert resp["result"] is True

    def test_limit_clamping(self, corpus_and_dispatcher):
        _, dispatcher = corpus_and_dispatcher
        request = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 5,
                "method": "corpus.search",
                "params": {"query": "test", "limit": 9999},
            }
        )
        # Should not error — limit is clamped server-side
        response = json.loads(dispatcher.dispatch(request))
        assert "result" in response


class TestServerAndRemote:
    """Integration test: server + remote adapter over Unix socket."""

    @pytest.fixture
    def daemon(self, sample_fragments):
        """Start a daemon in a thread, yield remote adapter, stop on cleanup."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            corpus_path = tmpdir / "test.duckdb"
            sock_path = tmpdir / "memexd.sock"
            pid_path = tmpdir / "memexd.pid"

            corpus = DuckDBCorpus(corpus_path)
            corpus.store(sample_fragments)
            corpus.rebuild_search_index()

            dispatcher = Dispatcher(corpus=corpus, graph=corpus, trails=corpus)
            server = Server(dispatcher, sock_path=sock_path, pid_path=pid_path)

            thread = threading.Thread(
                target=lambda: server.start(register_signals=False),
                daemon=True,
            )
            thread.start()

            # Wait for socket to appear
            for _ in range(50):
                if sock_path.exists():
                    break
                time.sleep(0.05)
            else:
                pytest.fail("Daemon socket did not appear")

            remote = RemoteCorpusAdapter(sock_path)
            yield remote

            remote.close()
            server.stop()
            thread.join(timeout=3)
            corpus.close()

    def test_stats_over_socket(self, daemon):
        stats = daemon.stats()
        assert stats.total_fragments > 0

    def test_search_over_socket(self, daemon):
        results = daemon.search("authentication")
        assert len(results) > 0
        assert all(isinstance(f, Fragment) for f in results)

    def test_find_by_conversation(self, daemon):
        stats = daemon.stats()
        if stats.conversations > 0:
            convs = daemon.list_conversations(limit=1)
            assert len(convs) > 0
            frags = daemon.find_by_conversation(convs[0].conversation_id)
            assert len(frags) > 0

    def test_schema(self, daemon):
        schema = daemon.schema()
        assert len(schema.fragments) > 0

    def test_trails_over_socket(self, daemon):
        trail_id = daemon.create_trail("socket trail", "testing")
        assert trail_id

        trails = daemon.list_trails()
        assert any(t.name == "socket trail" for t in trails)

        daemon.delete_trail("socket trail")
        trails = daemon.list_trails()
        assert not any(t.name == "socket trail" for t in trails)

    def test_concurrent_reads(self, daemon):
        """Two threads reading simultaneously — the whole point of the daemon."""
        results = [None, None]
        errors = [None, None]
        barrier = threading.Barrier(2, timeout=5)

        def search(idx, query):
            try:
                # Each thread needs its own connection
                adapter = RemoteCorpusAdapter(daemon._socket_path)
                # Barrier ensures both threads issue requests at the same time
                barrier.wait()
                results[idx] = adapter.search(query)
                adapter.close()
            except Exception as e:
                errors[idx] = e

        t1 = threading.Thread(target=search, args=(0, "authentication"))
        t2 = threading.Thread(target=search, args=(1, "API"))
        t1.start()
        t2.start()
        t1.join(timeout=5)
        t2.join(timeout=5)

        assert errors[0] is None, f"Thread 0 error: {errors[0]}"
        assert errors[1] is None, f"Thread 1 error: {errors[1]}"
        assert results[0] is not None
        assert results[1] is not None
