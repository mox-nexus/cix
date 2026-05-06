"""ApiCollector — delegates HTTP to an injected Requester; yields records.

No direct httpx import. No rate limiter (that's inside the Requester).
Constructor-injected dependencies are explicit: tests pass a fake Requester
without monkeypatching anything.
"""

from __future__ import annotations

import os
from collections.abc import Iterator, Mapping
from typing import Any, Protocol

from glom import GlomError, glom

from recon import DEFAULT_USER_AGENT
from recon.application.recon import find_unresolved, substitute
from recon.application.transforms import apply_normalize
from recon.domain.exceptions import CollectionError
from recon.domain.http import HttpResponse
from recon.domain.models import CollectorEntry, SourceEntry


class Requester(Protocol):
    """The port: given a source + HTTP parameters, return an HttpResponse.

    Rate limiting is the Requester's responsibility, not the collector's.
    """

    def request(
        self,
        source: SourceEntry,
        method: str,
        url: str,
        *,
        params: dict[str, str] | None = ...,
        headers: dict[str, str] | None = ...,
        json_body: dict[str, Any] | None = ...,
    ) -> HttpResponse: ...

    def get(
        self,
        source: SourceEntry,
        url: str,
        *,
        headers: dict[str, str] | None = ...,
    ) -> HttpResponse: ...


class ApiCollector:
    """Fetches structured data from an HTTP API and yields records.

    Returns an Iterator so large responses don't force list materialization
    at the call site. (True streaming into normalize/sink requires the
    requester to return a streaming body; current Requester buffers.)
    """

    def __init__(self, requester: Requester, env: Mapping[str, str] | None = None) -> None:
        self._requester = requester
        self._env = env if env is not None else os.environ

    def collect(
        self,
        entry: CollectorEntry,
        source: SourceEntry | None,
        *,
        raw_store: Any | None = None,
    ) -> Iterator[dict[str, Any]]:
        if not source:
            msg = f"API collector '{entry.name}' requires a source"
            raise CollectionError(msg)
        if not entry.endpoint:
            msg = f"API collector '{entry.name}' has no endpoint"
            raise CollectionError(msg)

        url = self._build_url(source.url, entry.endpoint, entry.params or {})
        query_params = self._build_query_params(entry.params or {})
        headers = self._build_headers(source)

        body: dict[str, Any] | None = None
        if entry.body:
            body = substitute(entry.body, entry.params or {})
            unresolved = find_unresolved(body)
            if unresolved:
                missing = ", ".join(sorted(set(unresolved)))
                msg = (
                    f"API collector '{entry.name}' body has unresolved placeholder(s): "
                    f"{{{missing}}}. Add them to params: — sending this literally to the "
                    f"server will silently fail or return empty results."
                )
                raise CollectionError(msg)

        resp = self._requester.request(
            source,
            entry.method,
            url,
            params=query_params,
            headers=headers,
            json_body=body,
        )

        if raw_store is not None:
            raw_store.save_http(
                entry.name,
                resp.body,
                status=resp.status_code,
                url=resp.url,
                headers=resp.headers,
                content_type=resp.content_type,
            )

        data = self._parse_response(resp, entry.response_format)

        if entry.extract and isinstance(data, (dict, list)):
            data = _extract(data, entry.extract)

        records = _ensure_list(data)

        if entry.normalize:
            for record in records:
                yield apply_normalize(record, entry.normalize)
        else:
            yield from records

    # --- Private ---

    def _build_headers(self, source: SourceEntry) -> dict[str, str]:
        ua = source.user_agent or DEFAULT_USER_AGENT
        return {"User-Agent": ua, **self._resolve_auth(source)}

    def _resolve_auth(self, source: SourceEntry) -> dict[str, str]:
        auth = source.auth
        if not auth.header or not auth.env:
            return {}
        value = self._env.get(auth.env, "")
        if not value:
            return {}
        return {auth.header: f"{auth.prefix}{value}"}

    def _build_url(
        self,
        base_url: str,
        endpoint: str,
        params: dict[str, str],
    ) -> str:
        path = substitute(endpoint, params)
        return f"{base_url.rstrip('/')}{path}"

    def _build_query_params(self, params: dict[str, str]) -> dict[str, str]:
        """Drop entries whose values still contain {placeholder}."""
        resolved = {}
        for k, v in params.items():
            if isinstance(v, str) and "{" in v:
                continue
            resolved[k] = v
        return resolved

    def _parse_response(self, resp: HttpResponse, fmt: str) -> Any:
        import json

        if fmt == "json":
            if not resp.text:
                return None
            try:
                return json.loads(resp.text)
            except json.JSONDecodeError as exc:
                msg = f"Response is not valid JSON from {resp.url}: {exc}"
                raise CollectionError(msg) from exc
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
