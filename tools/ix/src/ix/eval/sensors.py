"""Eval sensors — measure trial responses for evaluation experiments.

Each sensor implements Sensor protocol: sense(trial) -> list[Reading].
Each sensor has a typed Config model (Pydantic) for validated construction.
Ground truth is injected at construction by the service layer.
"""

from __future__ import annotations

import importlib.util
import re
import signal
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

    def measure(self, trial: Trial) -> list[Reading]:
        return [r for s in self._sensors for r in s.measure(trial)]


# --- Config Models ---


class ActivationSensorConfig(BaseModel, frozen=True, extra="forbid"):
    """Config for ActivationSensor. Validated from experiment.yaml sensor section.

    expected_skill is the experiment-level default. Per-probe expected_skill
    in probe metadata overrides it (same pattern as ToolUsageSensor).
    """

    type: str = "activation"
    expected_skill: str | None = None


class FunctionTestSensorConfig(BaseModel, frozen=True, extra="forbid"):
    """Config for FunctionTestSensor. Validated from experiment.yaml sensor section."""

    type: str = "function-test"
    timeout: int = 30


class ToolUsageSensorConfig(BaseModel, frozen=True, extra="forbid"):
    """Config for ToolUsageSensor. Validated from experiment.yaml sensor section."""

    type: str = "tool-usage"
    expected_tool: str = "memex"


class OutcomeSensorConfig(BaseModel, frozen=True, extra="forbid"):
    """Config for OutcomeSensor. Validated from experiment.yaml sensor section."""

    type: str = "outcome"
    graders_module: str | None = None  # Path to Python module with grader functions


# --- Sensors ---


