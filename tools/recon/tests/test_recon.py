"""Integration tests for the Recon dispatch loop."""

import json
import tempfile
from pathlib import Path

import yaml
from recon.adapters._out.api_collector import ApiCollector
from recon.adapters._out.cli_collector import CliCollector
from recon.adapters._out.web_collector import WebCollector
from recon.application.recon import run, substitute
from recon.application.utilization import RateLimiter
from recon.domain.models import ReconConfig


def _collectors():
    rl = RateLimiter()
    return {"cli": CliCollector(), "api": ApiCollector(rl), "web": WebCollector(rl)}


class TestSubstitute:
    def test_basic(self):
        assert substitute("/search/{query}", {"query": "test"}) == "/search/test"

    def test_missing_key(self):
        assert substitute("{missing}", {}) == "{missing}"

    def test_multiple(self):
        assert substitute("{a}/{b}", {"a": "1", "b": "2"}) == "1/2"


class TestReconRun:
    def test_single_cli_collector(self):
        config = ReconConfig.model_validate({
            "collectors": [
                {"name": "test", "type": "cli", "run": 'echo \'{"k": "v"}\''},
            ],
        })
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            archive = run(config, _collectors(), mission)
            assert archive.is_dir()
            assert (archive / "test.jsonl").exists()
            assert (archive / "meta.yaml").exists()

    def test_jsonl_content(self):
        config = ReconConfig.model_validate({
            "collectors": [
                {"name": "data", "type": "cli", "run": 'printf \'{"k": "v"}\\n\''},
            ],
        })
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            archive = run(config, _collectors(), mission)
            lines = (archive / "data.jsonl").read_text().strip().splitlines()
            records = [json.loads(line) for line in lines]
            assert len(records) == 1
            assert records[0]["k"] == "v"

    def test_multiple_collectors(self):
        config = ReconConfig.model_validate({
            "collectors": [
                {"name": "first", "type": "cli", "run": "echo one"},
                {"name": "second", "type": "cli", "run": "echo two"},
            ],
        })
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            archive = run(config, _collectors(), mission)
            assert (archive / "first.jsonl").exists()
            assert (archive / "second.jsonl").exists()

    def test_fan_out_across_catalog(self):
        """No source on collector → runs against all catalog entries."""
        config = ReconConfig.model_validate({
            "catalog": [
                {"name": "a", "type": "local", "url": "/tmp"},
                {"name": "b", "type": "local", "url": "/tmp"},
            ],
            "collectors": [
                {"name": "scan", "type": "cli", "run": "echo hello"},
            ],
        })
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            archive = run(config, _collectors(), mission)
            assert (archive / "scan-a.jsonl").exists()
            assert (archive / "scan-b.jsonl").exists()
            assert not (archive / "scan.jsonl").exists()

    def test_pinned_source_no_fan_out(self):
        """Collector with source= runs against that source only."""
        config = ReconConfig.model_validate({
            "catalog": [
                {"name": "s2", "url": "https://api.semanticscholar.org"},
                {"name": "arxiv", "url": "https://export.arxiv.org"},
            ],
            "collectors": [
                {"name": "test", "type": "cli", "run": "echo hello", "source": "s2"},
            ],
        })
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            archive = run(config, _collectors(), mission)
            assert (archive / "test.jsonl").exists()
            assert not (archive / "test-arxiv.jsonl").exists()

    def test_no_catalog_no_fan_out(self):
        """No catalog → collector runs once with no source."""
        config = ReconConfig.model_validate({
            "collectors": [
                {"name": "solo", "type": "cli", "run": "echo hello"},
            ],
        })
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            archive = run(config, _collectors(), mission)
            assert (archive / "solo.jsonl").exists()

    def test_source_ref_error_recorded(self):
        """Missing source reference records error, doesn't crash."""
        config = ReconConfig.model_validate({
            "collectors": [
                {"name": "bad", "type": "api", "source": "nonexistent", "endpoint": "/x"},
                {"name": "ok", "type": "cli", "run": "echo hi"},
            ],
        })
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            archive = run(config, _collectors(), mission)
            meta = yaml.safe_load((archive / "meta.yaml").read_text())
            assert meta["collectors"][0]["status"] == "error"
            assert "nonexistent" in meta["collectors"][0]["error"]
            # Second collector still ran
            assert meta["collectors"][1]["status"] == "ok"

    def test_meta_yaml_content(self):
        config = ReconConfig.model_validate({
            "collectors": [
                {"name": "meta-test", "type": "cli", "run": "echo hi"},
            ],
        })
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            archive = run(config, _collectors(), mission)
            meta = yaml.safe_load((archive / "meta.yaml").read_text())
            assert "timestamp" in meta
            assert meta["collectors"][0]["name"] == "meta-test"
            assert meta["collectors"][0]["status"] == "ok"
            assert "records" in meta["collectors"][0]

    def test_collector_error_recorded(self):
        config = ReconConfig.model_validate({
            "collectors": [
                {"name": "fail", "type": "cli", "run": "exit 2"},
                {"name": "ok", "type": "cli", "run": "echo hi"},
            ],
        })
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            archive = run(config, _collectors(), mission)
            meta = yaml.safe_load((archive / "meta.yaml").read_text())
            assert meta["collectors"][0]["status"] == "error"
            assert meta["collectors"][1]["status"] == "ok"
            assert (archive / "ok.jsonl").exists()

    def test_archive_directory_structure(self):
        config = ReconConfig.model_validate({
            "collectors": [
                {"name": "t", "type": "cli", "run": "echo hi"},
            ],
        })
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "my-mission"
            mission.mkdir()
            archive = run(config, _collectors(), mission)
            assert archive.parent.name == "archive"
            assert archive.parent.parent == mission

    def test_unknown_collector_type_recorded(self):
        """Unregistered type gets error in meta, doesn't crash."""
        config = ReconConfig.model_validate({
            "collectors": [
                {"name": "ok", "type": "cli", "run": "echo hi"},
            ],
        })
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            archive = run(config, {}, mission)  # empty registry
            meta = yaml.safe_load((archive / "meta.yaml").read_text())
            assert meta["collectors"][0]["status"] == "error"
            assert "No collector registered" in meta["collectors"][0]["error"]

    def test_empty_collector_output(self):
        """Empty records get _empty sentinel."""
        config = ReconConfig.model_validate({
            "collectors": [
                {"name": "empty", "type": "cli", "run": "true"},
            ],
        })
        with tempfile.TemporaryDirectory() as tmp:
            mission = Path(tmp) / "m"
            mission.mkdir()
            archive = run(config, _collectors(), mission)
            lines = (archive / "empty.jsonl").read_text().strip().splitlines()
            records = [json.loads(line) for line in lines]
            assert records == [{"_empty": True}]
