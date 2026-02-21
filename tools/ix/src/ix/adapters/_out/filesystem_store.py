"""Filesystem storage adapter — YAML+MD in, JSONL out.

Directory convention (lab as workspace):
  <lab>/
    <experiment>/experiment.yaml        — experiment config
    <experiment>/tasks/*.md             — probes (frontmatter + body)
    <experiment>/subjects/*.md          — subjects (frontmatter + body)
    <experiment>/results/trials.jsonl   — trial results
    <experiment>/results/summary-*.json — summaries

Backward compat: falls back to cases/ if tasks/ doesn't exist.
"""

from datetime import UTC, datetime
from pathlib import Path

import frontmatter
import yaml

from ix.domain.types import Probe, Subject
from ix.eval.models import ExperimentConfig, ExperimentResults, TrialRecord


class FilesystemStore:
    """Loads experiments from YAML+MD, persists results as JSONL.

    The workspace is a lab directory — experiments are direct children.
    """

    def __init__(self, workspace: Path):
        self._workspace = workspace

    def load_experiment(self, path: Path) -> ExperimentConfig:
        """Load experiment from a directory containing experiment.yaml + tasks/*.md."""
        config_path = path / "experiment.yaml"
        if not config_path.exists():
            raise FileNotFoundError(f"No experiment.yaml in {path}")

        with open(config_path) as f:
            config = yaml.safe_load(f)

        probes = self._load_probes(path)
        subjects = self._load_subjects(path, config)

        # Normalize sensor: string shorthand → config dict
        raw_sensor = config.get("sensor", "activation")
        sensor_config = {"type": raw_sensor} if isinstance(raw_sensor, str) else raw_sensor

        return ExperimentConfig(
            name=config.get("name", path.name),
            description=config.get("description", ""),
            subjects=tuple(subjects),
            sensor=sensor_config,
            trials=config.get("trials", 5),
            probes=tuple(probes),
        )

    def _load_probes(self, exp_path: Path) -> list[Probe]:
        """Load probes from tasks/ (preferred) or cases/ (backward compat).

        All frontmatter goes into metadata. id is extracted as top-level.
        """
        tasks_dir = exp_path / "tasks"
        cases_dir = exp_path / "cases"
        probe_dir = tasks_dir if tasks_dir.exists() else cases_dir

        if not probe_dir.exists():
            return []

        probes = []
        for md_path in sorted(probe_dir.glob("*.md")):
            post = frontmatter.load(str(md_path))
            metadata = dict(post.metadata)
            probe_id = metadata.pop("id", md_path.stem)
            prompt = post.content.strip()
            probes.append(Probe(id=probe_id, prompt=prompt, metadata=metadata))
        return probes

    def _load_subjects(self, exp_path: Path, config: dict) -> list[Subject]:
        """Load subjects from subjects/ directory or experiment.yaml config.

        subjects/ directory takes precedence. Falls back to YAML subjects list.
        """
        subjects_dir = exp_path / "subjects"
        if subjects_dir.exists():
            subjects = []
            for md_path in sorted(subjects_dir.glob("*.md")):
                post = frontmatter.load(str(md_path))
                meta = dict(post.metadata)
                name = meta.pop("name", md_path.stem)
                description = meta.pop("description", "")
                subjects.append(
                    Subject(
                        name=name,
                        description=description,
                        config={**meta, "system_prompt": post.content.strip()},
                    )
                )
            return subjects

        # Fall back to YAML config
        if raw_subjects := config.get("subjects"):
            return [
                Subject(
                    name=s["name"] if isinstance(s, dict) else s,
                    description=s.get("description", "") if isinstance(s, dict) else "",
                    config=s.get("config", {}) if isinstance(s, dict) else {},
                )
                for s in raw_subjects
            ]
        return []

    def list_experiments(self, base: Path) -> list[Path]:
        """Find all directories containing experiment.yaml."""
        experiments = []
        if not base.exists():
            return experiments
        for candidate in sorted(base.iterdir()):
            if candidate.is_dir() and (candidate / "experiment.yaml").exists():
                experiments.append(candidate)
        return experiments

    def append_result(self, experiment_name: str, result: TrialRecord) -> None:
        """Append a trial record to the JSONL log."""
        results_dir = self._workspace / experiment_name / "results"
        results_dir.mkdir(parents=True, exist_ok=True)

        log_path = results_dir / "trials.jsonl"
        with open(log_path, "a") as f:
            f.write(result.model_dump_json() + "\n")

    def save_summary(self, experiment_name: str, results: ExperimentResults) -> Path:
        """Save experiment summary as JSON."""
        results_dir = self._workspace / experiment_name / "results"
        results_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        summary_path = results_dir / f"summary-{timestamp}.json"

        with open(summary_path, "w") as f:
            f.write(results.model_dump_json(indent=2))

        latest_path = results_dir / "summary-latest.json"
        with open(latest_path, "w") as f:
            f.write(results.model_dump_json(indent=2))

        return summary_path
