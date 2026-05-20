"""Tests for ApiCollector — helpers + injected-Requester behavior.

No monkeypatching. Dependencies (Requester, env) are constructor args,
so tests pass fakes directly.
"""

import pytest
from recon.adapters._out.api_collector import ApiCollector, _ensure_list, _extract
from recon.application.recon import find_unresolved, substitute
from recon.domain.exceptions import CollectionError
from recon.domain.http import HttpResponse
from recon.domain.models import AuthConfig, CollectorEntry, SourceEntry


class _FakeRequester:
    """Minimal Requester double — records calls, returns canned HttpResponse."""

    def __init__(
        self, response: HttpResponse | None = None, raise_on_call: Exception | None = None
    ):
        self.response = response
        self.calls: list[dict] = []
        self.raise_on_call = raise_on_call

    def request(self, source, method, url, *, params=None, headers=None, json_body=None):
        self.calls.append(
            {
                "source": source,
                "method": method,
                "url": url,
                "params": params or {},
                "headers": headers or {},
                "json_body": json_body,
            }
        )
        if self.raise_on_call:
            raise self.raise_on_call
        return self.response

    def get(self, source, url, *, headers=None):
        return self.request(source, "GET", url, params={}, headers=headers)


def _ok_response(body_text: str, content_type: str = "application/json") -> HttpResponse:
    return HttpResponse(
        status_code=200,
        headers={"content-type": content_type},
        body=body_text.encode(),
        text=body_text,
        url="https://fake.test/",
        content_type=content_type,
    )


class TestExtract:
    def test_dotted_path(self):
        data = {"feed": {"entry": [{"title": "test"}]}}
        assert _extract(data, "feed.entry") == [{"title": "test"}]

    def test_single_level(self):
        assert _extract({"data": [1, 2]}, "data") == [1, 2]

    def test_missing(self):
        assert _extract({"a": 1}, "b") is None

    def test_deep_missing(self):
        assert _extract({"a": {"b": 1}}, "a.c") is None


class TestEnsureList:
    def test_list_of_dicts(self):
        assert _ensure_list([{"a": 1}, {"b": 2}]) == [{"a": 1}, {"b": 2}]

    def test_filters_non_dicts(self):
        assert _ensure_list([{"a": 1}, "skip", 42]) == [{"a": 1}]

    def test_single_dict(self):
        assert _ensure_list({"a": 1}) == [{"a": 1}]

    def test_string(self):
        assert _ensure_list("text") == []

    def test_none(self):
        assert _ensure_list(None) == []


class TestResolveAuth:
    def _collector(self, env: dict) -> ApiCollector:
        return ApiCollector(_FakeRequester(), env=env)

    def test_header_no_prefix(self):
        src = SourceEntry(
            name="s", url="https://x", auth=AuthConfig(header="x-api-key", env="FAKE_KEY")
        )
        col = self._collector({"FAKE_KEY": "abc123"})
        assert col._resolve_auth(src) == {"x-api-key": "abc123"}

    def test_header_with_prefix(self):
        src = SourceEntry(
            name="s",
            url="https://x",
            auth=AuthConfig(header="Authorization", env="FAKE_KEY", prefix="Bearer "),
        )
        col = self._collector({"FAKE_KEY": "fc-xyz"})
        assert col._resolve_auth(src) == {"Authorization": "Bearer fc-xyz"}

    def test_empty_env_returns_no_headers(self):
        src = SourceEntry(
            name="s",
            url="https://x",
            auth=AuthConfig(header="Authorization", env="FAKE_KEY", prefix="Bearer "),
        )
        col = self._collector({})  # FAKE_KEY absent
        assert col._resolve_auth(src) == {}


