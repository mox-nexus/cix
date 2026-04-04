"""ApiCollector — auth, retry, normalize, return records.

Rate limiting injected via RateLimiter. Retry via tenacity.
Uses glom for response extraction.
"""

from __future__ import annotations

import os
import sys
from typing import Any

import httpx
from glom import GlomError, glom
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from recon import DEFAULT_USER_AGENT
from recon.application.recon import substitute
from recon.application.transforms import apply_normalize
from recon.application.utilization import RateLimiter
from recon.domain.exceptions import CollectionError
from recon.domain.models import CollectorEntry, SourceEntry

# --- Retry ---


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
def _fetch(
    client: httpx.Client,
    method: str,
    url: str,
    *,
    params: dict[str, str],
    headers: dict[str, str],
) -> httpx.Response:
    """HTTP request with retry on 429/5xx/transport errors."""
    resp = client.request(method, url, params=params, headers=headers)
    resp.raise_for_status()
    return resp


# --- Collector ---


class ApiCollector:
    """HTTP collection with auth, retry. Rate limiting via injected RateLimiter."""

    def __init__(self, rate_limiter: RateLimiter) -> None:
        self._rate_limiter = rate_limiter

    def collect(
        self,
        entry: CollectorEntry,
        source: SourceEntry | None,
    ) -> list[dict[str, Any]]:
        """Collect from HTTP source, normalize, return records."""
        if not source:
            msg = f"API collector '{entry.name}' requires a source"
            raise CollectionError(msg)
        if not entry.endpoint:
            msg = f"API collector '{entry.name}' has no endpoint"
            raise CollectionError(msg)

        self._rate_limiter.acquire(source)

        url = self._build_url(source.url, entry.endpoint, entry.params or {})
        query_params = self._build_query_params(entry.params or {})
        auth_headers = self._resolve_auth(source)
        ua = source.user_agent or DEFAULT_USER_AGENT
        headers = {"User-Agent": ua, **auth_headers}

        if source.auth.param and source.auth.env:
            api_key = os.environ.get(source.auth.env, "")
            if api_key:
                query_params[source.auth.param] = api_key

        with httpx.Client(timeout=source.timeout, follow_redirects=True) as client:
            try:
                resp = _fetch(client, entry.method, url, params=query_params, headers=headers)
            except (httpx.HTTPStatusError, httpx.TransportError) as exc:
                msg = f"HTTP collection failed after retries: {url}"
                raise CollectionError(msg) from exc

        data = self._parse_response(resp, entry.response_format)

        if entry.extract and isinstance(data, (dict, list)):
            data = _extract(data, entry.extract)

        records = _ensure_list(data)

        if entry.normalize and records:
            records = [apply_normalize(record, entry.normalize) for record in records]

        return records

    # --- Private ---

    def _resolve_auth(self, source: SourceEntry) -> dict[str, str]:
        auth = source.auth
        if not auth.header or not auth.env:
            return {}
        value = os.environ.get(auth.env, "")
        if not value:
            return {}
        return {auth.header: value}

    def _build_url(
        self, base_url: str, endpoint: str, params: dict[str, str],
    ) -> str:
        path = substitute(endpoint, params)
        return f"{base_url.rstrip('/')}{path}"

    def _build_query_params(self, params: dict[str, str]) -> dict[str, str]:
        """Build query params, warning and dropping unresolved {placeholders}."""
        resolved = {}
        for k, v in params.items():
            if "{" in v:
                print(
                    f"  WARNING: dropping unresolved param {k}={v!r} "
                    f"— edit config to set actual values",
                    file=sys.stderr,
                )
            else:
                resolved[k] = v
        return resolved

    def _parse_response(self, resp: httpx.Response, fmt: str) -> Any:
        if fmt == "json":
            return resp.json()
        if fmt == "xml":
            import xmltodict

            return xmltodict.parse(
                resp.text,
                process_namespaces=True,
                namespaces={
                    "http://www.w3.org/2005/Atom": None,
                    "http://arxiv.org/schemas/atom": "arxiv:",
                    "http://a9.com/-/spec/opensearch/1.1/": "opensearch:",
                },
                force_list=("entry", "author", "link", "category"),
            )
        return resp.text


# --- Helpers ---


def _extract(data: Any, dotted_path: str) -> Any:
    """Navigate nested dict via dotted path using glom."""
    try:
        return glom(data, dotted_path)
    except (GlomError, KeyError, TypeError):
        return None


def _ensure_list(data: Any) -> list[dict[str, Any]]:
    """Coerce response to list of dicts."""
    if isinstance(data, list):
        return [d for d in data if isinstance(d, dict)]
    if isinstance(data, dict):
        return [data]
    return []
