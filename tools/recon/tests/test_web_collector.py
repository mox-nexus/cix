"""Tests for WebCollector — HTML to markdown, title extraction."""

import pytest
from recon.adapters._out.web_collector import WebCollector, _extract_title
from recon.application.utilization import RateLimiter
from recon.domain.exceptions import CollectionError
from recon.domain.models import CollectorEntry, SourceEntry


class TestExtractTitle:
    def test_basic(self):
        html = "<html><head><title>Hello World</title></head></html>"
        assert _extract_title(html) == "Hello World"

    def test_multiline(self):
        html = "<title>\n  My Page\n</title>"
        assert _extract_title(html) == "My Page"

    def test_missing(self):
        assert _extract_title("<html><body>No title here</body></html>") == ""

    def test_empty(self):
        assert _extract_title("<title></title>") == ""


class TestWebCollector:
    def test_requires_source(self):
        entry = CollectorEntry(name="test", type="web")
        with pytest.raises(CollectionError, match="requires a source"):
            WebCollector(RateLimiter()).collect(entry, None)

    def test_fetch_real_page(self):
        """Fetch a real public page and verify markdown conversion."""
        source = SourceEntry(
            name="httpbin",
            type="web",
            url="https://httpbin.org",
            rate_limit={"rps": 1, "burst": 1},
        )
        entry = CollectorEntry(name="test", type="web", source="httpbin", endpoint="/html")
        records = WebCollector(RateLimiter()).collect(entry, source)

        assert len(records) == 1
        record = records[0]
        assert record["status_code"] == 200
        assert record["content_type"] == "text/html"
        # Content should be markdown, not raw HTML
        assert "<html>" not in record["content"]
        assert "<body>" not in record["content"]
        # httpbin.org/html contains Herman Melville text
        assert "Herman Melville" in record["content"]

    def test_endpoint_appended(self):
        """Endpoint is appended to source URL."""
        source = SourceEntry(
            name="httpbin",
            type="web",
            url="https://httpbin.org",
            rate_limit={"rps": 1, "burst": 1},
        )
        entry = CollectorEntry(
            name="test",
            type="web",
            source="httpbin",
            endpoint="/html",
        )
        records = WebCollector(RateLimiter()).collect(entry, source)
        assert len(records) == 1
        assert records[0]["status_code"] == 200
        assert "Herman Melville" in records[0]["content"]

    def test_bad_url_raises(self):
        source = SourceEntry(
            name="bad",
            type="web",
            url="https://this-domain-does-not-exist-recon-test.invalid",
            rate_limit={"rps": 1, "burst": 1},
        )
        entry = CollectorEntry(name="test", type="web", source="bad")
        with pytest.raises(CollectionError, match="Web fetch failed"):
            WebCollector(RateLimiter()).collect(entry, source)
