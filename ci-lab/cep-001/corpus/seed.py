"""Seed the local memex corpus with test conversations via SQL."""

import json
import subprocess
from pathlib import Path


def insert(id: str, conv_id: str, role: str, content: str, ts: str):
    """Insert a fragment via memex query."""
    # Escape single quotes for SQL
    content = content.replace("'", "''")
    sql = (
        f"INSERT INTO fragments (id, conversation_id, role, content, timestamp, source_kind, source_id) "
        f"VALUES ('{id}', '{conv_id}', '{role}', '{content}', '{ts}', 'claude_conversations', 'test-corpus')"
    )
    subprocess.run(["memex", "query", sql], capture_output=True, text=True, check=True)


def main():
    export = json.loads(Path("corpus/export.json").read_text())
    count = 0
    for conv in export:
        for msg in conv["chat_messages"]:
            role = "human" if msg["sender"] == "human" else "assistant"
            insert(msg["uuid"], conv["uuid"], role, msg["text"], msg["created_at"])
            count += 1
    print(f"Inserted {count} fragments")

    # Generate embeddings
    print("Running backfill for embeddings...")
    result = subprocess.run(["memex", "backfill"], capture_output=True, text=True)
    print(result.stdout or result.stderr)


if __name__ == "__main__":
    main()
