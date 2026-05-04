"""Tests for WebCollector — fetches + converts via injected ports.

Both Requester and DocumentConverter are injected at construction time;
tests pass fakes directly. No monkeypatching, no network, no markitdown
dependency in the test path.
"""

import pytest
from recon.adapters._out.web_collector import WebCollector
from recon.domain.converters import ConversionResult
from recon.domain.exceptions import CollectionError
from recon.domain.http import HttpResponse
from recon.domain.models import CollectorEntry, SourceEntry


class _FakeRequester:
    def __init__(
        self,
        response: HttpResponse | None = None,
        raise_on_call: Exception | None = None,
    ):
        self.response = response
        self.raise_on_call = raise_on_call
        self.calls: list[dict] = []

    def request(self, source, method, url, *, params=None, headers=None, json_body=None):
        self.calls.append({"method": method, "url": url, "headers": headers})
        if self.raise_on_call:
            raise self.raise_on_call
        return self.response

    def get(self, source, url, *, headers=None):
        return self.request(source, "GET", url, params={}, headers=headers)


class _FakeConverter:
    def __init__(self, result: ConversionResult | None = None):
        self.result = result or ConversionResult(title="", text="")
        self.calls: list[dict] = []

    def convert(self, content: bytes, content_type: str, url: str) -> ConversionResult:
        self.calls.append({"content": content, "content_type": content_type, "url": url})
        return self.result


def _resp(url: str, body: bytes, content_type: str) -> HttpResponse:
    return HttpResponse(
        status_code=200,
        headers={"content-type": content_type},
        body=body,
        text=body.decode(errors="ignore"),
        url=url,
        content_type=content_type,
    )


class TestWebCollector:
    def test_requires_source(self):
        entry = CollectorEntry(name="test", type="web")
        with pytest.raises(CollectionError, match="requires a source"):
            list(WebCollector(_FakeRequester(), _FakeConverter()).collect(entry, None))

    def test_html_flows_through_converter(self):
        req = _FakeRequester(_resp("https://x/", b"<html><title>T</title></html>", "text/html"))
        conv = _FakeConverter(ConversionResult(title="My Page", text="# Heading\n\nBody"))
        source = SourceEntry(name="s", url="https://x")
        entry = CollectorEntry(name="t", type="web", source="s")

        records = list(WebCollector(req, conv).collect(entry, source))
        assert len(records) == 1
        record = records[0]
        assert record["title"] == "My Page"
        assert record["content"] == "# Heading\n\nBody"
        assert record["status_code"] == 200
        assert record["content_type"] == "text/html"
        # Converter received the raw bytes + content type + URL
        assert conv.calls[0]["content"] == b"<html><title>T</title></html>"
        assert conv.calls[0]["content_type"] == "text/html"

    def test_pdf_flows_through_same_path(self):
        """Same code path for PDFs — converter handles format detection."""
        req = _FakeRequester(_resp("https://x/report.pdf", b"%PDF-1.4 ...", "application/pdf"))
        conv = _FakeConverter(ConversionResult(title="Q4 Report", text="## Summary\n\nText."))
        source = SourceEntry(name="s", url="https://x")
        entry = CollectorEntry(name="t", type="web", source="s", endpoint="/report.pdf")

        records = list(WebCollector(req, conv).collect(entry, source))
        assert records[0]["title"] == "Q4 Report"
        assert records[0]["content_type"] == "application/pdf"
        assert "Summary" in records[0]["content"]
        assert conv.calls[0]["content_type"] == "application/pdf"

    def test_endpoint_appended_to_source_url(self):
        req = _FakeRequester(_resp("https://x/docs", b"<html></html>", "text/html"))
        conv = _FakeConverter()
        source = SourceEntry(name="s", url="https://x")
        entry = CollectorEntry(name="t", type="web", source="s", endpoint="/docs")
        list(WebCollector(req, conv).collect(entry, source))
        assert req.calls[0]["url"] == "https://x/docs"

    def test_requester_error_propagates(self):
        err = CollectionError("network down")
        req = _FakeRequester(raise_on_call=err)
        conv = _FakeConverter()
        source = SourceEntry(name="s", url="https://x")
        entry = CollectorEntry(name="t", type="web", source="s")
        with pytest.raises(CollectionError, match="network down"):
            list(WebCollector(req, conv).collect(entry, source))

    def test_converter_error_propagates(self):
        req = _FakeRequester(_resp("https://x", b"garbage", "application/octet-stream"))

        class _BadConverter:
            def convert(self, content, content_type, url):
                raise CollectionError("unsupported format")

        source = SourceEntry(name="s", url="https://x")
        entry = CollectorEntry(name="t", type="web", source="s")
        with pytest.raises(CollectionError, match="unsupported format"):
            list(WebCollector(req, _BadConverter()).collect(entry, source))

    def test_content_truncation(self):
        huge = "x" * 200_000
        req = _FakeRequester(_resp("https://x", b"<html></html>", "text/html"))
        conv = _FakeConverter(ConversionResult(title="T", text=huge))
        source = SourceEntry(name="s", url="https://x")
        entry = CollectorEntry(name="t", type="web", source="s")
        records = list(WebCollector(req, conv).collect(entry, source))
        assert "Content truncated" in records[0]["content"]
        assert len(records[0]["content"]) < len(huge)
