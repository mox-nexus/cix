"""Integration tests for the Recon dispatch loop."""

import json
import tempfile
from pathlib import Path

import pytest
import yaml
from recon.adapters._out.api_collector import ApiCollector
from recon.adapters._out.cli_collector import CliCollector
from recon.adapters._out.http_requester import HttpxRequester
from recon.adapters._out.web_collector import WebCollector
from recon.application.recon import run, substitute
from recon.application.utilization import RateLimiter
from recon.domain.converters import ConversionResult
from recon.domain.exceptions import ReconError
from recon.domain.models import ReconConfig


class _NoOpConverter:
    """Test-only converter that returns an empty ConversionResult.

    `run()` tests focus on dispatch/sink/error paths; they never exercise
    the web collector, so the converter never gets called.
    """

    def convert(self, content, content_type, url):
        return ConversionResult(title="", text="")


def _collectors():
    req = HttpxRequester(RateLimiter())
    return {
        "cli": CliCollector(),
        "api": ApiCollector(req),
        "web": WebCollector(req, _NoOpConverter()),
    }


class TestSubstitute:
    def test_basic(self):
        assert substitute("/search/{query}", {"query": "test"}) == "/search/test"

    def test_missing_key(self):
        assert substitute("{missing}", {}) == "{missing}"

    def test_multiple(self):
        assert substitute("{a}/{b}", {"a": "1", "b": "2"}) == "1/2"


