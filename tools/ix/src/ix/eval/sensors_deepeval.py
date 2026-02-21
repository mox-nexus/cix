"""DeepEval sensor — wraps DeepEval metrics as ix Sensors.

Lazy-imports deepeval to avoid heavy dependency unless explicitly used.
Install with: uv add ix[deepeval]

When a judge agent is provided, LLM calls go through Matrix's Agent protocol
via the AgentModelAdapter — making grading observable (tokens, cost, duration).
"""

from __future__ import annotations

import asyncio
import concurrent.futures
from typing import Any

from matrix import AgentResponse
from pydantic import BaseModel

from ix.domain.types import Probe, Reading, Trial

# --- Config ---


class DeepEvalSensorConfig(BaseModel, frozen=True, extra="forbid"):
    """Config for DeepEvalSensor. Validated from experiment.yaml sensor section."""

    type: str = "deepeval"
    metric: str = "answer_relevancy"
    threshold: float = 0.5
    model: str | None = None
    criteria: str | None = None  # For GEval custom criteria


# --- Agent Adapter ---


def _create_agent_adapter(agent: Any, model_name: str = "ix-agent") -> Any:
    """Create a DeepEval model adapter wrapping a Matrix Agent.

    Bridges Matrix's Agent protocol (async run(prompt) → AgentResponse)
    to DeepEval's DeepEvalBaseLLM interface (sync generate(prompt) → str).

    Class defined inside function to keep deepeval as a lazy import.
    """
    from deepeval.models import DeepEvalBaseLLM

    class AgentModelAdapter(DeepEvalBaseLLM):
        """Routes DeepEval LLM calls through a Matrix Agent.

        DeepEval constructs evaluation prompts internally.
        This adapter just provides the LLM execution layer.
        """

        def __init__(self) -> None:
            self._agent = agent
            self._model_name = model_name
            # DeepEvalBaseLLM.__init__ calls load_model and sets self.name
            # We skip it and set attributes directly to avoid side effects
            self.name = model_name
            self.model = None

        def load_model(self) -> None:
            return None

        def generate(self, prompt: str, **kwargs: Any) -> str:
            """Sync bridge: runs Agent.run() in a thread with its own event loop."""
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                response = pool.submit(asyncio.run, self._agent.run(prompt)).result()
            return response.content

        async def a_generate(self, prompt: str, **kwargs: Any) -> str:
            """Async path: directly awaits Agent.run()."""
            response = await self._agent.run(prompt)
            return response.content

        def get_model_name(self) -> str:
            return self._model_name

    return AgentModelAdapter()


# --- Metric Builder ---


_METRIC_BUILDERS: dict[str, str] = {
    "answer_relevancy": "deepeval.metrics:AnswerRelevancyMetric",
    "faithfulness": "deepeval.metrics:FaithfulnessMetric",
    "contextual_precision": "deepeval.metrics:ContextualPrecisionMetric",
    "contextual_recall": "deepeval.metrics:ContextualRecallMetric",
    "contextual_relevancy": "deepeval.metrics:ContextualRelevancyMetric",
    "hallucination": "deepeval.metrics:HallucinationMetric",
    "bias": "deepeval.metrics:BiasMetric",
    "toxicity": "deepeval.metrics:ToxicityMetric",
    "g_eval": "deepeval.metrics:GEval",
}


def _build_metric(
    metric_name: str,
    threshold: float,
    model: Any | None,
    criteria: str | None,
) -> Any:
    """Build a DeepEval metric instance by name.

    model can be a string (DeepEval's default provider) or an
    AgentModelAdapter (Matrix Agent-backed). Both are valid for the
    metric's model parameter.
    """
    dotpath = _METRIC_BUILDERS.get(metric_name)
    if dotpath is None:
        valid = sorted(_METRIC_BUILDERS)
        raise ValueError(
            f"Unknown DeepEval metric: {metric_name!r}. Valid metrics: {', '.join(valid)}"
        )

    module_path, class_name = dotpath.rsplit(":", 1)

    try:
        import importlib

        mod = importlib.import_module(module_path)
        metric_cls = getattr(mod, class_name)
    except ImportError as e:
        raise ImportError(
            "DeepEvalSensor requires 'deepeval'. Install with: uv add ix[deepeval]"
        ) from e

    kwargs: dict[str, Any] = {"threshold": threshold}
    if model is not None:
        kwargs["model"] = model
    if criteria is not None and metric_name == "g_eval":
        kwargs["criteria"] = criteria

    return metric_cls(**kwargs)


# --- Sensor ---


class DeepEvalSensor:
    """Wraps a DeepEval metric as an ix Sensor.

    Translates between ix's sense(trial) → list[Reading] protocol
    and DeepEval's BaseMetric.measure(LLMTestCase) API.

    When a judge agent is provided, LLM calls route through the
    AgentModelAdapter — observable via AgentResponse.
    When no judge is provided, DeepEval uses its default model.
    """

    Config = DeepEvalSensorConfig

    def __init__(
        self,
        *,
        metric_name: str = "answer_relevancy",
        threshold: float = 0.5,
        model: Any | None = None,
        criteria: str | None = None,
        judge: Any | None = None,
        ground_truth: dict[str, dict] | None = None,
    ):
        # Judge agent takes precedence over model string
        if judge is not None:
            model_or_adapter = _create_agent_adapter(
                judge,
                model_name=getattr(judge, "model_name", "ix-agent"),
            )
        else:
            model_or_adapter = model

        self._metric = _build_metric(metric_name, threshold, model_or_adapter, criteria)
        self._metric_name = metric_name
        self._threshold = threshold
        self._ground_truth = ground_truth or {}

    @classmethod
    def from_config(
        cls,
        config: DeepEvalSensorConfig,
        probes: tuple[Probe, ...] = (),
        judge: Any | None = None,
    ) -> DeepEvalSensor:
        ground_truth = {
            p.id: {
                "prompt": p.prompt,
                "expected_output": p.metadata.get("expected_output"),
                "context": p.metadata.get("context"),
            }
            for p in probes
        }
        return cls(
            metric_name=config.metric,
            threshold=config.threshold,
            model=config.model,
            criteria=config.criteria,
            judge=judge,
            ground_truth=ground_truth,
        )

    @property
    def name(self) -> str:
        return f"deepeval.{self._metric_name}"

    def sense(self, trial: Trial) -> list[Reading]:
        """Measure a trial via the DeepEval metric."""
        from deepeval.test_case import LLMTestCase

        response: AgentResponse = trial.response
        truth = self._ground_truth.get(trial.probe_id, {})

        kwargs: dict[str, Any] = {
            "input": truth.get("prompt", ""),
            "actual_output": response.content,
        }
        if truth.get("expected_output") is not None:
            kwargs["expected_output"] = truth["expected_output"]
        if truth.get("context") is not None:
            kwargs["context"] = truth["context"]

        test_case = LLMTestCase(**kwargs)
        self._metric.measure(test_case)

        score = float(self._metric.score) if self._metric.score is not None else 0.0
        reason = getattr(self._metric, "reason", "") or ""

        return [
            Reading(
                sensor_name=self.name,
                probe_id=trial.probe_id,
                trial_index=trial.trial_index,
                passed=score >= self._threshold,
                score=score,
                details=reason,
            )
        ]