class TestCollectThroughRequester:
    def test_basic_get_yields_records(self):
        resp = _ok_response('{"data": [{"title": "A"}, {"title": "B"}]}')
        req = _FakeRequester(resp)
        col = ApiCollector(req, env={})

        source = SourceEntry(name="s", url="https://x")
        entry = CollectorEntry(name="t", type="api", source="s", endpoint="/q", extract="data")
        records = list(col.collect(entry, source))
        assert [r["title"] for r in records] == ["A", "B"]

        # Requester was called exactly once with GET
        assert len(req.calls) == 1
        assert req.calls[0]["method"] == "GET"
        assert req.calls[0]["url"] == "https://x/q"

    def test_post_with_body(self):
        resp = _ok_response('{"results": [{"ok": true}]}')
        req = _FakeRequester(resp)
        col = ApiCollector(req, env={})

        source = SourceEntry(name="exa", url="https://api.exa.ai")
        entry = CollectorEntry(
            name="search",
            type="api",
            source="exa",
            endpoint="/search",
            method="POST",
            body={"query": "transformer attention", "numResults": 5},
            extract="results",
        )
        list(col.collect(entry, source))
        assert req.calls[0]["method"] == "POST"
        assert req.calls[0]["json_body"] == {"query": "transformer attention", "numResults": 5}

    def test_get_without_body(self):
        resp = _ok_response('{"data": [{"x": 1}]}')
        req = _FakeRequester(resp)
        col = ApiCollector(req, env={})

        source = SourceEntry(name="s", url="https://x")
        entry = CollectorEntry(name="g", type="api", source="s", endpoint="/q", extract="data")
        list(col.collect(entry, source))
        assert req.calls[0]["json_body"] is None

    def test_templated_body_end_to_end(self):
        resp = _ok_response('{"results": [{"ok": true}]}')
        req = _FakeRequester(resp)
        col = ApiCollector(req, env={})

        source = SourceEntry(name="exa", url="https://api.exa.ai")
        entry = CollectorEntry(
            name="search",
            type="api",
            source="exa",
            endpoint="/search",
            method="POST",
            params={"topic": "state space models"},
            body={"query": "{topic}", "numResults": 10},
            extract="results",
        )
        list(col.collect(entry, source))
        assert req.calls[0]["json_body"] == {"query": "state space models", "numResults": 10}

    def test_missing_placeholder_raises_before_request(self):
        req = _FakeRequester()  # no canned response; should never be called
        col = ApiCollector(req, env={})

        source = SourceEntry(name="exa", url="https://api.exa.ai")
        entry = CollectorEntry(
            name="search",
            type="api",
            source="exa",
            endpoint="/search",
            method="POST",
            params={"topic": "resolved"},
            body={"query": "{topic}", "missing": "{nowhere}"},
            extract="results",
        )
        with pytest.raises(CollectionError, match="unresolved placeholder"):
            list(col.collect(entry, source))
        assert req.calls == [], "Requester must not be invoked when body has unresolved vars"


class TestSubstituteUnified:
    def test_string_branch(self):
        assert substitute("hello {name}", {"name": "world"}) == "hello world"

    def test_flat_string(self):
        assert substitute({"q": "{topic}"}, {"topic": "attention"}) == {"q": "attention"}

    def test_preserves_non_strings(self):
        body = {"q": "{topic}", "n": 10, "flag": True, "nothing": None}
        out = substitute(body, {"topic": "x"})
        assert out == {"q": "x", "n": 10, "flag": True, "nothing": None}

    def test_nested_dict(self):
        assert substitute(
            {"contents": {"text": True, "filter": "{domain}"}}, {"domain": "arxiv.org"}
        ) == {"contents": {"text": True, "filter": "arxiv.org"}}

    def test_nested_list(self):
        assert substitute(
            {"includeDomains": ["{primary}", "secondary.com"]}, {"primary": "example.com"}
        ) == {"includeDomains": ["example.com", "secondary.com"]}

    def test_unresolved_placeholder_stays_literal(self):
        assert substitute({"q": "{missing}"}, {}) == {"q": "{missing}"}


class TestFindUnresolved:
    def test_empty_when_resolved(self):
        assert find_unresolved({"q": "hello"}) == []

    def test_finds_flat(self):
        assert find_unresolved({"q": "{topic}"}) == ["topic"]

    def test_finds_nested(self):
        assert sorted(find_unresolved({"a": {"b": "{x}"}, "c": ["{y}", "z"]})) == ["x", "y"]

    def test_ignores_non_strings(self):
        assert find_unresolved({"n": 10, "ok": True, "none": None}) == []


@pytest.mark.parametrize(
    "method,expected",
    [("GET", "GET"), ("POST", "POST"), ("PUT", "PUT"), ("PATCH", "PATCH"), ("DELETE", "DELETE")],
)
def test_method_expanded(method, expected):
    entry = CollectorEntry(name="x", type="api", endpoint="/y", method=method)
    assert entry.method == expected
