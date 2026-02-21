"""Tests for ClaudeAgent — Agent SDK adapter."""

import sys
import types

import pytest
from matrix.domain.types import AgentResponse

# --- SDK integration tests (mocked) ---


class _FakeTextBlock:
    def __init__(self, text: str):
        self.text = text


class _FakeToolUseBlock:
    def __init__(self, name: str, input: dict):
        self.name = name
        self.input = input


class _FakeAssistantMessage:
    def __init__(self, content: list):
        self.content = content


class _FakeResultMessage:
    def __init__(
        self,
        duration_ms: int = 100,
        total_cost_usd: float = 0.01,
        usage: dict | None = None,
        num_turns: int = 1,
    ):
        self.duration_ms = duration_ms
        self.total_cost_usd = total_cost_usd
        self.usage = usage or {"input_tokens": 50, "output_tokens": 30}
        self.num_turns = num_turns


@pytest.fixture
def fake_sdk(monkeypatch):
    """Install a fake claude_agent_sdk module into sys.modules."""
    captured: dict = {"calls": []}

    async def fake_query(prompt, options=None):
        captured["calls"].append({"prompt": prompt, "options": options})
        yield _FakeAssistantMessage([_FakeTextBlock(f"echo: {prompt}")])
        yield _FakeResultMessage()

    sdk = types.ModuleType("claude_agent_sdk")
    sdk.query = fake_query  # type: ignore[attr-defined]
    sdk.ClaudeAgentOptions = lambda **kw: kw  # type: ignore[attr-defined]
    sdk.AssistantMessage = _FakeAssistantMessage  # type: ignore[attr-defined]
    sdk.TextBlock = _FakeTextBlock  # type: ignore[attr-defined]
    sdk.ToolUseBlock = _FakeToolUseBlock  # type: ignore[attr-defined]
    sdk.ResultMessage = _FakeResultMessage  # type: ignore[attr-defined]

    monkeypatch.setitem(sys.modules, "claude_agent_sdk", sdk)
    return captured


@pytest.fixture
def fake_sdk_with_tools(monkeypatch):
    """SDK mock that returns tool use blocks."""
    captured: dict = {"calls": []}

    async def fake_query(prompt, options=None):
        captured["calls"].append({"prompt": prompt, "options": options})
        yield _FakeAssistantMessage(
            [
                _FakeTextBlock("Let me help with that."),
                _FakeToolUseBlock("Skill", {"skill": "build-eval"}),
            ]
        )
        yield _FakeResultMessage(
            duration_ms=250,
            total_cost_usd=0.05,
            usage={"input_tokens": 100, "output_tokens": 80},
            num_turns=2,
        )

    sdk = types.ModuleType("claude_agent_sdk")
    sdk.query = fake_query  # type: ignore[attr-defined]
    sdk.ClaudeAgentOptions = lambda **kw: kw  # type: ignore[attr-defined]
    sdk.AssistantMessage = _FakeAssistantMessage  # type: ignore[attr-defined]
    sdk.TextBlock = _FakeTextBlock  # type: ignore[attr-defined]
    sdk.ToolUseBlock = _FakeToolUseBlock  # type: ignore[attr-defined]
    sdk.ResultMessage = _FakeResultMessage  # type: ignore[attr-defined]

    monkeypatch.setitem(sys.modules, "claude_agent_sdk", sdk)
    return captured


class TestClaudeAgent:
    @pytest.mark.anyio
    async def test_run_returns_agent_response(self, fake_sdk):
        from matrix.adapters._out.runtime.claude import ClaudeAgent

        agent = ClaudeAgent(system_prompt="You are helpful.", max_turns=1)
        response = await agent.run("hello")

        assert isinstance(response, AgentResponse)
        assert response.content == "echo: hello"
        assert response.tool_calls == ()
        assert response.tokens_input == 50
        assert response.tokens_output == 30
        assert response.duration_ms == 100
        assert response.cost_usd == 0.01
        assert response.num_turns == 1

    @pytest.mark.anyio
    async def test_run_captures_tool_calls(self, fake_sdk_with_tools):
        from matrix.adapters._out.runtime.claude import ClaudeAgent

        agent = ClaudeAgent(system_prompt="test")
        response = await agent.run("write evals")

        assert response.content == "Let me help with that."
        assert len(response.tool_calls) == 1
        assert response.tool_calls[0] == {
            "name": "Skill",
            "input": {"skill": "build-eval"},
        }
        assert response.duration_ms == 250
        assert response.cost_usd == 0.05
        assert response.tokens_input == 100
        assert response.tokens_output == 80
        assert response.num_turns == 2

    @pytest.mark.anyio
    async def test_options_passed_correctly(self, fake_sdk):
        from matrix.adapters._out.runtime.claude import ClaudeAgent

        agent = ClaudeAgent(
            system_prompt="Be concise.",
            max_turns=3,
            allowed_tools=["Read"],
            plugins=[{"name": "test"}],
        )
        await agent.run("hi")

        assert len(fake_sdk["calls"]) == 1
        opts = fake_sdk["calls"][0]["options"]
        assert opts["system_prompt"] == "Be concise."
        assert opts["max_turns"] == 3
        assert opts["allowed_tools"] == ["Read"]
        assert opts["plugins"] == [{"name": "test"}]

    @pytest.mark.anyio
    async def test_empty_prompt(self, fake_sdk):
        from matrix.adapters._out.runtime.claude import ClaudeAgent

        agent = ClaudeAgent()
        response = await agent.run("")

        assert response.content == "echo: "

    def test_default_max_turns(self, fake_sdk):
        from matrix.adapters._out.runtime.claude import ClaudeAgent

        agent = ClaudeAgent()
        assert agent._max_turns == 1

    def test_custom_max_turns(self, fake_sdk):
        from matrix.adapters._out.runtime.claude import ClaudeAgent

        agent = ClaudeAgent(max_turns=5)
        assert agent._max_turns == 5

    def test_no_system_prompt(self, fake_sdk):
        from matrix.adapters._out.runtime.claude import ClaudeAgent

        agent = ClaudeAgent()
        assert agent._system_prompt is None