class TestReconRun:
    def test_single_cli_collector(self):
        config = ReconConfig.model_validate(
            {
                "collectors": [
                    {"name": "test", "type": "cli", "run": 'echo \'{"k": "v"}\''},
                ],
            }
        )
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            archive, _ = run(config, _collectors(), mission)
            assert archive.is_dir()
            assert (archive / "test.jsonl").exists()
            assert (archive / "meta.yaml").exists()

    def test_jsonl_content(self):
        config = ReconConfig.model_validate(
            {
                "collectors": [
                    {"name": "data", "type": "cli", "run": 'printf \'{"k": "v"}\\n\''},
                ],
            }
        )
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            archive, _ = run(config, _collectors(), mission)
            lines = (archive / "data.jsonl").read_text().strip().splitlines()
            records = [json.loads(line) for line in lines]
            assert len(records) == 1
            assert records[0]["k"] == "v"

    def test_multiple_collectors(self):
        config = ReconConfig.model_validate(
            {
                "collectors": [
                    {"name": "first", "type": "cli", "run": "echo one"},
                    {"name": "second", "type": "cli", "run": "echo two"},
                ],
            }
        )
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            archive, _ = run(config, _collectors(), mission)
            assert (archive / "first.jsonl").exists()
            assert (archive / "second.jsonl").exists()

    def test_fan_out_across_catalog(self):
        """No source on collector → runs against all catalog entries."""
        config = ReconConfig.model_validate(
            {
                "catalog": [
                    {"name": "a", "type": "local", "url": "/tmp"},
                    {"name": "b", "type": "local", "url": "/tmp"},
                ],
                "collectors": [
                    {"name": "scan", "type": "cli", "run": "echo hello"},
                ],
            }
        )
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            archive, _ = run(config, _collectors(), mission)
            assert (archive / "scan-a.jsonl").exists()
            assert (archive / "scan-b.jsonl").exists()
            assert not (archive / "scan.jsonl").exists()

    def test_pinned_source_no_fan_out(self):
        """Collector with source= runs against that source only."""
        config = ReconConfig.model_validate(
            {
                "catalog": [
                    {"name": "s2", "url": "https://api.semanticscholar.org"},
                    {"name": "arxiv", "url": "https://export.arxiv.org"},
                ],
                "collectors": [
                    {"name": "test", "type": "cli", "run": "echo hello", "source": "s2"},
                ],
            }
        )
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            archive, _ = run(config, _collectors(), mission)
            assert (archive / "test.jsonl").exists()
            assert not (archive / "test-arxiv.jsonl").exists()

    def test_no_catalog_no_fan_out(self):
        """No catalog → collector runs once with no source."""
        config = ReconConfig.model_validate(
            {
                "collectors": [
                    {"name": "solo", "type": "cli", "run": "echo hello"},
                ],
            }
        )
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            archive, _ = run(config, _collectors(), mission)
            assert (archive / "solo.jsonl").exists()

    def test_source_ref_error_recorded(self):
        """Missing source reference records error, doesn't crash."""
        config = ReconConfig.model_validate(
            {
                "collectors": [
                    {"name": "bad", "type": "api", "source": "nonexistent", "endpoint": "/x"},
                    {"name": "ok", "type": "cli", "run": "echo hi"},
                ],
            }
        )
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            archive, _ = run(config, _collectors(), mission)
            meta = yaml.safe_load((archive / "meta.yaml").read_text())
            assert meta["collectors"][0]["status"] == "error"
            assert "nonexistent" in meta["collectors"][0]["error"]
            # Second collector still ran
            assert meta["collectors"][1]["status"] == "ok"

    def test_meta_yaml_content(self):
        config = ReconConfig.model_validate(
            {
                "collectors": [
                    {"name": "meta-test", "type": "cli", "run": "echo hi"},
                ],
            }
        )
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            archive, _ = run(config, _collectors(), mission)
            meta = yaml.safe_load((archive / "meta.yaml").read_text())
            assert "timestamp" in meta
            assert meta["collectors"][0]["name"] == "meta-test"
            assert meta["collectors"][0]["status"] == "ok"
            assert "records" in meta["collectors"][0]

    def test_collector_error_recorded(self):
        config = ReconConfig.model_validate(
            {
                "collectors": [
                    {"name": "fail", "type": "cli", "run": "exit 2"},
                    {"name": "ok", "type": "cli", "run": "echo hi"},
                ],
            }
        )
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            archive, _ = run(config, _collectors(), mission)
            meta = yaml.safe_load((archive / "meta.yaml").read_text())
            assert meta["collectors"][0]["status"] == "error"
            assert meta["collectors"][1]["status"] == "ok"
            assert (archive / "ok.jsonl").exists()

    def test_archive_directory_structure(self):
        config = ReconConfig.model_validate(
            {
                "collectors": [
                    {"name": "t", "type": "cli", "run": "echo hi"},
                ],
            }
        )
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "my-mission"
            mission.mkdir()
            archive, _ = run(config, _collectors(), mission)
            assert archive.parent.name == "archive"
            assert archive.parent.parent == mission

    def test_unknown_collector_type_recorded(self):
        """Unregistered type gets error in meta, doesn't crash."""
        config = ReconConfig.model_validate(
            {
                "collectors": [
                    {"name": "ok", "type": "cli", "run": "echo hi"},
                ],
            }
        )
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            archive, _ = run(config, {}, mission)  # empty registry
            meta = yaml.safe_load((archive / "meta.yaml").read_text())
            assert meta["collectors"][0]["status"] == "error"
            assert "No collector registered" in meta["collectors"][0]["error"]

    def test_empty_collector_output(self):
        """Empty records get _empty sentinel."""
        config = ReconConfig.model_validate(
            {
                "collectors": [
                    {"name": "empty", "type": "cli", "run": "true"},
                ],
            }
        )
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            archive, _ = run(config, _collectors(), mission)
            lines = (archive / "empty.jsonl").read_text().strip().splitlines()
            records = [json.loads(line) for line in lines]
            assert records == [{"_empty": True}]


class TestCollisionDetection:
    def test_pinned_and_fanout_collide(self):
        """Fan-out of `foo` over source `arxiv` produces `foo-arxiv`,
        same name as a pinned collector `foo-arxiv`. Pre-flight must catch it."""
        config = ReconConfig.model_validate(
            {
                "catalog": [{"name": "arxiv", "type": "local", "url": "/tmp"}],
                "collectors": [
                    {"name": "foo", "type": "cli", "run": "echo hi"},
                    {"name": "foo-arxiv", "type": "cli", "source": "arxiv", "run": "echo hi"},
                ],
            }
        )
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            with pytest.raises(ReconError, match="Output name collision"):
                run(config, _collectors(), mission)
            # No archive dir should have been created
            assert not (mission / "archive").exists()


