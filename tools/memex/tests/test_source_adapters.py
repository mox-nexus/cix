"""Tests for source adapters (Claude and OpenAI)."""

import json
import zipfile

import pytest
from memex.adapters._out.sources.claude_conversations import ClaudeConversationsAdapter
from memex.adapters._out.sources.openai_conversations import OpenAIConversationsAdapter


class TestClaudeAdapter:
    @pytest.fixture
    def adapter(self):
        return ClaudeConversationsAdapter()

    def test_source_kind(self, adapter):
        assert adapter.source_kind() == "claude_conversations"

    def test_can_handle_json(self, adapter, tmp_path):
        f = tmp_path / "conversations.json"
        f.touch()
        assert adapter.can_handle(f) is True

    def test_can_handle_zip(self, adapter, tmp_path):
        f = tmp_path / "claude-export.zip"
        with zipfile.ZipFile(f, "w") as zf:
            zf.writestr("conversations.json", "[]")
        assert adapter.can_handle(f) is True

    def test_cannot_handle_unrelated(self, adapter, tmp_path):
        f = tmp_path / "notes.txt"
        f.touch()
        assert adapter.can_handle(f) is False

    def test_can_handle_data_zip(self, adapter, tmp_path):
        f = tmp_path / "data-2026-02-03-abc.zip"
        with zipfile.ZipFile(f, "w") as zf:
            zf.writestr("conversations.json", "[]")
        assert adapter.can_handle(f) is True

    def test_ingest_conversations(self, adapter, tmp_path):
        data = [
            {
                "uuid": "conv-1",
                "name": "Test Conversation",
                "summary": "A test",
                "created_at": "2025-01-01T12:00:00Z",
                "chat_messages": [
                    {
                        "uuid": "msg-1",
                        "sender": "human",
                        "text": "Hello Claude",
                        "created_at": "2025-01-01T12:00:00Z",
                        "content": [],
                        "attachments": [],
                    },
                    {
                        "uuid": "msg-2",
                        "sender": "assistant",
                        "text": "Hello! How can I help?",
                        "created_at": "2025-01-01T12:01:00Z",
                        "content": [],
                        "attachments": [],
                    },
                ],
            }
        ]
        f = tmp_path / "conversations.json"
        f.write_text(json.dumps(data))

        fragments = list(adapter.ingest(f))
        # Summary + 2 messages
        assert len(fragments) == 3
        roles = {frag.role for frag in fragments}
        assert "user" in roles
        assert "assistant" in roles
        assert "summary" in roles

    def test_ingest_artifacts(self, adapter, tmp_path):
        data = [
            {
                "uuid": "conv-1",
                "chat_messages": [
                    {
                        "uuid": "msg-1",
                        "sender": "assistant",
                        "text": "",
                        "created_at": "2025-01-01T12:00:00Z",
                        "content": [
                            {
                                "type": "tool_use",
                                "name": "artifacts",
                                "input": {
                                    "id": "art-1",
                                    "title": "Test Code",
                                    "content": "print('hello')",
                                },
                            }
                        ],
                        "attachments": [],
                    }
                ],
            }
        ]
        f = tmp_path / "conversations.json"
        f.write_text(json.dumps(data))

        fragments = list(adapter.ingest(f))
        artifacts = [frag for frag in fragments if frag.role == "artifact"]
        assert len(artifacts) == 1
        assert "Test Code" in artifacts[0].content

    def test_ingest_thinking(self, adapter, tmp_path):
        data = [
            {
                "uuid": "conv-1",
                "chat_messages": [
                    {
                        "uuid": "msg-1",
                        "sender": "assistant",
                        "text": "answer",
                        "created_at": "2025-01-01T12:00:00Z",
                        "content": [{"type": "thinking", "thinking": "Let me consider..."}],
                        "attachments": [],
                    }
                ],
            }
        ]
        f = tmp_path / "conversations.json"
        f.write_text(json.dumps(data))

        fragments = list(adapter.ingest(f))
        thinking = [frag for frag in fragments if frag.role == "thinking"]
        assert len(thinking) == 1
        assert "consider" in thinking[0].content

    def test_ingest_attachments(self, adapter, tmp_path):
        data = [
            {
                "uuid": "conv-1",
                "chat_messages": [
                    {
                        "uuid": "msg-1",
                        "sender": "human",
                        "text": "check this file",
                        "created_at": "2025-01-01T12:00:00Z",
                        "content": [],
                        "attachments": [
                            {
                                "file_name": "notes.txt",
                                "extracted_content": "Important notes here",
                            }
                        ],
                    }
                ],
            }
        ]
        f = tmp_path / "conversations.json"
        f.write_text(json.dumps(data))

        fragments = list(adapter.ingest(f))
        attachments = [frag for frag in fragments if frag.role == "attachment"]
        assert len(attachments) == 1
        assert "notes.txt" in attachments[0].content

    def test_ingest_zip(self, adapter, tmp_path):
        conv_data = [
            {
                "uuid": "conv-1",
                "chat_messages": [
                    {
                        "uuid": "msg-1",
                        "sender": "human",
                        "text": "Hello",
                        "created_at": "2025-01-01T12:00:00Z",
                        "content": [],
                        "attachments": [],
                    }
                ],
            }
        ]
        memories_data = [
            {
                "conversations_memory": "Remember to use OAuth",
                "project_memories": {"proj-1": "Use hexagonal arch"},
            }
        ]
        projects_data = [
            {
                "uuid": "proj-1",
                "name": "Test Project",
                "created_at": "2025-01-01T12:00:00Z",
                "prompt_template": "You are a helpful assistant",
                "docs": [],
            }
        ]

        zip_path = tmp_path / "claude-export.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("conversations.json", json.dumps(conv_data))
            zf.writestr("memories.json", json.dumps(memories_data))
            zf.writestr("projects.json", json.dumps(projects_data))

        fragments = list(adapter.ingest(zip_path))
        roles = {frag.role for frag in fragments}
        assert "user" in roles
        assert "memory" in roles
        assert "project_prompt" in roles

    def test_empty_text_skipped(self, adapter, tmp_path):
        data = [
            {
                "uuid": "conv-1",
                "chat_messages": [
                    {
                        "uuid": "msg-1",
                        "sender": "human",
                        "text": "  ",
                        "created_at": "2025-01-01T12:00:00Z",
                        "content": [],
                        "attachments": [],
                    }
                ],
            }
        ]
        f = tmp_path / "conversations.json"
        f.write_text(json.dumps(data))

        fragments = list(adapter.ingest(f))
        assert all(frag.content.strip() for frag in fragments)


