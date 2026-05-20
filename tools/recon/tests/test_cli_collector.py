"""Tests for CliCollector — subprocess → streaming records."""

import tempfile
from pathlib import Path

import pytest
from recon.adapters._out.cli_collector import CliCollector, _parse_line
from recon.domain.exceptions import CollectionError
from recon.domain.models import CollectorEntry, SourceEntry


class TestParseLine:
    def test_jsonl(self):
        assert _parse_line('{"a": 1}', 1) == {"a": 1}

    def test_text_fallback(self):
        assert _parse_line("line one", 3) == {"line_number": 3, "line": "line one"}

    def test_empty(self):
        assert _parse_line("", 1) is None
        assert _parse_line("   ", 1) is None

    def test_non_dict_json_falls_back(self):
        """JSON arrays/numbers aren't records — treat as text line."""
        assert _parse_line("[1, 2, 3]", 1) == {"line_number": 1, "line": "[1, 2, 3]"}


class TestCliCollector:
    def test_basic_jsonl(self):
        entry = CollectorEntry(
            name="test",
            type="cli",
            run='printf \'{"x": 1}\\n{"x": 2}\\n\'',
        )
        records = list(CliCollector().collect(entry, None))
        assert len(records) == 2
        assert records[0]["x"] == 1

    def test_text_output(self):
        entry = CollectorEntry(
            name="lines",
            type="cli",
            run="echo 'hello world'",
        )
        records = list(CliCollector().collect(entry, None))
        assert len(records) == 1
        assert "line" in records[0]

    def test_patterns(self):
        entry = CollectorEntry(
            name="pats",
            type="cli",
            run="echo '{pattern}'",
            patterns=["alpha", "beta"],
        )
        records = list(CliCollector().collect(entry, None))
        assert len(records) == 2
        assert records[0]["_pattern"] == "alpha"
        assert records[1]["_pattern"] == "beta"

    def test_source_url_substitution(self):
        entry = CollectorEntry(
            name="url-test",
            type="cli",
            run="echo '{url}'",
        )
        source = SourceEntry(name="test", url="https://example.com")
        records = list(CliCollector().collect(entry, source))
        assert "https://example.com" in records[0]["line"]

    def test_source_as_cwd(self):
        """Local source URL is used as working directory."""
        with tempfile.TemporaryDirectory() as tmp:
            Path(tmp, "marker.txt").write_text("found")

            entry = CollectorEntry(
                name="cwd-test",
                type="cli",
                run="cat marker.txt",
            )
            source = SourceEntry(name="repo", type="local", url=tmp)
            records = list(CliCollector().collect(entry, source))
            assert "found" in records[0]["line"]

    def test_normalize(self):
        entry = CollectorEntry(
            name="norm",
            type="cli",
            run='printf \'{"nested": {"val": 42}}\\n\'',
            normalize={"value": "nested.val"},
        )
        records = list(CliCollector().collect(entry, None))
        assert records[0]["value"] == 42

    def test_no_run_raises(self):
        entry = CollectorEntry(name="bad", type="cli")
        with pytest.raises(CollectionError, match="no 'run' field"):
            list(CliCollector().collect(entry, None))

    def test_failed_command_raises(self):
        """Exit code other than 0/1 surfaces during iteration."""
        entry = CollectorEntry(
            name="fail",
            type="cli",
            run="exit 2",
        )
        with pytest.raises(CollectionError, match="exit 2"):
            list(CliCollector().collect(entry, None))

    def test_empty_output(self):
        """Command with no stdout yields nothing (dispatch loop adds sentinel)."""
        entry = CollectorEntry(
            name="empty",
            type="cli",
            run="true",
        )
        records = list(CliCollector().collect(entry, None))
        assert records == []

    def test_streaming_yields_lazily(self):
        """Generator shape — records are yielded as produced, not batched."""
        entry = CollectorEntry(
            name="streaming",
            type="cli",
            run='printf \'{"i": 1}\\n{"i": 2}\\n{"i": 3}\\n\'',
        )
        gen = CliCollector().collect(entry, None)
        # next() without list() proves it's a generator
        first = next(gen)
        assert first["i"] == 1
        rest = list(gen)
        assert [r["i"] for r in rest] == [2, 3]

    def test_generator_cleanup_on_abandonment(self):
        """Abandoning the iterator kills the subprocess (no leak)."""
        entry = CollectorEntry(
            name="longlived",
            type="cli",
            run="printf '{\"a\": 1}\\n' && sleep 10 && printf '{\"a\": 2}\\n'",
        )
        gen = CliCollector().collect(entry, None)
        next(gen)  # read first record
        gen.close()  # abandon — should kill subprocess
        # If the subprocess were still alive, this test would hang on teardown.
        # The actual assertion is implicit: test completes quickly.
