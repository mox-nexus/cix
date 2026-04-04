"""Integration tests against live APIs and real filesystems.

Run with: pytest tests/test_integration.py -v
"""

import json
import tempfile
from pathlib import Path

import pytest

from recon.adapters._out.api_collector import ApiCollector
from recon.adapters._out.cli_collector import CliCollector
from recon.adapters._out.web_collector import WebCollector
from recon.application.recon import run
from recon.application.utilization import RateLimiter
from recon.domain.exceptions import CollectionError
from recon.domain.models import CollectorEntry, ReconConfig, SourceEntry


def _collectors():
    rl = RateLimiter()
    return {"cli": CliCollector(), "api": ApiCollector(rl), "web": WebCollector(rl)}


# --- OpenAlex (no auth, fast) ---


class TestOpenAlexLive:
    def test_search(self):
        source = SourceEntry(
            name="openalex",
            url="https://api.openalex.org",
            user_agent="recon/0.7.0 (mailto:test@example.com)",
        )
        entry = CollectorEntry(
            name="test", type="api", source="openalex",
            endpoint="/works",
            params={
                "search": "collaborative intelligence",
                "per_page": "3",
                "select": "id,display_name,publication_year,cited_by_count",
            },
            extract="results",
            normalize={
                "title": "display_name",
                "year": "publication_year",
                "citations": "cited_by_count",
            },
        )
        records = ApiCollector(RateLimiter()).collect(entry, source)
        assert len(records) == 3
        assert all(r["title"] is not None for r in records)
        assert all(isinstance(r["year"], int) for r in records)

    def test_inverted_index_transform(self):
        """OpenAlex abstract_inverted_index → $inverted_index → text."""
        source = SourceEntry(
            name="openalex",
            url="https://api.openalex.org",
            user_agent="recon/0.7.0 (mailto:test@example.com)",
        )
        entry = CollectorEntry(
            name="test", type="api", source="openalex",
            endpoint="/works",
            params={
                "search": "attention mechanism transformer",
                "per_page": "3",
                "select": "display_name,abstract_inverted_index",
            },
            extract="results",
            normalize={
                "title": "display_name",
                "abstract": "abstract_inverted_index|$inverted_index",
            },
        )
        records = ApiCollector(RateLimiter()).collect(entry, source)
        assert len(records) == 3
        # At least one paper should have an abstract (some don't)
        abstracts = [r["abstract"] for r in records if r["abstract"]]
        assert len(abstracts) >= 1
        # Reconstructed abstract is a string, not a dict
        assert isinstance(abstracts[0], str)
        assert len(abstracts[0]) > 20

    def test_full_survey_to_jsonl(self):
        config = ReconConfig.model_validate({
            "catalog": [{
                "name": "openalex",
                "url": "https://api.openalex.org",
                "user_agent": "recon/0.7.0 (mailto:test@example.com)",
            }],
            "collectors": [{
                "name": "oa-search", "type": "api", "source": "openalex",
                "endpoint": "/works",
                "params": {
                    "search": "attention mechanism",
                    "per_page": "2",
                    "select": "id,display_name,publication_year",
                },
                "extract": "results",
                "normalize": {"title": "display_name", "year": "publication_year"},
            }],
        })
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            archive = run(config, _collectors(), mission)
            jsonl = archive / "oa-search.jsonl"
            assert jsonl.exists()
            records = [json.loads(line) for line in jsonl.read_text().splitlines()]
            assert len(records) == 2
            assert records[0]["title"] is not None


# --- Semantic Scholar (rate limited without API key) ---


class TestS2Live:
    def test_search_or_rate_limited(self):
        """S2 works if under rate limit, raises CollectionError if 429."""
        source = SourceEntry(
            name="s2",
            url="https://api.semanticscholar.org/graph/v1",
            rate_limit={"rps": 0.33, "burst": 1},
        )
        entry = CollectorEntry(
            name="test", type="api", source="s2",
            endpoint="/paper/search",
            params={
                "query": "attention mechanism",
                "limit": "2",
                "fields": "title,year",
            },
            extract="data",
            normalize={"title": "title", "year": "year"},
        )
        try:
            records = ApiCollector(RateLimiter()).collect(entry, source)
            assert len(records) == 2
            assert all(r["title"] is not None for r in records)
        except CollectionError:
            pass  # 429 rate limit expected without API key


