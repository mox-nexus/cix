"""Tests for CliCollector — subprocess → records."""

import tempfile
from pathlib import Path

import pytest
from recon.adapters._out.cli_collector import CliCollector, _parse_stdout
from recon.domain.exceptions import CollectionError
from recon.domain.models import CollectorEntry, SourceEntry


class TestParseStdout:
    def test_jsonl(self):
        stdout = '{"a": 1}\n{"a": 2}\n'
        records = _parse_stdout(stdout)
        assert len(records) == 2
        assert records[0] == {"a": 1}

    def test_text_fallback(self):
        stdout = "line one\nline two\n"
        records = _parse_stdout(stdout)
        assert len(records) == 2
        assert records[0] == {"line_number": 1, "line": "line one"}

    def test_empty(self):
        assert _parse_stdout("") == []
        assert _parse_stdout("  \n  ") == []


class TestCliCollector:
    def test_basic_jsonl(self):
        entry = CollectorEntry(
            name="test",
            type="cli",
            run='printf \'{"x": 1}\\n{"x": 2}\\n\'',
        )
        records = CliCollector().collect(entry, None)
        assert len(records) == 2
        assert records[0]["x"] == 1

    def test_text_output(self):
        entry = CollectorEntry(
            name="lines",
            type="cli",
            run="echo 'hello world'",
        )
        records = CliCollector().collect(entry, None)
        assert len(records) == 1
        assert "line" in records[0]

    def test_patterns(self):
        entry = CollectorEntry(
            name="pats",
            type="cli",
            run="echo '{pattern}'",
            patterns=["alpha", "beta"],
        )
        records = CliCollector().collect(entry, None)
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
        records = CliCollector().collect(entry, source)
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
            records = CliCollector().collect(entry, source)
            assert "found" in records[0]["line"]

    def test_normalize(self):
        entry = CollectorEntry(
            name="norm",
            type="cli",
            run='printf \'{"nested": {"val": 42}}\\n\'',
            normalize={"value": "nested.val"},
        )
        records = CliCollector().collect(entry, None)
        assert records[0]["value"] == 42

    def test_no_run_raises(self):
        entry = CollectorEntry(name="bad", type="cli")
        with pytest.raises(CollectionError, match="no 'run' field"):
            CliCollector().collect(entry, None)

    def test_failed_command_raises(self):
        entry = CollectorEntry(
            name="fail",
            type="cli",
            run="exit 2",
        )
        with pytest.raises(CollectionError, match="exit 2"):
            CliCollector().collect(entry, None)

    def test_empty_output(self):
        """Command with no stdout returns empty list."""
        entry = CollectorEntry(
            name="empty",
            type="cli",
            run="true",
        )
        records = CliCollector().collect(entry, None)
        assert records == []
