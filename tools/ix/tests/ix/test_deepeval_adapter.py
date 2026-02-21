"""Tests for DeepEval agent adapter — bridges Matrix Agent to DeepEval's model interface.

Tests the adapter in isolation using MockAgent. Does NOT require DeepEval's
metrics to run — just verifies the adapter correctly translates between protocols.
"""

import os

import pytest
from ix.adapters._out.mock_runtime import MockAgent
from ix.eval.sensors_deepeval import DeepEvalSensor, DeepEvalSensorConfig, _create_agent_adapter


class TestAgentModelAdapter:
    """Test the adapter bridges Agent to DeepEvalBaseLLM correctly."""

    def test_generate_returns_content(self):
        """Sync generate() routes through Agent.run() and returns content."""
        agent = MockAgent(expected_skill="build-eval")
        adapter = _create_agent_adapter(agent, model_name="mock-agent")

        result = adapter.generate("test prompt")

        assert isinstance(result, str)
        assert len(result) > 0

    async def test_a_generate_returns_content(self):
        """Async a_generate() directly awaits Agent.run()."""
        agent = MockAgent(expected_skill="build-eval")
        adapter = _create_agent_adapter(agent, model_name="mock-agent")

        result = await adapter.a_generate("test prompt")

        assert isinstance(result, str)
        assert len(result) > 0

    def test_model_name(self):
        agent = MockAgent(expected_skill="build-eval")
        adapter = _create_agent_adapter(agent, model_name="claude-haiku")

        assert adapter.get_model_name() == "claude-haiku"

    def test_is_deepeval_base_llm(self):
        """Adapter satisfies DeepEval's type check."""
        from deepeval.models import DeepEvalBaseLLM

        agent = MockAgent(expected_skill="build-eval")
        adapter = _create_agent_adapter(agent)

        assert isinstance(adapter, DeepEvalBaseLLM)

    def test_generate_ignores_extra_kwargs(self):
        """DeepEval may pass schema=... which we ignore."""
        agent = MockAgent(expected_skill="build-eval")
        adapter = _create_agent_adapter(agent)

        result = adapter.generate("test", schema=None)
        assert isinstance(result, str)


class TestDeepEvalSensorWithJudge:
    """Test DeepEvalSensor accepts a judge agent."""

    def test_from_config_with_judge(self):
        """from_config passes judge through to constructor."""
        config = DeepEvalSensorConfig(metric="answer_relevancy", threshold=0.5)
        judge = MockAgent(expected_skill="judge")

        sensor = DeepEvalSensor.from_config(config, probes=(), judge=judge)

        assert sensor.name == "deepeval.answer_relevancy"

    @pytest.mark.skipif(
        not os.environ.get("OPENAI_API_KEY"),
        reason="DeepEval default model requires OPENAI_API_KEY",
    )
    def test_from_config_without_judge(self):
        """from_config works without judge (DeepEval default model)."""
        config = DeepEvalSensorConfig(metric="answer_relevancy", threshold=0.5)

        sensor = DeepEvalSensor.from_config(config, probes=())

        assert sensor.name == "deepeval.answer_relevancy"


class TestCompositeSensorWithDeepEval:
    """Test CompositeSensor works with DeepEval sensors."""

    def test_composite_includes_deepeval(self):
        """CompositeSensor can wrap a DeepEvalSensor alongside others."""
        from ix.eval.sensors import ActivationSensor, CompositeSensor

        activation = ActivationSensor(expected_skill="build-eval")
        judge = MockAgent(expected_skill="judge")
        deepeval_sensor = DeepEvalSensor(
            metric_name="answer_relevancy",
            threshold=0.5,
            judge=judge,
        )

        composite = CompositeSensor([activation, deepeval_sensor])

        assert "activation" in composite.name
        assert "deepeval.answer_relevancy" in composite.name
