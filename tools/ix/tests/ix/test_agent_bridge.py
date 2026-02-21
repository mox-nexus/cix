"""Tests for MockAgent — implements Agent protocol (run → AgentResponse)."""

from ix.adapters._out.mock_runtime import MockAgent
from matrix import AgentResponse


class TestMockAgent:
    async def test_run_returns_agent_response(self):
        """MockAgent returns structured AgentResponse objects."""
        agent = MockAgent(expected_skill="build-eval", seed=42)
        result = await agent.run("How do I write evals?")
        assert isinstance(result, AgentResponse)

    async def test_always_activates_without_expectations(self):
        """Without expectations, always produces a Skill tool call."""
        agent = MockAgent(expected_skill="build-eval")
        result = await agent.run("test")
        assert "build-eval" in result.content
        assert len(result.tool_calls) == 1
        assert result.tool_calls[0]["name"] == "Skill"
        assert result.tool_calls[0]["input"]["skill"] == "build-eval"

    async def test_stochastic_with_expectations(self):
        """With expectations and seed, produces deterministic activation rates."""
        expectations = {
            "must prompt": True,
            "not prompt": False,
        }
        agent = MockAgent(expected_skill="build-eval", seed=42, expectations=expectations)

        # Run multiple trials
        must_activations = 0
        not_activations = 0
        for _ in range(100):
            result = await agent.run("must prompt")
            if len(result.tool_calls) > 0:
                must_activations += 1
            result = await agent.run("not prompt")
            if len(result.tool_calls) > 0:
                not_activations += 1

        # 90/10 split: must_trigger ~90%, should_not ~10%
        assert must_activations > 70
        assert not_activations < 30
