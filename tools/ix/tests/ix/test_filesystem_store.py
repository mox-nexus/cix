"""Tests for FilesystemStore — YAML+MD loading, JSONL persistence.

Workspace = lab directory. Experiments are direct children.
"""

import json
from pathlib import Path

import pytest
from ix.adapters._out.filesystem_store import FilesystemStore
from ix.domain.types import Reading
from ix.eval.models import (
    ExperimentResults,
    TrialRecord,
)
from matrix import AgentResponse


@pytest.fixture
def lab(tmp_path: Path) -> Path:
    """Lab directory (the workspace)."""
    return tmp_path


@pytest.fixture
def store(lab: Path) -> FilesystemStore:
    return FilesystemStore(lab)


@pytest.fixture
def sample_experiment(lab: Path) -> Path:
    """Create a minimal experiment directly in the lab."""
    exp_dir = lab / "test-exp"
    exp_dir.mkdir()

    (exp_dir / "experiment.yaml").write_text(
        "name: test-exp\n"
        "description: A test experiment\n"
        "subjects:\n"
        "  - name: build-eval\n"
        "trials: 3\n"
    )

    cases_dir = exp_dir / "cases"
    cases_dir.mkdir()

    (cases_dir / "must-001.md").write_text(
        "---\nid: must-001\nexpectation: must_trigger\n---\nHow do I write evals?\n"
    )

    (cases_dir / "not-001.md").write_text(
        "---\n"
        "id: not-001\n"
        "expectation: should_not_trigger\n"
        "---\n"
        "Write a Python function to sort a list\n"
    )

    return exp_dir


class TestLoadExperiment:
    def test_loads_config(self, store: FilesystemStore, sample_experiment: Path):
        exp = store.load_experiment(sample_experiment)
        assert exp.name == "test-exp"
        assert exp.subjects[0].name == "build-eval"
        assert exp.trials == 3

    def test_loads_probes(self, store: FilesystemStore, sample_experiment: Path):
        exp = store.load_experiment(sample_experiment)
        assert len(exp.probes) == 2
        assert exp.probes[0].id == "must-001"
        assert exp.probes[0].metadata["expectation"] == "must_trigger"
        assert "evals" in exp.probes[0].prompt

    def test_probes_sorted_by_filename(self, store: FilesystemStore, sample_experiment: Path):
        exp = store.load_experiment(sample_experiment)
        assert exp.probes[0].id == "must-001"
        assert exp.probes[1].id == "not-001"

    def test_missing_config_raises(self, store: FilesystemStore, lab: Path):
        with pytest.raises(FileNotFoundError):
            store.load_experiment(lab / "nonexistent")


class TestListExperiments:
    def test_finds_experiments(self, store: FilesystemStore, sample_experiment: Path, lab: Path):
        experiments = store.list_experiments(lab)
        assert len(experiments) == 1
        assert experiments[0].name == "test-exp"

    def test_empty_lab(self, store: FilesystemStore, lab: Path):
        experiments = store.list_experiments(lab)
        assert experiments == []


class TestAppendResult:
    def test_creates_jsonl(self, store: FilesystemStore, lab: Path):
        result = TrialRecord(
            probe_id="must-001",
            trial=0,
            observation=AgentResponse(content="test"),
            reading=Reading(
                sensor_name="activation",
                probe_id="must-001",
                trial_index=0,
                passed=True,
            ),
        )
        store.append_result("test-exp", result)

        jsonl_path = lab / "test-exp" / "results" / "trials.jsonl"
        assert jsonl_path.exists()
        line = json.loads(jsonl_path.read_text().strip())
        assert line["probe_id"] == "must-001"

    def test_appends_multiple(self, store: FilesystemStore, lab: Path):
        for i in range(3):
            store.append_result(
                "test-exp",
                TrialRecord(
                    probe_id="must-001",
                    trial=i,
                    observation=AgentResponse(content=f"resp-{i}"),
                    reading=Reading(
                        sensor_name="activation",
                        probe_id="must-001",
                        trial_index=i,
                        passed=True,
                    ),
                ),
            )

        jsonl_path = lab / "test-exp" / "results" / "trials.jsonl"
        lines = jsonl_path.read_text().strip().split("\n")
        assert len(lines) == 3


class TestSaveSummary:
    def test_creates_summary(self, store: FilesystemStore, lab: Path):
        results = ExperimentResults(
            experiment_name="test-exp",
            precision=1.0,
            recall=1.0,
            f1=1.0,
            tp=5,
            fp=0,
            fn=0,
            tn=3,
        )
        path = store.save_summary("test-exp", results)
        assert path.exists()
        data = json.loads(path.read_text())
        assert data["f1"] == 1.0

    def test_creates_latest(self, store: FilesystemStore, lab: Path):
        results = ExperimentResults(experiment_name="test-exp")
        store.save_summary("test-exp", results)
        latest = lab / "test-exp" / "results" / "summary-latest.json"
        assert latest.exists()