# --- arXiv (XML, can be slow) ---


class TestArxivLive:
    def test_xml_search(self):
        """arXiv returns XML, parsed via xmltodict. Skips on timeout."""
        source = SourceEntry(name="arxiv", url="https://export.arxiv.org/api")
        entry = CollectorEntry(
            name="test", type="api", source="arxiv",
            endpoint="/query",
            params={"search_query": "attention mechanism", "max_results": "2"},
            response_format="xml",
            extract="feed.entry",
            normalize={
                "title": "title",
                "authors": "author.*.name",
                "published": "published",
            },
        )
        try:
            records = ApiCollector(RateLimiter()).collect(entry, source)
            assert len(records) == 2
            assert all(r["title"] is not None for r in records)
            # Authors should be a list
            assert isinstance(records[0]["authors"], list)
        except CollectionError:
            pytest.skip("arXiv API timed out (known to be slow)")


# --- Zenodo (HTML descriptions) ---


class TestZenodoLive:
    def test_html2text_transform(self):
        """Zenodo descriptions are HTML, $html2text strips tags."""
        source = SourceEntry(
            name="zenodo",
            url="https://zenodo.org/api",
            rate_limit={"rps": 1, "burst": 2},
            user_agent="recon/0.7.0 (https://github.com/mox-labs/cix)",
        )
        entry = CollectorEntry(
            name="test", type="api", source="zenodo",
            endpoint="/records",
            params={"q": "machine learning", "size": "2", "sort": "bestmatch"},
            extract="hits.hits",
            normalize={
                "title": "metadata.title",
                "abstract": "metadata.description|$html2text",
                "authors": "metadata.creators.*.name",
            },
        )
        records = ApiCollector(RateLimiter()).collect(entry, source)
        assert len(records) == 2
        assert all(r["title"] is not None for r in records)
        # Abstract should be plain text (no HTML tags)
        for r in records:
            if r["abstract"]:
                assert "<p>" not in r["abstract"]
                assert "</" not in r["abstract"]


# --- Fan-out with real local directories ---


class TestFanOutLive:
    def test_cli_fan_out_with_cwd(self, tmp_path):
        """Two local sources, one collector, fan-out verifies cwd."""
        repo_a = tmp_path / "repo-a"
        repo_b = tmp_path / "repo-b"
        repo_a.mkdir()
        repo_b.mkdir()
        (repo_a / "hello.txt").write_text("from repo a")
        (repo_b / "hello.txt").write_text("from repo b")

        config = ReconConfig.model_validate({
            "catalog": [
                {"name": "a", "type": "local", "url": str(repo_a)},
                {"name": "b", "type": "local", "url": str(repo_b)},
            ],
            "collectors": [
                {"name": "read", "type": "cli", "run": "cat hello.txt"},
            ],
        })
        mission = tmp_path / "mission"
        mission.mkdir()
        archive = run(config, _collectors(), mission)

        a_lines = (archive / "read-a.jsonl").read_text().splitlines()
        b_lines = (archive / "read-b.jsonl").read_text().splitlines()
        a_records = [json.loads(l) for l in a_lines]
        b_records = [json.loads(l) for l in b_lines]
        assert "from repo a" in a_records[0]["line"]
        assert "from repo b" in b_records[0]["line"]

    def test_mixed_survey_with_errors(self, tmp_path):
        """One source succeeds, another uses a command that hard-fails."""
        good = tmp_path / "good"
        good.mkdir()
        (good / "data.txt").write_text("found")

        config = ReconConfig.model_validate({
            "catalog": [
                {"name": "good", "type": "local", "url": str(good)},
                {"name": "bad", "type": "local", "url": str(good)},
            ],
            "collectors": [
                {"name": "ok", "type": "cli", "run": "cat data.txt", "source": "good"},
                {"name": "fail", "type": "cli", "run": "exit 2", "source": "bad"},
            ],
        })
        mission = tmp_path / "mission"
        mission.mkdir()
        archive = run(config, _collectors(), mission)

        assert (archive / "ok.jsonl").exists()
        import yaml
        meta = yaml.safe_load((archive / "meta.yaml").read_text())
        statuses = {c["name"]: c["status"] for c in meta["collectors"]}
        assert statuses["ok"] == "ok"
        assert statuses["fail"] == "error"
