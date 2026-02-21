"""Shared test fixtures for ix tests."""

from matrix import AgentResponse


def mock_response(*, activated: bool, skill: str = "build-eval") -> AgentResponse:
    """Create an AgentResponse for testing."""
    if activated:
        return AgentResponse(
            content="mock",
            tool_calls=({"name": "Skill", "input": {"skill": skill}},),
        )
    return AgentResponse(content="mock")
