"""Test fixtures for memex."""

from datetime import datetime

import pytest
from memex.domain.models import Fragment, Provenance


@pytest.fixture
def sample_fragments() -> list[Fragment]:
    """Create sample fragments for testing."""
    return [
        Fragment(
            id="frag-1",
            conversation_id="conv-1",
            role="assistant",
            content="OAuth 2.0 is the recommended authentication protocol for APIs.",
            provenance=Provenance(
                source_kind="claude_conversations",
                source_id="msg-1",
                timestamp=datetime(2025, 1, 1, 12, 0),
            ),
        ),
        Fragment(
            id="frag-2",
            conversation_id="conv-1",
            role="user",
            content="What about JWT tokens for session management?",
            provenance=Provenance(
                source_kind="claude_conversations",
                source_id="msg-2",
                timestamp=datetime(2025, 1, 1, 12, 1),
            ),
        ),
        Fragment(
            id="frag-3",
            conversation_id="conv-2",
            role="assistant",
            content="Rate limiting protects your API from abuse.",
            provenance=Provenance(
                source_kind="openai",
                source_id="msg-3",
                timestamp=datetime(2025, 1, 2, 10, 0),
            ),
        ),
        Fragment(
            id="frag-4",
            conversation_id="conv-2",
            role="assistant",
            content="Consider implementing exponential backoff for retries.",
            provenance=Provenance(
                source_kind="openai",
                source_id="msg-4",
                timestamp=datetime(2025, 1, 2, 10, 5),
            ),
        ),
        Fragment(
            id="frag-5",
            conversation_id="conv-3",
            role="assistant",
            content="The authentication flow should validate tokens on every request.",
            provenance=Provenance(
                source_kind="claude_conversations",
                source_id="msg-5",
                timestamp=datetime(2025, 1, 3, 14, 0),
            ),
        ),
    ]
