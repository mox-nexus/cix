"""Tests for MockAgent — ix-specific test double implementing Agent protocol.

Verifies deterministic and stochastic behavior, protocol conformance,
and response structure. Source: ix/adapters/_out/mock_runtime.py.
"""

from ix.adapters._out.mock_runtime import MockAgent
from matrix import AgentResponse


class TestProtocol:
    async def test_satisfies_agent_protocol(self):
        """MockAgent.run(prompt) -> AgentResponse — structurally satisfies Agent."""
        agent = MockAgent()
        result = await agent.run("test")
        assert isinstance(result, AgentResponse)


class TestDeterministicMode:
    """Without expectations, MockAgent always activates the expected skill."""

    async def test_always_activates(self):
        agent = MockAgent(expected_skill="build-eval")
        result = await agent.run("anything")

        assert len(result.tool_calls) == 1
        assert result.tool_calls[0]["name"] == "Skill"
        assert result.tool_calls[0]["input"]["skill"] == "build-eval"

    async def test_content_mentions_skill(self):
        agent = MockAgent(expected_skill="build-eval")
        result = await agent.run("How do evals work?")
        assert "build-eval" in result.content


class TestStochasticMode:
    """With expectations and seed, produces deterministic activation rates."""

    async def test_same_seed_same_output(self):
        agent1 = MockAgent(expected_skill="build-eval", seed=42, expectations={"q": True})
        agent2 = MockAgent(expected_skill="build-eval", seed=42, expectations={"q": True})

        r1 = await agent1.run("q")
        r2 = await agent2.run("q")
        assert r1 == r2

    async def test_no_tool_calls_when_not_activated(self):
        """seed=7 with should_not_trigger (10% rate) should NOT activate."""
        agent = MockAgent(
            expected_skill="build-eval",
            seed=7,
            expectations={"hello": False},
        )
        response = await agent.run("hello")
        assert len(response.tool_calls) == 0

    async def test_activation_rates_match_expectations(self):
        """must_trigger ~90%, should_not ~10% over many trials."""
        expectations = {"must prompt": True, "not prompt": False}

        agent = MockAgent(expected_skill="build-eval", seed=42, expectations=expectations)
        must_activations = 0
        not_activations = 0
        for _ in range(100):
            result = await agent.run("must prompt")
            if len(result.tool_calls) > 0:
                must_activations += 1
            result = await agent.run("not prompt")
            if len(result.tool_calls) > 0:
                not_activations += 1

        assert must_activations > 70, f"Expected >70 must_trigger activations, got {must_activations}"
        assert not_activations < 30, f"Expected <30 should_not activations, got {not_activations}"
