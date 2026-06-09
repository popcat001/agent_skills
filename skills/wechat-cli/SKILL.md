---
name: wechat-cli
description: Query WeChat messages, contacts, sessions, and chat history using the wechat-cli tool. Use when the user wants to search messages, view chat history, list contacts, check unread sessions, export chats, or get new messages from WeChat.
---

# wechat-cli

CLI tool for querying WeChat messages, contacts, and chat data from local WeChat databases.

## Commands

| Command | Description |
|---------|-------------|
| `sessions` | List recent sessions |
| `history` | Get message history for a chat |
| `search` | Search message content |
| `contacts` | Search or list contacts |
| `new-messages` | Get incremental new messages since last call |
| `unread` | View unread sessions |
| `export` | Export chat history to markdown or plain text |
| `members` | List group chat members |
| `favorites` | View WeChat favorites |
| `stats` | Chat statistics and analysis |

## Common Patterns

```bash
# Recent sessions
wechat-cli sessions
wechat-cli sessions --limit 10

# Chat history
wechat-cli history "张三" --limit 20
wechat-cli history "AI交流群" --start-time "2026-04-01"
wechat-cli history "张三" --start-time "2026-04-01" --end-time "2026-05-01"

# Search messages
wechat-cli search "Claude" --chat "AI交流群"   # search within a specific chat
wechat-cli search "你好" --limit 50            # global search

# Contacts
wechat-cli contacts --query "李"

# New messages (incremental polling)
wechat-cli new-messages

# Unread sessions
wechat-cli unread
wechat-cli unread --limit 10
wechat-cli unread --format text

# Export chat
wechat-cli export "张三" --format markdown
wechat-cli export "AI交流群" --format txt --output chat.txt
wechat-cli export "张三" --start-time "2026-04-01" --limit 1000
```

## export Options

| Option | Description |
|--------|-------------|
| `--format [markdown\|txt]` | Output format |
| `--output TEXT` | Output file path (default: stdout) |
| `--start-time TEXT` | Start time: `YYYY-MM-DD [HH:MM[:SS]]` |
| `--end-time TEXT` | End time: `YYYY-MM-DD [HH:MM[:SS]]` |
| `--limit INTEGER` | Max number of messages to export |

## unread Options

| Option | Description |
|--------|-------------|
| `--limit INTEGER` | Max number of sessions to return |
| `--format [json\|text]` | Output format (default: json) |

## Global Options

| Option | Description |
|--------|-------------|
| `--config TEXT` | Path to config.json (auto-detected by default) |
| `--version` | Show version |

## Notes

- Chat names (`"张三"`, `"AI交流群"`) are matched against WeChat display names — use the name as it appears in WeChat.
- `new-messages` tracks state between calls; call it repeatedly to poll for new activity.
- Time filters use format `YYYY-MM-DD` or `YYYY-MM-DD HH:MM` or `YYYY-MM-DD HH:MM:SS`.
- If the config is not found automatically, run `wechat-cli init` first or pass `--config` explicitly.
