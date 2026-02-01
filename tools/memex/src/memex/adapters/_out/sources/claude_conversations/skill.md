# Claude.ai Conversations Adapter

Ingests conversation exports from Claude.ai.

## How to Export

1. Go to [claude.ai](https://claude.ai)
2. Click your profile → Settings
3. Go to Account → Export Data
4. Wait for email with download link
5. Download the zip file

## Supported Formats

- `.zip` — Claude.ai export zip (contains conversations.json)
- `.json` — Direct conversations.json file

## Usage

```bash
memex ingest ~/Downloads/claude-export.zip
memex ingest ~/Downloads/conversations.json
```

## What Gets Ingested

- All conversations with their UUIDs
- Messages with sender (human → user, assistant)
- Timestamps (created_at)
- Message content (text field)

## Notes

- Empty messages are skipped
- Timestamps are converted to UTC
- source_kind is set to "claude_conversations"
