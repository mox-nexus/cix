"""WebCollector — fetches web pages, converts HTML to markdown, returns records.

Uses markdownify (Python Turndown equivalent) to preserve document structure
as markdown — headings, links, lists, code blocks. Not plain text stripping.
Rate limiting injected via RateLimiter. Retry via tenacity.
"""

from __future__ import annotations

import re
from typing import Any

import httpx
from markdownify import markdownify as md
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from recon import DEFAULT_USER_AGENT
from recon.application.utilization import RateLimiter
from recon.domain.exceptions import CollectionError
from recon.domain.models import CollectorEntry, SourceEntry

_MAX_CONTENT_CHARS = 100_000
_MAX_REDIRECTS = 10


def _extract_title(html: str) -> str:
    """Extract <title> from HTML via regex."""
    match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else ""


def _is_retryable(exc: BaseException) -> bool:
    """Retry on 5xx and transport errors. Not 429 — web pages don't rate-limit like APIs."""
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code >= 500
    return isinstance(exc, httpx.TransportError)


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=8),
    retry=retry_if_exception(_is_retryable),
    reraise=True,
)
def _fetch(
    client: httpx.Client,
    url: str,
    *,
    headers: dict[str, str],
) -> httpx.Response:
    """HTTP GET with retry on 5xx/transport errors."""
    resp = client.get(url, headers=headers)
    resp.raise_for_status()
    return resp


class WebCollector:
    """Fetches web pages, converts HTML to markdown. Rate limiting + retry."""

    def __init__(self, rate_limiter: RateLimiter) -> None:
        self._rate_limiter = rate_limiter

    def collect(
        self,
        entry: CollectorEntry,
        source: SourceEntry | None,
    ) -> list[dict[str, Any]]:
        """Fetch page, convert to markdown, return as record."""
        if not source:
            msg = f"Web collector '{entry.name}' requires a source"
            raise CollectionError(msg)

        url = source.url.rstrip("/")
        if entry.endpoint:
            url = f"{url}{entry.endpoint}"

        self._rate_limiter.acquire(source)

        ua = source.user_agent or DEFAULT_USER_AGENT
        headers = {
            "User-Agent": ua,
            "Accept": "text/html, text/markdown, */*",
        }

        try:
            with httpx.Client(
                timeout=source.timeout,
                follow_redirects=True,
                max_redirects=_MAX_REDIRECTS,
            ) as client:
                resp = _fetch(client, url, headers=headers)
        except (httpx.HTTPStatusError, httpx.TransportError) as exc:
            msg = f"Web fetch failed after retries: {url}"
            raise CollectionError(msg) from exc

        content_type = resp.headers.get("content-type", "")
        raw = resp.text

        if "text/html" in content_type:
            title = _extract_title(raw)
            # Truncate raw HTML before conversion to bound markdownify memory
            if len(raw) > _MAX_CONTENT_CHARS * 3:
                raw = raw[: _MAX_CONTENT_CHARS * 3]
            content = md(raw, strip=["img", "script", "style", "noscript"])
        else:
            title = ""
            content = raw

        content = re.sub(r"\n{3,}", "\n\n", content).strip()

        if len(content) > _MAX_CONTENT_CHARS:
            content = content[:_MAX_CONTENT_CHARS] + "\n\n[Content truncated due to length...]"

        return [
            {
                "url": str(resp.url),
                "title": title,
                "content": content,
                "status_code": resp.status_code,
                "content_type": content_type.split(";")[0].strip(),
            }
        ]
