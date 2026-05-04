"""HttpxRequester — the only adapter that imports httpx.

Rate limiting lives here, not in collectors. Every call to `request()` acquires
a token for its source before hitting the network, so paginated collectors
can't forget to rate-limit per-page. Adapters construct HttpResponse domain
value objects; collectors never see httpx.Response.
"""

from __future__ import annotations

from typing import Any

import httpx
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from recon.application.utilization import RateLimiter
from recon.domain.exceptions import CollectionError
from recon.domain.http import HttpResponse
from recon.domain.models import SourceEntry


def _is_retryable(exc: BaseException) -> bool:
    """Retry on 429, 5xx, and transport errors."""
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code == 429 or exc.response.status_code >= 500
    return isinstance(exc, httpx.TransportError)


def _retry_wait(retry_state: Any) -> float:
    """Use retry-after header if present, else exponential backoff."""
    exc = retry_state.outcome.exception()
    if isinstance(exc, httpx.HTTPStatusError):
        retry_after = exc.response.headers.get("retry-after")
        if retry_after:
            try:
                return float(retry_after)
            except ValueError:
                pass
    return wait_exponential(multiplier=1, min=1, max=8)(retry_state)


@retry(
    stop=stop_after_attempt(3),
    wait=_retry_wait,
    retry=retry_if_exception(_is_retryable),
    reraise=True,
)
def _do_request(
    client: httpx.Client,
    method: str,
    url: str,
    *,
    params: dict[str, str],
    headers: dict[str, str],
    json_body: dict[str, Any] | None,
) -> httpx.Response:
    resp = client.request(method, url, params=params, headers=headers, json=json_body)
    resp.raise_for_status()
    return resp


def _to_domain(resp: httpx.Response) -> HttpResponse:
    """Convert httpx.Response to the domain value object."""
    content_type = resp.headers.get("content-type", "")
    return HttpResponse(
        status_code=resp.status_code,
        headers=dict(resp.headers),
        body=resp.content,
        text=resp.text,
        url=str(resp.url),
        content_type=content_type.split(";")[0].strip(),
    )


class HttpxRequester:
    """HTTP adapter with rate limiting and retry. Returns HttpResponse VO."""

    def __init__(self, rate_limiter: RateLimiter) -> None:
        self._rate_limiter = rate_limiter

    def request(
        self,
        source: SourceEntry,
        method: str,
        url: str,
        *,
        params: dict[str, str] | None = None,
        headers: dict[str, str] | None = None,
        json_body: dict[str, Any] | None = None,
    ) -> HttpResponse:
        """Single HTTP request. Rate-limits against the source before firing.

        Paginated callers call this in a loop; each call acquires its own
        token, so rate limits are always honored at the page level.
        """
        self._rate_limiter.acquire(source)
        try:
            with httpx.Client(timeout=source.timeout, follow_redirects=True) as client:
                resp = _do_request(
                    client,
                    method,
                    url,
                    params=params or {},
                    headers=headers or {},
                    json_body=json_body,
                )
        except (httpx.HTTPStatusError, httpx.TransportError) as exc:
            status = ""
            snippet = ""
            if isinstance(exc, httpx.HTTPStatusError):
                status = f" (HTTP {exc.response.status_code})"
                text = exc.response.text or ""
                if text:
                    snippet = f"\nResponse body: {text[:200]}"
            msg = f"HTTP request failed after retries: {url}{status}{snippet}"
            raise CollectionError(msg) from exc

        return _to_domain(resp)

    def get(
        self,
        source: SourceEntry,
        url: str,
        *,
        headers: dict[str, str] | None = None,
    ) -> HttpResponse:
        """Simple GET shortcut for the web collector. Same rate-limit path."""
        return self.request(source, "GET", url, headers=headers)
