# Slack Integration Scripts

Direct Slack API integration via Python scripts. Zero external dependencies - uses Python stdlib + curl only.

## Quick Start

### 1. Set Environment Variables

```bash
# Add to ~/.zshrc or ~/.bashrc
export SLACK_BOT_TOKEN="xoxb-your-bot-token"
export SLACK_USER_TOKEN="xoxp-your-user-token"  # Optional, needed for search
export SLACK_TEAM_ID="T..."  # Optional, for Enterprise Grid
export SLACK_DEFAULT_TOKEN="bot"  # Optional, default: bot

# Reload shell
source ~/.zshrc
```

### 2. Get Tokens

Visit https://api.slack.com/apps to create a Slack App and generate tokens.

**Required Bot Token Scopes:**
- `channels:history`, `channels:read`
- `chat:write`, `reactions:write`
- `users:read`, `users:read.email`
- `usergroups:read`

**User Token (optional, for search):**
- `search:read`

### 3. Run Scripts

```bash
# List channels
./slack_list_channels.py --limit 50

# Get channel history
./slack_get_channel_history.py --channel-id C12345678 --limit 20

# Post message
./slack_post_message.py --channel-id C12345678 --text "Hello from script!"

# Get help for any script
./slack_get_channel_info.py --help
```

## Architecture

### Shared Module: `slack_api_client.py`

Core functionality used by all scripts:
- **Token Management**: Bot/user token selection with automatic fallback
- **HTTP Client**: curl subprocess execution (no requests library)
- **Error Classification**: 6 error types (Auth, Permission, NotFound, RateLimit, Validation, Generic)
- **Rate Limiting**: Exponential backoff (1s, 2s, 4s)
- **Token Fallback**: Automatic retry with alternate token on auth/permission errors

### Token Fallback Logic

Critical feature from MCP server implementation:

```python
# Try user token first
try:
    response = client.request('conversations.history', params, use_user_token=True)
except SlackAuthenticationError:
    # Automatically retry with bot token
    response = client.request('conversations.history', params, use_user_token=False)
```

This enables scripts to work even when:
- User token lacks required scopes (falls back to bot)
- Bot token lacks required scopes (falls back to user)
- Token preferences don't match operation requirements

## Available Scripts

### Channels (4 scripts)

**slack_list_channels.py** - List public channels
```bash
./slack_list_channels.py --limit 100
./slack_list_channels.py --cursor dXNlcjpVMDYx  # Pagination
```

**slack_get_channel_info.py** - Get channel details
```bash
./slack_get_channel_info.py --channel-id C12345678
```

**slack_get_channel_history.py** - Get channel messages
```bash
./slack_get_channel_history.py --channel-id C12345678 --limit 50
./slack_get_channel_history.py --channel-id C12345678 --oldest 1234567890.123456
```

**slack_get_thread_replies.py** - Get thread replies
```bash
./slack_get_thread_replies.py --channel-id C12345678 --thread-ts 1234567890.123456
```

### Messages (7 scripts)

**slack_post_message.py** - Post message to channel
```bash
./slack_post_message.py --channel-id C12345678 --text "Hello!"
./slack_post_message.py --channel-id C12345678 --text "Personal message" --use-user-token
```

**slack_send_dm.py** - Send direct message
```bash
./slack_send_dm.py --user-id U12345678 --text "Direct message"
```

**slack_send_group_dm.py** - Send group DM
```bash
./slack_send_group_dm.py --user-ids U123,U456,U789 --text "Group message"
```

**slack_reply_to_thread.py** - Reply to thread
```bash
./slack_reply_to_thread.py --channel-id C123 --thread-ts 1234567890.123456 --text "Reply"
```

**slack_update_message.py** - Update existing message
```bash
./slack_update_message.py --channel-id C123 --timestamp 1234567890.123456 --text "Updated"
```

**slack_add_reaction.py** - Add emoji reaction
```bash
./slack_add_reaction.py --channel-id C123 --timestamp 1234567890.123456 --reaction thumbsup
```

**slack_search_messages.py** - Search messages (requires user token)
```bash
./slack_search_messages.py --query "bug report" --channel-names engineering --count 50
./slack_search_messages.py --query "incident" --count 100
```

### Users (5 scripts)

**slack_get_users.py** - List all users
```bash
./slack_get_users.py --limit 200
```

**slack_get_user_profile.py** - Get user details
```bash
./slack_get_user_profile.py --user-id U12345678
```

**slack_get_user_by_email.py** - Get user by email
```bash
./slack_get_user_by_email.py --email jane.doe@adobe.com
```

**slack_search_users.py** - Search users
```bash
./slack_search_users.py --query "Jane Doe" --limit 10
```

**slack_lookup_user.py** - Lookup user (auto-detects type)
```bash
./slack_lookup_user.py --identifier jane.doe@adobe.com  # Email
./slack_lookup_user.py --identifier jdoe                # Username
./slack_lookup_user.py --identifier U12345678           # User ID
```

### User Groups (2 scripts)

**slack_list_usergroups.py** - List user groups
```bash
./slack_list_usergroups.py
./slack_list_usergroups.py --include-disabled --include-users
```

