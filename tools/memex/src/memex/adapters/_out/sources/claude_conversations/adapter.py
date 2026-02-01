"""Claude.ai conversations source adapter."""

import json
import tempfile
import zipfile
from collections.abc import Iterator
from datetime import datetime
from importlib.resources import files
from pathlib import Path

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
        return "conversation" in name or "claude" in name

    def source_kind(self) -> str:
        return SOURCE_CLAUDE_CONVERSATIONS

    def ingest(self, path: Path) -> Iterator[Fragment]:
        """Parse Claude.ai export and yield Fragments.

        Export structure:
        [
            {
                "uuid": "...",
                "name": "...",
                "chat_messages": [
                    {"uuid": "...", "sender": "human|assistant", "text": "...", "created_at": "..."}
                ]
            }
        ]
        """
        if path.suffix == ".zip":
            yield from self._ingest_zip(path)
        else:
            yield from self._ingest_json(path)

    def skill(self) -> str:
        """Return skill documentation for this adapter."""
        skill_file = files(__package__) / "skill.md"
        return skill_file.read_text()

    def _ingest_json(self, path: Path) -> Iterator[Fragment]:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        for conversation in data:
            conv_id = conversation.get("uuid", "")
            messages = conversation.get("chat_messages", [])

            for msg in messages:
                content = msg.get("text", "")
                if not content:
                    continue

                msg_id = msg.get("uuid", "")
                timestamp = self._parse_timestamp(msg.get("created_at"))
                role = "user" if msg.get("sender") == "human" else "assistant"

                yield Fragment(
                    id=msg_id,
                    conversation_id=conv_id,
                    role=role,
                    content=content,
                    provenance=Provenance(
                        source_kind=self.source_kind(),
                        source_id=msg_id,
                        timestamp=timestamp,
                    ),
                )

    def _ingest_zip(self, path: Path) -> Iterator[Fragment]:
        """Extract and ingest from zip file."""
        with zipfile.ZipFile(path, "r") as zf:
            json_files = [
                n for n in zf.namelist() if n.endswith(".json") and "conversation" in n.lower()
            ]
            if not json_files:
                json_files = [n for n in zf.namelist() if n.endswith(".json")]

            if not json_files:
                raise ValueError(f"No JSON files found in {path}")

            with tempfile.TemporaryDirectory() as tmpdir:
                extracted = zf.extract(json_files[0], tmpdir)
                yield from self._ingest_json(Path(extracted))

    def _parse_timestamp(self, ts: str | None) -> datetime | None:
        if not ts:
            return None
        try:
            return datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return None