class TestAtomicJsonlWrite:
    def test_tmp_is_cleaned_up_on_success(self):
        config = ReconConfig.model_validate(
            {"collectors": [{"name": "t", "type": "cli", "run": "echo '{\"a\": 1}'"}]}
        )
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            archive, _ = run(config, _collectors(), mission)
            # final file exists, no lingering .tmp
            assert (archive / "t.jsonl").exists()
            assert not (archive / "t.jsonl.tmp").exists()


class TestIncompleteSentinel:
    def test_sentinel_on_collector_error(self):
        """A failed collector should produce a .incomplete sentinel so
        downstream readers know the archive isn't fully trustworthy."""
        config = ReconConfig.model_validate(
            {
                "collectors": [
                    {"name": "ok", "type": "cli", "run": "echo '{\"a\": 1}'"},
                    {"name": "bad", "type": "cli", "run": "exit 2"},
                ],
            }
        )
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            archive, results = run(config, _collectors(), mission)
            statuses = {r["name"]: r["status"] for r in results}
            assert statuses == {"ok": "ok", "bad": "error"}
            assert (archive / ".incomplete").exists()
            assert (archive / "meta.yaml").exists()

    def test_no_sentinel_when_all_ok(self):
        config = ReconConfig.model_validate(
            {"collectors": [{"name": "ok", "type": "cli", "run": "echo '{\"a\": 1}'"}]}
        )
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            archive, _ = run(config, _collectors(), mission)
            assert not (archive / ".incomplete").exists()


class TestPreserveRaw:
    def test_disabled_by_default(self):
        """preserve_raw: false → no raw/ subdir in archive."""
        config = ReconConfig.model_validate(
            {"collectors": [{"name": "t", "type": "cli", "run": "echo '{\"a\": 1}'"}]}
        )
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            archive, _ = run(config, _collectors(), mission)
            assert not (archive / "raw").exists()

    def test_cli_raw_captured_with_hash(self):
        """preserve_raw: true → stdout lands in raw/<name>/body + meta.yaml w/ sha256."""
        import hashlib

        import yaml as _yaml

        config = ReconConfig.model_validate(
            {
                "preserve_raw": True,
                "collectors": [
                    {"name": "echoer", "type": "cli", "run": 'printf \'{"a": 1}\\n{"a": 2}\\n\''},
                ],
            }
        )
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            archive, _ = run(config, _collectors(), mission)

            raw_body = archive / "raw" / "echoer" / "body"
            raw_meta = archive / "raw" / "echoer" / "meta.yaml"
            assert raw_body.exists()
            assert raw_meta.exists()

            body_bytes = raw_body.read_bytes()
            assert b'{"a": 1}' in body_bytes
            assert b'{"a": 2}' in body_bytes

            meta = _yaml.safe_load(raw_meta.read_text())
            assert meta["type"] == "cli"
            assert meta["collector"] == "echoer"
            assert meta["exit_code"] == 0
            assert meta["bytes"] == len(body_bytes)
            assert meta["sha256"] == hashlib.sha256(body_bytes).hexdigest()

    def test_jsonl_still_produced_alongside_raw(self):
        """Raw doesn't replace processed output — both exist."""
        config = ReconConfig.model_validate(
            {
                "preserve_raw": True,
                "collectors": [
                    {"name": "t", "type": "cli", "run": "echo '{\"a\": 1}'"},
                ],
            }
        )
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            archive, _ = run(config, _collectors(), mission)
            assert (archive / "t.jsonl").exists()
            assert (archive / "raw" / "t" / "body").exists()


class TestEventCallback:
    def test_emits_ok_and_error_events(self):
        events: list[dict] = []
        config = ReconConfig.model_validate(
            {
                "collectors": [
                    {"name": "ok", "type": "cli", "run": "echo '{\"a\": 1}'"},
                    {"name": "bad", "type": "cli", "run": "exit 2"},
                ],
            }
        )
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            run(config, _collectors(), mission, on_event=events.append)
        kinds = [e["kind"] for e in events]
        assert "ok" in kinds and "error" in kinds
        ok_event = next(e for e in events if e["kind"] == "ok")
        assert ok_event["name"] == "ok"
        assert ok_event["records"] == 1
