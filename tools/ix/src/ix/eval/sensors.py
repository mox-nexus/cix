"""Eval sensors — measure trial responses for evaluation experiments.

Each sensor implements Sensor protocol: sense(trial) -> list[Reading].
Each sensor has a typed Config model (Pydantic) for validated construction.
Ground truth is injected at construction by the service layer.
"""

from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path
from typing import Any

from matrix import AgentResponse
from pydantic import BaseModel

from ix.domain.types import Probe, Reading, Trial

# --- Composite ---


class CompositeSensor:
    """Runs N sensors, flattens readings. Caller sees one Sensor.

    Standard composite pattern. Built by the composition layer from
    experiment config when multiple sensors are configured.
    Single sensor? Skip the wrapper — it already satisfies the protocol.
    """

    def __init__(self, sensors: list) -> None:
        if not sensors:
            raise ValueError("CompositeSensor requires at least one sensor")
        self._sensors = sensors

    @property
    def name(self) -> str:
        return "+".join(s.name for s in self._sensors)

    def sense(self, trial: Trial) -> list[Reading]:
        return [r for s in self._sensors for r in s.sense(trial)]


# --- Config Models ---


class ActivationSensorConfig(BaseModel, frozen=True, extra="forbid"):
    """Config for ActivationSensor. Validated from experiment.yaml sensor section."""

    type: str = "activation"
    expected_skill: str = "build-eval"


class FunctionTestSensorConfig(BaseModel, frozen=True, extra="forbid"):
    """Config for FunctionTestSensor. Validated from experiment.yaml sensor section."""

    type: str = "function-test"
    timeout: int = 30


# --- Sensors ---


class ActivationSensor:
    """Checks whether the expected skill activated in the response.

    Configured with expected_skill at construction. Ground truth is
    the skill name — same for all probes in the experiment.
    """

    Config = ActivationSensorConfig

    def __init__(self, expected_skill: str = "build-eval"):
        self._expected_skill = expected_skill

    @classmethod
    def from_config(
        cls,
        config: ActivationSensorConfig,
        probes: tuple[Probe, ...] = (),
        **kwargs: Any,
    ) -> ActivationSensor:
        return cls(expected_skill=config.expected_skill)

    @property
    def name(self) -> str:
        return "activation"

    def sense(self, trial: Trial) -> list[Reading]:
        """Check if any tool call activated the expected skill."""
        response: AgentResponse = trial.response

        activated = any(
            self._expected_skill in tc.get("input", {}).get("skill", "")
            or "eval" in tc.get("input", {}).get("skill", "").lower()
            for tc in response.tool_calls
            if tc.get("name") == "Skill"
        )

        return [
            Reading(
                sensor_name=self.name,
                probe_id=trial.probe_id,
                trial_index=trial.trial_index,
                passed=activated,
                score=1.0 if activated else 0.0,
                details=f"skill={self._expected_skill}, activated={activated}",
            )
        ]


class FunctionTestSensor:
    """Runs generated code against test cases.

    Ground truth (test_cases + function_name per probe) is injected
    at construction via the ground_truth registry. The service layer
    extracts this from probe metadata and passes it in.

    The sensor:
    1. Extracts code from trial.response
    2. Loads it into an isolated module namespace
    3. Runs each test case: fn(input) == expected
    4. Returns a Reading with pass/fail + score + details
    """

    Config = FunctionTestSensorConfig

    def __init__(
        self,
        *,
        ground_truth: dict[str, dict] | None = None,
        timeout: int = 30,
    ):
        self._ground_truth = ground_truth or {}
        self._timeout = timeout

    @classmethod
    def from_config(
        cls,
        config: FunctionTestSensorConfig,
        probes: tuple[Probe, ...] = (),
        **kwargs: Any,
    ) -> FunctionTestSensor:
        ground_truth = {
            p.id: {
                "function_name": p.metadata.get("function_name", ""),
                "test_cases": p.metadata.get("test_cases", []),
            }
            for p in probes
        }
        return cls(ground_truth=ground_truth, timeout=config.timeout)

    @property
    def name(self) -> str:
        return "function-test"

    def sense(self, trial: Trial) -> list[Reading]:
        """Extract code from response, run against probe's test cases."""
        truth = self._ground_truth.get(trial.probe_id, {})
        test_cases = truth.get("test_cases", [])
        function_name = truth.get("function_name", "")

        code = self._extract_code(trial.response)
        if not code:
            return [
                self._reading(trial, passed=False, score=0.0, details="no code found in response")
            ]

        if not test_cases or not function_name:
            return [
                self._reading(
                    trial,
                    passed=False,
                    score=0.0,
                    details=f"missing ground truth for probe '{trial.probe_id}'",
                )
            ]

        try:
            fn = self._load_function(code, function_name)
        except Exception as e:
            return [self._reading(trial, passed=False, score=0.0, details=f"load error: {e}")]

        passed, failures = 0, []
        for tc in test_cases:
            try:
                inp = tc["input"]
                result = fn(*inp) if isinstance(inp, list) else fn(inp)
                if result == tc["expected"]:
                    passed += 1
                else:
                    desc = tc.get("description", "?")
                    failures.append(f"{desc}: got {result!r}, expected {tc['expected']!r}")
            except Exception as e:
                desc = tc.get("description", "?")
                failures.append(f"{desc}: {type(e).__name__}: {e}")

        total = len(test_cases)
        score = passed / total if total else 0.0
        return [
            self._reading(
                trial,
                passed=(passed == total),
                score=score,
                metrics={
                    "tests_passed": passed,
                    "tests_failed": total - passed,
                    "tests_total": total,
                },
                details="; ".join(failures) if failures else f"all {total} tests passed",
            )
        ]

    def _reading(
        self,
        trial: Trial,
        *,
        passed: bool,
        score: float,
        details: str = "",
        metrics: dict | None = None,
    ) -> Reading:
        return Reading(
            sensor_name=self.name,
            probe_id=trial.probe_id,
            trial_index=trial.trial_index,
            passed=passed,
            score=score,
            metrics=metrics or {},
            details=details,
        )

    def _extract_code(self, response: Any) -> str | None:
        """Extract code from response — handles str or AgentResponse."""
        if isinstance(response, str):
            return response
        if hasattr(response, "content"):
            return response.content
        return None

    def _load_function(self, code: str, function_name: str):
        """Load code into isolated module, extract named function."""
        tmp = Path(tempfile.mktemp(suffix=".py"))
        tmp.write_text(code)
        try:
            spec = importlib.util.spec_from_file_location("solution", tmp)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        finally:
            tmp.unlink()
        return getattr(module, function_name)
