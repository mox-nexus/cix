# ChatGPT/OpenAI Conversations Adapter

Ingests conversation exports from ChatGPT.

## How to Export

1. Go to [chatgpt.com](https://chatgpt.com)
2. Click your profile → Settings
3. Go to Data Controls → Export Data
4. Wait for email with download link
5. Download the zip file

## Supported Formats

- `.zip` — ChatGPT export zip (contains conversations.json)
- `.json` — Direct conversations.json file

## Usage

```bash
memex ingest ~/Downloads/chatgpt-export.zip
memex ingest ~/Downloads/conversations.json
```

## What Gets Ingested

- All conversations with their IDs
- Messages with sender (user, assistant)
- Timestamps (create_time as Unix timestamp)
- Message content (text parts)
- Nested conversation structure (mapping → nodes)

## Notes

- System messages are skipped
- Empty messages are skipped
- Timestamps are converted to UTC
- source_kind is set to "openai"
- Handles nested content.parts structure
