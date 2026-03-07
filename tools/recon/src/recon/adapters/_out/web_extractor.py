"""Web content extractor — implements WebFetchPort."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

import httpx
import trafilatura


class WebExtractorAdapter:
    """WebFetchPort implementation. Fetches URLs and extracts text via trafilatura."""

    def fetch(self, url: str, output_dir: Path) -> Path | None:
        output_dir.mkdir(parents=True, exist_ok=True)

        try:
            with httpx.Client(follow_redirects=True, timeout=30) as client:
                resp = client.get(url)
                resp.raise_for_status()
        except (httpx.HTTPError, OSError):
            return None

        content_type = resp.headers.get("content-type", "")
        slug = _url_slug(url)

        # PDF — write directly for pdftotext to handle
        if "pdf" in content_type or resp.content[:5] == b"%PDF-":
            pdf_path = output_dir / f"{slug}.pdf"
            pdf_path.write_bytes(resp.content)
            return pdf_path

        # HTML — extract with trafilatura
        text = trafilatura.extract(resp.text)
        if not text or len(text.strip()) < 100:
            return None

        txt_path = output_dir / f"{slug}.txt"
        txt_path.write_text(text)
        return txt_path


def _url_slug(url: str) -> str:
    parsed = urlparse(url)
    parts = parsed.netloc.replace("www.", "").split(".")
    domain = parts[0] if parts else "web"
    path = parsed.path.strip("/").replace("/", "-")[:40]
    return f"{domain}-{path}" if path else domain
