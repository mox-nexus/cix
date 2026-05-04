"""WebCollector — fetch a document, convert it to markdown, yield a record.

HTTP is delegated to the injected Requester (shared rate-limited instance);
conversion is delegated to the injected DocumentConverter (markitdown by
default — handles HTML, PDF, DOCX, PPTX, XLSX, EPub, CSV, JSON, XML, ZIP,
images with OCR, audio transcription, YouTube).

The collector is now format-agnostic: same code path for a web page, a PDF
URL, a DOCX download, or a YouTube transcript. Returns Iterator[dict] —
yields one record today; streaming-many-records is reserved for future
multi-page crawlers.
"""

from __future__ import annotations

import re
from collections.abc import Iterator
from typing import Any

from recon.adapters._out.api_collector import Requester
from recon.domain.converters import DocumentConverter
from recon.domain.exceptions import CollectionError
from recon.domain.http import HttpResponse
from recon.domain.models import CollectorEntry, SourceEntry

_MAX_CONTENT_CHARS = 100_000


class WebCollector:
    """HTTP GET → document-to-markdown conversion → one JSONL record."""

    def __init__(self, requester: Requester, converter: DocumentConverter) -> None:
        self._requester = requester
        self._converter = converter

    def collect(
        self,
        entry: CollectorEntry,
        source: SourceEntry | None,
        *,
        raw_store: Any | None = None,
    ) -> Iterator[dict[str, Any]]:
        if not source:
            msg = f"Web collector '{entry.name}' requires a source"
            raise CollectionError(msg)

        url = source.url.rstrip("/")
        if entry.endpoint:
            url = f"{url}{entry.endpoint}"

        headers = {
            "User-Agent": source.user_agent or "recon/web",
            # Widened from HTML-only so non-HTML content types (PDF, DOCX,
            # images, audio) are served directly by the origin.
            "Accept": "*/*",
        }
        resp: HttpResponse = self._requester.get(source, url, headers=headers)

        if raw_store is not None:
            raw_store.save_http(
                entry.name,
                resp.body,
                status=resp.status_code,
                url=resp.url,
                headers=resp.headers,
                content_type=resp.content_type,
            )

        result = self._converter.convert(resp.body, resp.content_type, resp.url)

        content = re.sub(r"\n{3,}", "\n\n", result.text).strip()
        if len(content) > _MAX_CONTENT_CHARS:
            content = content[:_MAX_CONTENT_CHARS] + "\n\n[Content truncated due to length...]"

        yield {
            "url": resp.url,
            "title": result.title,
            "content": content,
            "status_code": resp.status_code,
            "content_type": resp.content_type,
        }
