"""Core protocols — ExperimentRuntime, Sensor.

Composable building blocks of any experiment.
Each is a typing.Protocol: implement the methods, satisfy the contract.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

from ix.domain.types import Reading, Trial


@runtime_checkable
class ExperimentRuntime(Protocol):
    """Executes a prompt and returns a response.

    Eval domain: Agent wraps Claude SDK (run → AgentResponse).
    Benchmark domain: wraps HTTP client, matcher engine, etc.

    The runtime already knows its identity (system prompt, config).
    Callers just provide the task prompt.
    """

    async def run(self, prompt: str) -> Any: ...


@runtime_checkable
class Sensor(Protocol):
    """Measures a trial and produces readings.

    The sensor is an instrument — it observes a trial (probe_id + response).
    Ground truth (test cases, rubrics) is injected at construction by
    the service layer, not discovered from the probe.

    The trial gives the sensor a key (probe_id) to look up its
    pre-configured ground truth, and a response to measure.
    """

    @property
    def name(self) -> str: ...

    def sense(self, trial: Trial) -> list[Reading]: ...
