"""Tests for ApiCollector — helpers."""

from recon.adapters._out.api_collector import _ensure_list, _extract


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
