"""ChatGPT/OpenAI conversations source adapter.

Uses ijson for streaming JSON parse to handle large exports without OOM.
"""

import tempfile
import zipfile
from collections.abc import Iterator
from datetime import UTC, datetime
from importlib.resources import files
from pathlib import Path

import ijson

from memex.domain.models import SOURCE_OPENAI, Fragment, Provenance


class OpenAIConversationsAdapter:
    """Adapter for ChatGPT conversation exports.

    Handles zip exports from ChatGPT (Settings → Data Controls → Export).
    Yields Fragment objects (Karman: Fragment is THE entity).
    """

    def can_handle(self, path: Path) -> bool:
        """Check if this looks like a ChatGPT export."""
        name = path.name.lower()
        # Check filename first
        if "chatgpt" in name or "openai" in name:
            return path.suffix in (".zip", ".json")
        # For zip files, check contents for conversations.json (ChatGPT export signature)
        if path.suffix == ".zip":
            try:
                with zipfile.ZipFile(path, "r") as zf:
                    return "conversations.json" in zf.namelist()
            except zipfile.BadZipFile:
                return False
        return False

    def source_kind(self) -> str:
        return SOURCE_OPENAI

    def ingest(self, path: Path) -> Iterator[Fragment]:
        """Parse ChatGPT export and yield Fragments.

        Export structure:
        [
            {
                "title": "...",
                "create_time": 1234567890.123,
                "mapping": {
                    "uuid": {
                        "id": "uuid",
                        "message": {
                            "author": {"role": "user|assistant|system"},
                            "content": {"parts": ["text"]},
                            "create_time": 1234567890.123
                        },
                        "parent": "parent-uuid",
                        "children": ["child-uuid"]
                    }
                }
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
        """Stream parse JSON using ijson for O(1) memory regardless of file size."""
        with open(path, "rb") as f:
            # Stream through each conversation in the array
            for conversation in ijson.items(f, "item"):
                conv_id = conversation.get("id", conversation.get("title", ""))
                mapping = conversation.get("mapping", {})

                for node_id, node in mapping.items():
                    message = node.get("message")
                    if not message:
                        continue

                    author = message.get("author", {})
                    role = author.get("role", "")

                    # Skip system messages
                    if role == "system":
                        continue

                    # Normalize role
                    if role not in ("user", "assistant"):
                        continue

                    # Extract content
                    content_obj = message.get("content", {})
                    parts = content_obj.get("parts", [])

                    # Handle different content types
                    text_parts = []
                    for part in parts:
                        if isinstance(part, str):
                            text_parts.append(part)
                        elif isinstance(part, dict) and "text" in part:
                            text_parts.append(part["text"])

                    content = "\n".join(text_parts)
                    if not content.strip():
                        continue

                    # Parse timestamp
                    timestamp = self._parse_timestamp(message.get("create_time"))
                    msg_id = message.get("id", node_id)

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
            # Look for conversations.json
            json_files = [
                n for n in zf.namelist() if n.endswith(".json") and "conversation" in n.lower()
            ]
            if not json_files:
                # Try any json file
                json_files = [n for n in zf.namelist() if n.endswith(".json")]

            if not json_files:
                raise ValueError(f"No JSON files found in {path}")

            with tempfile.TemporaryDirectory() as tmpdir:
                extracted = zf.extract(json_files[0], tmpdir)
                yield from self._ingest_json(Path(extracted))

    def _parse_timestamp(self, ts: float | int | None) -> datetime | None:
        """Parse Unix timestamp to datetime."""
        if not ts:
            return None
        try:
            # Handle Decimal or other numeric types from JSON
            return datetime.fromtimestamp(float(ts), tz=UTC)
        except (ValueError, OSError, TypeError):
            return None
