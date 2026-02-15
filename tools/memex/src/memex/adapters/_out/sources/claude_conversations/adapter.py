"""Claude.ai conversations source adapter.

Uses ijson for streaming JSON parse to handle large exports without OOM.

Extracts:
- Conversation messages (from chat_messages[].text)
- Artifacts (from chat_messages[].content[] tool_use blocks)
- Conversation summaries (from conversation name + summary)
- Memories (from memories.json — global + per-project)
- Projects (from projects.json — prompt templates + uploaded docs)
"""

import json
import tempfile
import zipfile
from collections.abc import Iterator
from datetime import datetime
from importlib.resources import files
from pathlib import Path

import ijson

from memex.domain.models import SOURCE_CLAUDE_CONVERSATIONS, Fragment, Provenance


class ClaudeConversationsAdapter:
    """Adapter for Claude.ai conversation exports.

    Handles both raw JSON and zip exports.
    Yields Fragment objects (Karman: Fragment is THE entity).
    """

    def can_handle(self, path: Path) -> bool:
        """Check if this looks like a Claude.ai export."""
        if path.suffix not in (".json", ".zip"):
            return False
        name = path.name.lower()
        # Match old format (conversations.json, claude-export.zip)
        # and new format (data-2026-02-03-*.zip with conversations.json inside)
        if "conversation" in name or "claude" in name:
            return True
        # Check for new Anthropic export format (data-YYYY-MM-DD-*.zip)
        if name.startswith("data-") and path.suffix == ".zip":
            return self._is_claude_zip(path)
        return False

    def _is_claude_zip(self, path: Path) -> bool:
        """Check if zip contains conversations.json (Claude export marker)."""
        try:
            with zipfile.ZipFile(path, "r") as zf:
                return "conversations.json" in zf.namelist()
        except (zipfile.BadZipFile, OSError):
            return False

    def source_kind(self) -> str:
        return SOURCE_CLAUDE_CONVERSATIONS

    def ingest(self, path: Path) -> Iterator[Fragment]:
        """Parse Claude.ai export and yield Fragments.

        For zip exports: processes conversations.json, memories.json, projects.json.
        For raw JSON: processes as conversations only.
        """
        if path.suffix == ".zip":
            yield from self._ingest_zip(path)
        else:
            yield from self._ingest_conversations(path)

    def skill(self) -> str:
        """Return skill documentation for this adapter."""
        skill_file = files(__package__) / "skill.md"
        return skill_file.read_text()

    # ── Conversations ──────────────────────────────────────────────

    def _ingest_conversations(self, path: Path) -> Iterator[Fragment]:
        """Stream parse conversations JSON. Yields messages, artifacts, and summaries."""
        with open(path, "rb") as f:
            for conversation in ijson.items(f, "item"):
                yield from self._process_conversation(conversation)

    def _process_conversation(self, conversation: dict) -> Iterator[Fragment]:
        """Extract all fragments from a single conversation."""
        conv_id = conversation.get("uuid", "")
        conv_name = conversation.get("name", "")
        conv_summary = conversation.get("summary", "")
        conv_created = self._parse_timestamp(conversation.get("created_at"))

        # Conversation summary fragment (makes conversation titles searchable)
        if conv_name or conv_summary:
            parts = []
            if conv_name:
                parts.append(f"# {conv_name}")
            if conv_summary:
                parts.append(conv_summary)
            yield Fragment(
                id=f"{conv_id}:summary",
                conversation_id=conv_id,
                role="summary",
                content="\n\n".join(parts),
                provenance=Provenance(
                    source_kind=self.source_kind(),
                    source_id=f"{conv_id}:summary",
                    timestamp=conv_created,
                ),
            )

        # Messages and artifacts
        for msg in conversation.get("chat_messages", []):
            yield from self._process_message(msg, conv_id)

    def _process_message(self, msg: dict, conv_id: str) -> Iterator[Fragment]:
        """Extract message and artifact fragments from a single message."""
        msg_id = msg.get("uuid", "")
        timestamp = self._parse_timestamp(msg.get("created_at"))
        role = "user" if msg.get("sender") == "human" else "assistant"

        # Message fragment from text field (preserves existing behavior)
        text = msg.get("text", "")
        if text.strip():
            yield Fragment(
                id=msg_id,
                conversation_id=conv_id,
                role=role,
                content=text,
                provenance=Provenance(
                    source_kind=self.source_kind(),
                    source_id=msg_id,
                    timestamp=timestamp,
                ),
            )

        # Structured content[] — artifacts, thinking, tool use
        for idx, block in enumerate(msg.get("content", [])):
            if not isinstance(block, dict):
                continue

            block_type = block.get("type", "")
            block_ts = self._parse_timestamp(block.get("start_timestamp"))

            # Artifacts (Claude-generated documents, code, analyses)
            if block_type == "tool_use" and block.get("name") == "artifacts":
                artifact_input = block.get("input", {})
                artifact_id = artifact_input.get("id", "")
                artifact_title = artifact_input.get("title", "Untitled")
                artifact_content = artifact_input.get("content", "")

                if not artifact_content:
                    continue

                yield Fragment(
                    id=f"{msg_id}:artifact:{artifact_id}",
                    conversation_id=conv_id,
                    role="artifact",
                    content=f"# {artifact_title}\n\n{artifact_content}",
                    provenance=Provenance(
                        source_kind=self.source_kind(),
                        source_id=f"{msg_id}:artifact:{artifact_id}",
                        timestamp=block_ts,
                    ),
                )

            # Thinking (Claude's extended reasoning — the CIS reasoning process)
            elif block_type == "thinking":
                thinking_text = block.get("thinking", "")
                if not thinking_text or not thinking_text.strip():
                    continue

                yield Fragment(
                    id=f"{msg_id}:thinking:{idx}",
                    conversation_id=conv_id,
                    role="thinking",
                    content=thinking_text,
                    provenance=Provenance(
                        source_kind=self.source_kind(),
                        source_id=f"{msg_id}:thinking:{idx}",
                        timestamp=block_ts,
                    ),
                )

        # Attachment fragments (uploaded files with extracted text)
        for i, att in enumerate(msg.get("attachments", [])):
            if not isinstance(att, dict):
                continue
            extracted = att.get("extracted_content", "")
            if not extracted or not extracted.strip():
                continue

            file_name = att.get("file_name", "attachment")
            yield Fragment(
                id=f"{msg_id}:attachment:{i}",
                conversation_id=conv_id,
                role="attachment",
                content=f"# {file_name}\n\n{extracted}",
                provenance=Provenance(
                    source_kind=self.source_kind(),
                    source_id=f"{msg_id}:attachment:{i}",
                    timestamp=timestamp,
                ),
            )

    # ── Memories ───────────────────────────────────────────────────

    def _ingest_memories(self, path: Path) -> Iterator[Fragment]:
        """Parse memories.json — global conversation memory + per-project memories."""
        with open(path) as f:
            data = json.load(f)

        if not data or not isinstance(data, list):
            return

        mem = data[0]

        # Global conversation memory
        conv_memory = mem.get("conversations_memory", "")
        if conv_memory and conv_memory.strip():
            yield Fragment(
                id="memory:global",
                conversation_id=None,
                role="memory",
                content=f"# Conversation Memory\n\n{conv_memory}",
                provenance=Provenance(
                    source_kind=self.source_kind(),
                    source_id="memory:global",
                ),
            )

        # Per-project memories (keyed by project UUID)
        project_memories = mem.get("project_memories", {})
        if isinstance(project_memories, dict):
            for project_uuid, memory_text in project_memories.items():
                if not memory_text or not memory_text.strip():
                    continue
                yield Fragment(
                    id=f"memory:project:{project_uuid}",
                    conversation_id=project_uuid,
                    role="memory",
                    content=f"# Project Memory\n\n{memory_text}",
                    provenance=Provenance(
                        source_kind=self.source_kind(),
                        source_id=f"memory:project:{project_uuid}",
                    ),
                )

    # ── Projects ───────────────────────────────────────────────────

    def _ingest_projects(self, path: Path) -> Iterator[Fragment]:
        """Parse projects.json — prompt templates and uploaded docs."""
        with open(path) as f:
            data = json.load(f)

        if not isinstance(data, list):
            return

        for project in data:
            project_uuid = project.get("uuid", "")
            project_name = project.get("name", "Untitled Project")
            created_at = self._parse_timestamp(project.get("created_at"))

            # Project prompt template
            prompt = project.get("prompt_template", "")
            if prompt and prompt.strip():
                yield Fragment(
                    id=f"project:{project_uuid}:prompt",
                    conversation_id=project_uuid,
                    role="project_prompt",
                    content=f"# {project_name}\n\n{prompt}",
                    provenance=Provenance(
                        source_kind=self.source_kind(),
                        source_id=f"project:{project_uuid}:prompt",
                        timestamp=created_at,
                    ),
                )

            # Uploaded docs
            for doc in project.get("docs", []):
                doc_uuid = doc.get("uuid", "")
                doc_name = doc.get("filename", "Untitled")
                doc_content = doc.get("content", "")
                doc_created = self._parse_timestamp(doc.get("created_at"))

                if not doc_content or not doc_content.strip():
                    continue

                yield Fragment(
                    id=f"project:{project_uuid}:doc:{doc_uuid}",
                    conversation_id=project_uuid,
                    role="document",
                    content=f"# {doc_name}\n\n{doc_content}",
                    provenance=Provenance(
                        source_kind=self.source_kind(),
                        source_id=f"project:{project_uuid}:doc:{doc_uuid}",
                        timestamp=doc_created,
                    ),
                )

    # ── Zip handling ───────────────────────────────────────────────

    def _ingest_zip(self, path: Path) -> Iterator[Fragment]:
        """Extract and ingest all supported files from zip export."""
        with zipfile.ZipFile(path, "r") as zf:
            namelist = zf.namelist()

            with tempfile.TemporaryDirectory() as tmpdir:
                # Conversations (required)
                conv_files = [
                    n for n in namelist if n.endswith(".json") and "conversation" in n.lower()
                ]
                if not conv_files:
                    raise ValueError(f"No conversations.json found in {path}")

                extracted = zf.extract(conv_files[0], tmpdir)
                yield from self._ingest_conversations(Path(extracted))

                # Memories (optional)
                if "memories.json" in namelist:
                    extracted = zf.extract("memories.json", tmpdir)
                    yield from self._ingest_memories(Path(extracted))

                # Projects (optional)
                if "projects.json" in namelist:
                    extracted = zf.extract("projects.json", tmpdir)
                    yield from self._ingest_projects(Path(extracted))

    # ── Utilities ──────────────────────────────────────────────────

    def _parse_timestamp(self, ts: str | None) -> datetime | None:
        if not ts:
            return None
        try:
            return datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return None