class ActivationSensor:
    """Deterministic grader — did the agent activate the right skill?

    Expectation-aware: accounts for must_trigger vs should_not_trigger.
    A should_not_trigger probe that correctly doesn't activate → passed=True.
    """

    Config = ActivationSensorConfig

    def __init__(
        self,
        expected_skill: str | None = None,
        expectations: dict[str, str] | None = None,
        expected_skills: dict[str, str] | None = None,
    ):
        self._expected_skill = expected_skill
        self._expectations = expectations or {}
        self._expected_skills = expected_skills or {}

    @classmethod
    def from_config(
        cls,
        config: ActivationSensorConfig,
        probes: tuple[Probe, ...] = (),
        **kwargs: Any,
    ) -> ActivationSensor:
        expectations = {p.id: p.metadata.get("expectation", "must_trigger") for p in probes}
        expected_skills = {
            p.id: p.metadata.get("expected_skill", config.expected_skill)
            for p in probes
            if p.metadata.get("expected_skill") or config.expected_skill
        }
        return cls(
            expected_skill=config.expected_skill,
            expectations=expectations,
            expected_skills=expected_skills,
        )

    @property
    def name(self) -> str:
        return "activation"

    def measure(self, trial: Trial) -> list[Reading]:
        """Grade: did the agent's activation match the expectation?"""
        response: AgentResponse = trial.response

        # Resolve which skill this probe expects
        expected = self._expected_skills.get(trial.probe_id, self._expected_skill)

        # Check if any Skill tool call matches
        activated_skill = None
        for tc in response.tool_calls:
            if tc.get("name") != "Skill":
                continue
            skill_value = tc.get("input", {}).get("skill", "")
            if expected and expected in skill_value:
                activated_skill = skill_value
                break
            if not activated_skill:
                activated_skill = skill_value

        activated = activated_skill is not None and (
            expected is None or expected in activated_skill
        )

        expectation = self._expectations.get(trial.probe_id, "must_trigger")

        if expectation == "must_trigger":
            passed = activated
        elif expectation == "should_not_trigger":
            passed = not (activated_skill is not None)
        else:  # acceptable
            passed = True

        return [
            Reading(
                sensor_name=self.name,
                probe_id=trial.probe_id,
                trial_index=trial.trial_index,
                passed=passed,
                score=1.0 if passed else 0.0,
                metrics={
                    "expected_skill": expected,
                    "activated_skill": activated_skill,
                },
                details=(
                    f"expected={expected}, activated={activated_skill}, "
                    f"expectation={expectation}"
                ),
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

    def measure(self, trial: Trial) -> list[Reading]:
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
        except TimeoutError as e:
            return [self._reading(trial, passed=False, score=0.0, details=f"timeout: {e}")]
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
        """Extract Python code from response.

        Handles str or AgentResponse. If the content contains markdown
        code blocks (```python ... ```), extracts the last one (usually
        the final version). Otherwise returns the raw content.
        """
        text = None
        if isinstance(response, str):
            text = response
        elif hasattr(response, "content"):
            text = response.content

        if text is None:
            return None

        # Try ```python blocks first (last block = final version)
        blocks = re.findall(r"```python\s*\n(.*?)```", text, re.DOTALL)
        if blocks:
            return blocks[-1].strip()

        # Try any ``` blocks
        blocks = re.findall(r"```\s*\n(.*?)```", text, re.DOTALL)
        if blocks:
            return blocks[-1].strip()

        # No code blocks — return raw (might be pure code)
        return text

    def _load_function(self, code: str, function_name: str):
        """Load code into isolated module, extract named function.

        Enforces self._timeout on exec_module to prevent infinite loops
        in generated code. Uses SIGALRM on Unix; noop on Windows.
        """
        tmp = Path(tempfile.mktemp(suffix=".py"))
        tmp.write_text(code)
        try:
            spec = importlib.util.spec_from_file_location("solution", tmp)
            module = importlib.util.module_from_spec(spec)
            self._exec_with_timeout(spec.loader.exec_module, module)
        finally:
            tmp.unlink()
        return getattr(module, function_name)

    def _exec_with_timeout(self, fn, *args):
        """Execute fn with SIGALRM timeout. Noop on platforms without SIGALRM."""
        if not hasattr(signal, "SIGALRM"):
            return fn(*args)

        def handler(signum, frame):
            raise TimeoutError(f"execution exceeded {self._timeout}s timeout")

        prev = signal.signal(signal.SIGALRM, handler)
        signal.alarm(self._timeout)
        try:
            return fn(*args)
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, prev)


class ToolUsageSensor:
    """Checks if the agent used the right tool with the right subcommand.

    Probe metadata carries expected usage:
      expected_command: "dig"       — which subcommand
      expected_args: "auth"         — substring in query (optional)

    Scores: 1.0 = right tool + right command + right args,
            0.5 = right tool + right command, wrong/missing args,
            0.0 = wrong tool or no tool call.
    """

    Config = ToolUsageSensorConfig

    def __init__(
        self,
        expected_tool: str = "memex",
        expectations: dict[str, dict] | None = None,
    ):
        self._expected_tool = expected_tool
        self._expectations = expectations or {}

    @classmethod
    def from_config(
        cls,
        config: ToolUsageSensorConfig,
        probes: tuple[Probe, ...] = (),
        **kwargs: Any,
    ) -> ToolUsageSensor:
        expectations = {
            p.id: {
                "command": p.metadata.get("expected_command", ""),
                "args": p.metadata.get("expected_query", p.metadata.get("expected_args", "")),
                "expectation": p.metadata.get("expectation", "must_trigger"),
            }
            for p in probes
        }
        return cls(expected_tool=config.expected_tool, expectations=expectations)

    @property
    def name(self) -> str:
        return "tool-usage"

    def measure(self, trial: Trial) -> list[Reading]:
        response: AgentResponse = trial.response
        expect = self._expectations.get(trial.probe_id, {})
        expected_cmd = expect.get("command", "")
        expected_args = expect.get("args", "")
        expectation = expect.get("expectation", "must_trigger")

        # Find tool calls matching expected tool — direct or via Bash
        matching = self._find_tool_calls(response.tool_calls)

        if not matching:
            # No tool call — correct for should_not_trigger
            if expectation == "should_not_trigger":
                return [
                    self._reading(
                        trial,
                        passed=True,
                        score=1.0,
                        details=f"correctly did not use {self._expected_tool}",
                    )
                ]
            return [
                self._reading(
                    trial, passed=False, score=0.0, details=f"no {self._expected_tool} tool call"
                )
            ]

        # Tool was called — wrong for should_not_trigger
        if expectation == "should_not_trigger":
            return [
                self._reading(
                    trial,
                    passed=False,
                    score=0.0,
                    details=f"incorrectly used {self._expected_tool}",
                )
            ]

        tc = matching[0]
        tc_input = tc.get("input", {})
        actual_cmd = str(tc_input.get("command", "")).replace("\n", " ").strip()
        actual_query = str(tc_input.get("query", "")).replace("\n", " ").strip()

        # Check command correctness
        cmd_correct = expected_cmd and expected_cmd.lower() in actual_cmd.lower()
        args_correct = (
            not expected_args
            or expected_args.lower() in actual_query.lower()
            or expected_args.lower() in str(tc_input).lower()
        )

        if cmd_correct and args_correct:
            score = 1.0
            passed = True
            detail = f"correct: {actual_cmd}({actual_query})"
        elif cmd_correct:
            score = 0.5
            passed = True
            detail = f"right command ({actual_cmd}) but args missing/wrong: {actual_query}"
        else:
            score = 0.0
            passed = False
            detail = f"wrong command: got {actual_cmd}, expected {expected_cmd}"

        return [self._reading(trial, passed=passed, score=score, details=detail)]

    def _find_tool_calls(self, tool_calls: tuple[dict, ...]) -> list[dict]:
        """Find tool calls matching expected_tool — direct or via Bash.

        ClaudeAgent records Bash tool calls like:
          {"name": "Bash", "input": {"command": "memex dig 'auth tokens'"}}
        We parse these into normalized form matching the direct tool schema.
        """
        # Direct matches (AnthropicAgent style)
        direct = [tc for tc in tool_calls if tc.get("name") == self._expected_tool]
        if direct:
            return direct

        # Bash matches (ClaudeAgent style)
        bash_matches = []
        for tc in tool_calls:
            if tc.get("name") != "Bash":
                continue
            cmd = str(tc.get("input", {}).get("command", ""))
            if self._expected_tool not in cmd:
                continue
            # Parse "memex dig 'query'" → {"command": "dig", "query": "query"}
            parsed = self._parse_bash_command(cmd)
            if parsed:
                bash_matches.append({"name": self._expected_tool, "input": parsed})
        return bash_matches

    def _parse_bash_command(self, bash_cmd: str) -> dict | None:
        """Parse a bash command like 'memex dig "query"' into structured form.

        Handles compound commands: 'cd /path && memex dig "query"'
        Handles pipes: 'memex dig "query" | head'
        """
        # Split on && and ; to find the memex segment
        import shlex

        for segment in re.split(r"&&|;", bash_cmd):
            segment = segment.strip()
            if self._expected_tool not in segment:
                continue

            # Strip pipes — take only the memex part
            segment = segment.split("|")[0].strip()

            try:
                parts = shlex.split(segment)
            except ValueError:
                parts = segment.split()

            try:
                tool_idx = next(i for i, p in enumerate(parts) if p == self._expected_tool)
            except StopIteration:
                continue

            remaining = parts[tool_idx + 1 :]
            if not remaining:
                return {"command": "", "query": ""}

            # First non-flag arg is the subcommand
            subcommand = ""
            query_parts = []
            for part in remaining:
                if part.startswith("-"):
                    continue
                if not subcommand:
                    subcommand = part
                else:
                    query_parts.append(part)

            return {
                "command": subcommand,
                "query": " ".join(query_parts),
            }

        return None

    def _reading(self, trial: Trial, *, passed: bool, score: float, details: str) -> Reading:
        return Reading(
            sensor_name=self.name,
            probe_id=trial.probe_id,
            trial_index=trial.trial_index,
            passed=passed,
            score=score,
            details=details,
        )


class OutcomeSensor:
    """Grades intent→outcome: did the agent's answer contain the expected facts?

    Two grading modes:
      1. Functional graders (preferred): Python functions per probe that validate
         against corpus ground truth. Loaded from graders_module in config.
      2. String containment (fallback): checks expected_facts from probe metadata.

    Scores:
      - answer_score: from grader function or fraction of expected_facts found
      - efficiency metrics: num_turns, num_tool_calls, tokens (from AgentResponse)
    """

    Config = OutcomeSensorConfig

    def __init__(
        self,
        ground_truth: dict[str, dict] | None = None,
        graders: dict[str, Any] | None = None,
    ):
        self._ground_truth = ground_truth or {}
        self._graders = graders or {}

    @classmethod
    def from_config(
        cls,
        config: OutcomeSensorConfig,
        probes: tuple[Probe, ...] = (),
        **kwargs: Any,
    ) -> OutcomeSensor:
        ground_truth = {
            p.id: {
                "expected_facts": p.metadata.get("expected_facts", []),
                "expected_command": p.metadata.get("expected_command", ""),
            }
            for p in probes
        }
        graders = {}
        if config.graders_module:
            graders = cls._load_graders(config.graders_module)
        return cls(ground_truth=ground_truth, graders=graders)

    @staticmethod
    def _load_graders(module_path: str) -> dict[str, Any]:
        """Load grader functions from a Python module file."""
        spec = importlib.util.spec_from_file_location("graders", module_path)
        if spec is None or spec.loader is None:
            return {}
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        registry = getattr(mod, "GRADERS", {})
        return dict(registry)

    @property
    def name(self) -> str:
        return "outcome"

    def measure(self, trial: Trial) -> list[Reading]:
        response: AgentResponse = trial.response

        # Efficiency metrics from AgentResponse
        num_tool_calls = len(response.tool_calls)
        metrics = {
            "num_turns": response.num_turns,
            "num_tool_calls": num_tool_calls,
            "tokens_input": response.tokens_input,
            "tokens_output": response.tokens_output,
            "duration_ms": response.duration_ms,
        }
        if response.cost_usd is not None:
            metrics["cost_usd"] = response.cost_usd

        # Path quality: did it use the right command?
        truth = self._ground_truth.get(trial.probe_id, {})
        expected_cmd = truth.get("expected_command", "")
        if expected_cmd and response.tool_calls:
            cmd_used = any(
                expected_cmd.lower() in str(tc.get("input", {}).get("command", "")).lower()
                for tc in response.tool_calls
            )
            metrics["correct_command"] = cmd_used

        # Grade: functional grader (preferred) or string containment (fallback)
        grader = self._graders.get(trial.probe_id)
        if grader is not None:
            answer_score = grader(response.content)
            details = (
                f"grader={trial.probe_id}, score={answer_score:.0%}, "
                f"turns={response.num_turns}, tools={num_tool_calls}"
            )
        else:
            expected_facts = truth.get("expected_facts", [])
            if not expected_facts:
                msg = f"no grader or expected_facts for probe '{trial.probe_id}'"
                return [
                    self._reading(
                        trial,
                        passed=False,
                        score=0.0,
                        details=msg,
                    )
                ]
            content_lower = response.content.lower()
            found = [f for f in expected_facts if f.lower() in content_lower]
            missed = [f for f in expected_facts if f.lower() not in content_lower]
            answer_score = len(found) / len(expected_facts)
            details_parts = []
            if found:
                details_parts.append(f"found: {found}")
            if missed:
                details_parts.append(f"missed: {missed}")
            details_parts.append(f"turns={response.num_turns}, tools={num_tool_calls}")
            details = "; ".join(details_parts)

        metrics["answer_score"] = answer_score

        return [
            self._reading(
                trial,
                passed=answer_score > 0.5,
                score=answer_score,
                metrics=metrics,
                details=details,
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