**slack_get_usergroup_members.py** - Get usergroup members
```bash
./slack_get_usergroup_members.py --usergroup-id S12345678
```

### Utilities

**parse_slack_url.py** - Parse Slack URLs
```bash
./parse_slack_url.py "https://adobe.slack.com/archives/C123/p1234567890123456"
# Output: {"channel_id": "C123", "thread_ts": "1234567890.123456"}
```

## Output Format

### Success Response

```json
{
  "ok": true,
  "data": {
    "channel": "C12345678",
    "messages": [...]
  },
  "execution_time_ms": 245
}
```

### Error Response (stderr)

```json
{
  "ok": false,
  "error_type": "SlackAuthenticationError",
  "message": "Invalid authentication token",
  "method": "conversations.history",
  "help": "Check token validity at https://api.slack.com/apps",
  "timestamp": "2026-03-06T14:30:00Z"
}
```

### Exit Codes

- `0`: Success
- `1`: Slack API error (authentication, permission, not found, validation)
- `2`: Rate limit error
- `3`: Network/connectivity error
- `4`: Parameter validation error

## Error Types

Scripts classify Slack API errors into 6 types:

1. **SlackAuthenticationError**: Invalid/expired tokens
2. **SlackPermissionError**: Missing scopes
3. **SlackResourceNotFoundError**: Channel/user/message not found
4. **SlackRateLimitError**: Rate limit exceeded (includes retry_after)
5. **SlackValidationError**: Invalid parameters
6. **SlackError**: Generic errors

## Advanced Usage

### Pagination

```bash
# Get first page
./slack_get_channel_history.py --channel-id C123 --limit 100 > page1.json

# Extract cursor
CURSOR=$(jq -r '.data.response_metadata.next_cursor' page1.json)

# Get next page
./slack_get_channel_history.py --channel-id C123 --limit 100 --cursor "$CURSOR" > page2.json
```

### JSON Input for Complex Parameters

```bash
# Post message with blocks
echo '{
  "channel": "C123",
  "text": "Fallback text",
  "blocks": [
    {
      "type": "section",
      "text": {"type": "mrkdwn", "text": "Hello *world*"}
    }
  ]
}' | ./slack_post_message.py --json-input
```

### Logging

Enable request logging:

```bash
export SLACK_LOG_FILE=~/Desktop/slack-api.log
./slack_get_channel_history.py --channel-id C123
```

Log format:
```
[2026-03-06 14:30:00] [conversations.history] Token: bot (xoxb-***456)
  Params: {"channel": "C123", "limit": 50}
```

## Testing

Run test suite:

```bash
./test_slack_api_client.py
```

Tests verify:
- Configuration validation
- Error classification
- Token type enum
- Output formatting
- Script executability
- Help documentation

## Comparison with MCP Server

| Feature | MCP Server | Scripts |
|---------|-----------|---------|
| Installation | 5-step setup, Node.js required | Zero setup, scripts in repo |
| Dependencies | npm packages | Python stdlib + curl only |
| Distribution | Separate repository | Included in skill |
| Debugging | Opaque MCP protocol | Direct script execution |
| Token Fallback | ✓ Implemented | ✓ Implemented |
| Rate Limiting | ✓ Implemented | ✓ Implemented |
| Error Classification | ✓ 6 types | ✓ 6 types |
| Feature Parity | 18 operations | 18 operations ✓ |

## Security

**Token Protection:**
- Never commit tokens to version control
- Store in environment variables or secure vault
- Use minimal required scopes
- Rotate tokens periodically

**Token Masking:**
- Tokens are masked in logs: `xoxb-***456`
- Never exposed in error messages
- Redacted from debug output

**Data Privacy:**
- Slack content may contain sensitive information
- Follow data handling policies
- Consider privacy when creating public artifacts

## Troubleshooting

**"No tokens configured"**
- Run: `echo $SLACK_BOT_TOKEN`
- If empty, export tokens in shell config
- Reload shell: `source ~/.zshrc`

**"channel_not_found"**
- Verify channel ID format (C123, D456, G789)
- Check bot is invited to private channels
- Use parse_slack_url.py to extract correct ID

**"Rate limit exceeded"**
- Scripts automatically retry with exponential backoff
- If persists, reduce request frequency
- Check Slack API tier limits

**"ImportError: slack_api_client"**
- Run scripts from skills/slack-integration/scripts directory
- Or add directory to PYTHONPATH

## Contributing

When adding new operations:

1. Add operation to `slack_api_client.py` if needed
2. Create new script following naming pattern: `slack_<operation>.py`
3. Use argparse for CLI arguments
4. Import and use SlackAPIClient
5. Output JSON to stdout, errors to stderr
6. Make executable: `chmod +x slack_<operation>.py`
7. Add tests to `test_slack_api_client.py`
8. Update this README

## Resources

- Slack API Documentation: https://api.slack.com/methods
- Slack App Management: https://api.slack.com/apps
- Architecture Document: `/tmp/claude/slack-mcp-to-skill/iteration-1/IMPORTANT-architecture-slack-direct-api.md`
- Main Skill Documentation: `../SKILL.md`