class TestOpenAIAdapter:
    @pytest.fixture
    def adapter(self):
        return OpenAIConversationsAdapter()

    def test_source_kind(self, adapter):
        assert adapter.source_kind() == "openai"

    def test_can_handle_chatgpt_zip(self, adapter, tmp_path):
        f = tmp_path / "chatgpt-export.zip"
        with zipfile.ZipFile(f, "w") as zf:
            zf.writestr("conversations.json", "[]")
        assert adapter.can_handle(f) is True

    def test_cannot_handle_unrelated(self, adapter, tmp_path):
        f = tmp_path / "data.csv"
        f.touch()
        assert adapter.can_handle(f) is False

    def test_ingest_json(self, adapter, tmp_path):
        data = [
            {
                "id": "conv-1",
                "title": "Test Chat",
                "create_time": 1704067200.0,
                "mapping": {
                    "node-1": {
                        "id": "node-1",
                        "message": {
                            "id": "msg-1",
                            "author": {"role": "user"},
                            "content": {"parts": ["What is OAuth?"]},
                            "create_time": 1704067200.0,
                        },
                    },
                    "node-2": {
                        "id": "node-2",
                        "message": {
                            "id": "msg-2",
                            "author": {"role": "assistant"},
                            "content": {"parts": ["OAuth is an authorization framework."]},
                            "create_time": 1704067260.0,
                        },
                    },
                    "node-sys": {
                        "id": "node-sys",
                        "message": {
                            "id": "msg-sys",
                            "author": {"role": "system"},
                            "content": {"parts": ["You are ChatGPT"]},
                            "create_time": 1704067190.0,
                        },
                    },
                },
            }
        ]
        f = tmp_path / "conversations.json"
        f.write_text(json.dumps(data))

        fragments = list(adapter.ingest(f))
        # System messages should be skipped
        assert len(fragments) == 2
        roles = {frag.role for frag in fragments}
        assert "user" in roles
        assert "assistant" in roles
        assert "system" not in roles

    def test_ingest_skips_empty_parts(self, adapter, tmp_path):
        data = [
            {
                "id": "conv-1",
                "title": "Test",
                "mapping": {
                    "node-1": {
                        "id": "node-1",
                        "message": {
                            "id": "msg-1",
                            "author": {"role": "user"},
                            "content": {"parts": ["  "]},
                            "create_time": 1704067200.0,
                        },
                    }
                },
            }
        ]
        f = tmp_path / "conversations.json"
        f.write_text(json.dumps(data))

        fragments = list(adapter.ingest(f))
        assert len(fragments) == 0

    def test_ingest_zip(self, adapter, tmp_path):
        data = [
            {
                "id": "conv-1",
                "title": "Test",
                "mapping": {
                    "node-1": {
                        "id": "node-1",
                        "message": {
                            "id": "msg-1",
                            "author": {"role": "user"},
                            "content": {"parts": ["Hello GPT"]},
                            "create_time": 1704067200.0,
                        },
                    }
                },
            }
        ]
        zip_path = tmp_path / "chatgpt-export.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("conversations.json", json.dumps(data))

        fragments = list(adapter.ingest(zip_path))
        assert len(fragments) == 1
        assert fragments[0].provenance.source_kind == "openai"
