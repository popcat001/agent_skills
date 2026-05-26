---
name: slack-integration
description: This skill should be used when working with Slack to read messages, threads, channels, search conversations, or create Jira tickets from Slack content. Use when the user mentions Slack operations, wants to extract information from Slack threads, or needs to create Jira issues from Slack discussions. Provides direct Slack API access via Python scripts.
---

> **IMPORTANT**: Always use the `--use-user-token` flag when calling any script that supports it. This sends messages and performs actions on behalf of the user (via SLACK_USER_TOKEN) instead of the bot. This applies to all write operations: `slack_post_message.py`, `slack_reply_to_thread.py`, `slack_send_dm.py`, `slack_send_group_dm.py`, `slack_update_message.py`, `slack_add_reaction.py`.

# Slack Integration

## Overview

This skill provides comprehensive capabilities for working with Slack at Adobe, including reading messages and threads, searching conversations, and integrating with Jira for issue creation. It uses Python scripts that call the Slack API directly, eliminating the need for MCP server installation.

**Key Capabilities**:
- Parse Slack URLs to extract channel and thread identifiers
- Read channel history and thread replies
- Search for messages across channels
- Create Jira tickets from Slack threads or conversations
- Post messages and reply to threads
- Look up users and channels

## Prerequisites

### Environment Configuration

**Required**: Set up Slack API tokens as environment variables.

**Configuration**:
1. Export environment variables (add to `~/.zshrc` or `~/.bashrc`):
   ```bash
   export SLACK_BOT_TOKEN="xoxb-..."      # Required for most operations
   export SLACK_USER_TOKEN="xoxp-..."    # Required for search operations
   export SLACK_TEAM_ID="T..."           # Optional, for Enterprise Grid
   export SLACK_DEFAULT_TOKEN="bot"      # Optional, default: bot
   ```

2. Reload shell configuration:
   ```bash
   source ~/.zshrc  # or ~/.bashrc
   ```

**Detailed Token Setup**:

#### Step 1: Create a Slack App

1. Visit https://api.slack.com/apps
2. Click **"Create New App"** → **"From scratch"**
3. Enter app name (e.g., "Claude Code Integration")
4. Select your Adobe workspace
5. Click **"Create App"**

#### Step 2: Configure Bot Token Scopes

1. Navigate to **"OAuth & Permissions"** in the sidebar
2. Scroll to **"Scopes"** → **"Bot Token Scopes"**
3. Add the following scopes:
   - `channels:history` - Read messages from public channels
   - `channels:read` - View basic channel info
   - `chat:write` - Post messages
   - `reactions:write` - Add emoji reactions
   - `users:read` - View users in workspace
   - `users:read.email` - View email addresses
   - `usergroups:read` - View user groups
   - `groups:history` - Read private channel messages (optional)
   - `im:history` - Read direct messages (optional)
   - `mpim:history` - Read group DMs (optional)

#### Step 3: Install App to Workspace

1. Scroll to **"OAuth Tokens for Your Workspace"**
2. Click **"Install to Workspace"**
3. Review permissions and click **"Allow"**
4. Copy the **Bot User OAuth Token** (starts with `xoxb-`)

#### Step 4: Get User Token (Optional, for Search)

User tokens are needed for `slack_search_messages` functionality:

1. Navigate to **"OAuth & Permissions"**
2. Scroll to **"User Token Scopes"**
3. Add scope: `search:read`
4. Reinstall app to workspace
5. Copy the **User OAuth Token** (starts with `xoxp-`)

#### Step 5: Invite Bot to Channels

For **private channels**, you must invite the bot:

1. Open the private channel in Slack
2. Type: `/invite @your-bot-name`
3. The bot will now have access to read/write messages

**Note**: Public channels don't require invitation, but the bot can only see messages after it joins.

#### Step 6: Verify Setup

```bash
cd skills/slack-integration/scripts
./slack_list_channels.py --limit 5
```

If successful, you'll see a JSON response with channel information.

#### Common Token Issues

**Token starts with wrong prefix**:
- Bot token MUST start with `xoxb-`
- User token MUST start with `xoxp-`
- If you see `xoxa-` or other prefixes, regenerate the correct token type

**"invalid_auth" error**:
- Token may have been revoked - check at https://api.slack.com/apps
- Verify you copied the entire token (they're long!)
- Reinstall app to workspace to refresh tokens

**"missing_scope" error**:
- Add the required scope in app settings
- **Important**: After adding scopes, you MUST reinstall the app
- New tokens will be generated with updated permissions

**Enterprise Grid workspaces**:
- Set `SLACK_TEAM_ID` if you have multiple workspaces
- Find Team ID in workspace settings → About This Workspace

**Required Dependencies**:
- Python 3.7+ (already available)
- `curl` command (already available on macOS/Linux)
- No pip packages required - uses Python stdlib only

### Jira Integration

For creating Jira tickets from Slack content, ensure the `/jira-integration` skill is available with:
- `JIRA_TOKEN` environment variable configured
- Adobe VPN connection active
- Access to target Jira project (e.g., GS)

## Core Capabilities

### 1. Parsing Slack URLs

Slack URLs come in several formats. Extract the necessary identifiers to use with Python scripts.

**Implementation**: Uses `scripts/parse_slack_url.py`

**Common URL Formats**:

```
# Channel message with timestamp
https://adobe.slack.com/archives/C12345678/p1234567890123456

# Thread (message with replies)
https://adobe.slack.com/archives/C12345678/p1234567890123456?thread_ts=1234567890.123456

# Channel link
https://adobe.slack.com/archives/C12345678
```

**Parsing Logic**:

```python
# Extract from URL like: https://adobe.slack.com/archives/C12345678/p1234567890123456
# Channel ID: C12345678 (starts with C, D, or G)
# Timestamp: 1234567890.123456 (convert p1234567890123456 -> 1234567890.123456)

import re

def parse_slack_url(url: str) -> dict:
    """Parse Slack URL to extract channel_id and timestamp"""
    result = {}

    # Extract channel ID (C, D, or G prefix)
    channel_match = re.search(r'/archives/([CDG][A-Z0-9]+)', url)
    if channel_match:
        result['channel_id'] = channel_match.group(1)

    # Extract timestamp from p-format (p1234567890123456 -> 1234567890.123456)
    ts_match = re.search(r'/p(\d{10})(\d{6})', url)
    if ts_match:
        result['timestamp'] = f"{ts_match.group(1)}.{ts_match.group(2)}"
        result['thread_ts'] = result['timestamp']  # Parent message timestamp

    # Extract thread_ts if present
    thread_match = re.search(r'thread_ts=(\d+\.\d+)', url)
    if thread_match:
        result['thread_ts'] = thread_match.group(1)

    return result

# Example usage:
# url = "https://adobe.slack.com/archives/C12345678/p1234567890123456"
# parsed = parse_slack_url(url)
# -> {'channel_id': 'C12345678', 'timestamp': '1234567890.123456', 'thread_ts': '1234567890.123456'}
```

**Reference**: See `references/slack_url_parsing.md` for comprehensive URL format documentation

### 2. Reading Slack Content

Use Python scripts to read messages and threads directly from Slack API.

**Available Scripts**:

#### `slack_get_channel_history.py`
Get recent messages from a channel.

```bash
# Example: Get last 20 messages from a channel
./scripts/slack_get_channel_history.py --channel-id C12345678 --limit 20

# With pagination
./scripts/slack_get_channel_history.py --channel-id C12345678 --limit 100 --cursor dXNlcjpVMDYx
```

**Returns**: JSON with messages array, including content, author, timestamp, and metadata

#### `slack_get_thread_replies.py`
Get all replies in a message thread.

```bash
# Example: Get all replies in a thread
./scripts/slack_get_thread_replies.py --channel-id C12345678 --thread-ts 1234567890.123456
```

**Returns**: JSON with messages array containing thread replies

**Common Pattern - Read Thread from URL**:

```bash
# User provides: "https://adobe.slack.com/archives/C12345678/p1234567890123456"

# 1. Parse URL to extract identifiers
./scripts/parse_slack_url.py "https://adobe.slack.com/archives/C12345678/p1234567890123456"
# Output: {"channel_id": "C12345678", "thread_ts": "1234567890.123456"}

# 2. Get thread replies
./scripts/slack_get_thread_replies.py --channel-id C12345678 --thread-ts 1234567890.123456

# 3. Process JSON output to extract key information for downstream operations
```

#### `slack_search_messages.py`
Search for messages across channels.

```bash
# Example: Search for bug reports in engineering channel
./scripts/slack_search_messages.py --query "bug report" --channel-names engineering --count 50

# Search across all channels
./scripts/slack_search_messages.py --query "incident" --count 100
```

**Note**: Requires `SLACK_USER_TOKEN` with `search:read` scope

**Returns**: JSON with matching messages, including content, channel, timestamp, and metadata

### 3. Channel and User Information

Get information about channels and users.

#### `slack_list_channels.py`
List public channels in workspace.

```bash
./scripts/slack_list_channels.py --limit 100
./scripts/slack_list_channels.py --limit 50 --cursor dXNlcjpVMDYx  # With pagination
```

#### `slack_get_channel_info.py`
Get details about a specific channel.

```bash
./scripts/slack_get_channel_info.py --channel-id C12345678
```

#### `slack_lookup_user.py`
Find user by email, username, or user ID with auto-detection.

```bash
# By email
./scripts/slack_lookup_user.py --identifier jdoe@adobe.com

# By username
./scripts/slack_lookup_user.py --identifier jdoe

# By user ID
./scripts/slack_lookup_user.py --identifier U12345678
```

**Auto-detection**:
- Contains "@" → email lookup
- Starts with "U" → user_id lookup
- Otherwise → username lookup

### 4. Posting Messages and Replies

Send messages to channels or reply to threads.

#### `slack_post_message.py`
Post a new message to a channel.

```bash
# Post as bot (default)
./scripts/slack_post_message.py --channel-id C12345678 --text "Message content"

# Post as user
./scripts/slack_post_message.py --channel-id C12345678 --text "Personal message" --use-user-token

# Post to thread
./scripts/slack_post_message.py --channel-id C12345678 --text "Reply" --thread-ts 1234567890.123456
```

#### `slack_reply_to_thread.py`
Reply to a specific thread.

```bash
./scripts/slack_reply_to_thread.py --channel-id C12345678 --thread-ts 1234567890.123456 --text "Reply content"

# Reply as user
./scripts/slack_reply_to_thread.py --channel-id C12345678 --thread-ts 1234567890.123456 --text "Personal reply" --use-user-token
```

#### `slack_add_reaction.py`
Add emoji reaction to a message.

```bash
# Add reaction (emoji name without colons)
./scripts/slack_add_reaction.py --channel-id C12345678 --timestamp 1234567890.123456 --reaction white_check_mark

# Add reaction as user
./scripts/slack_add_reaction.py --channel-id C12345678 --timestamp 1234567890.123456 --reaction thumbsup --use-user-token
```

### 5. Creating Jira Tickets from Slack Threads

**Primary Use Case**: Convert Slack discussions into actionable Jira tickets.

**Workflow**:

```
1. User provides Slack thread URL
   Example: "https://adobe.slack.com/archives/C12345678/p1234567890123456"

2. Parse the URL
   Extract: channel_id = C12345678, thread_ts = 1234567890.123456

3. Fetch thread content
   Tool: slack_get_thread_replies
   Input: {"channel_id": "C12345678", "thread_ts": "1234567890.123456"}

4. Analyze and summarize thread
   - Identify the main issue/request
   - Extract key points and context
   - Identify participants
   - Determine issue type (bug, feature request, task, etc.)

5. Format Jira description
   Create description following Jira best practices:

   h3. Summary
   [ELI5 explanation of the issue/request]

   h3. Context from Slack
   *Original Thread*: [Slack Thread|<original_url>]
   *Participants*: @user1, @user2, @user3
   *Date*: 2026-03-06

   h3. Discussion Summary
   [Concise summary of the thread discussion, key points, and decisions]

   h3. Acceptance Criteria
   # [Derived from thread discussion]
   # [Additional criteria as needed]

   h3. Additional Context
   See original Slack thread for full discussion history.

6. Create Jira issue
   Use /jira-integration skill:
   python3 scripts/jira_create.py \
     --project GS \
     --summary "Short title from thread" \
     --description-file /tmp/issue_desc.txt \
     --type Story \
     --assignee [derived from thread or unassigned] \
     --components [if applicable]

7. Link back to Slack (optional)
   Tool: slack_reply_to_thread
   Input: {
     "channel_id": "C12345678",
     "thread_ts": "1234567890.123456",
     "text": "Created Jira ticket: https://jira.corp.adobe.com/browse/GS-12345"
   }
```

**Example**:

```
User: "Create a Jira ticket from this Slack thread:
       https://adobe.slack.com/archives/C12345678/p1234567890123456"

Agent:
1. Parse URL → channel_id: C12345678, thread_ts: 1234567890.123456

2. Call slack_get_thread_replies with parsed identifiers

3. Analyze thread content:
   - Original message: "We need to add rate limiting to the API"
   - Replies discuss implementation approach
   - Conclusion: Use token bucket algorithm, limit 100 req/min

4. Create description file:
   cat > /tmp/jira_desc.txt <<'EOF'
   h3. Summary
   Add rate limiting to the API to prevent abuse and ensure fair usage.

   h3. Context from Slack
   *Original Thread*: [Slack Discussion|https://adobe.slack.com/archives/C12345678/p1234567890123456]
   *Participants*: @jdoe, @asmith, @bwilson
   *Date*: 2026-03-06

   h3. Discussion Summary
   Team discussed adding rate limiting after noticing API abuse patterns.
   Agreed on token bucket algorithm with 100 requests per minute limit.
   Should return 429 status code when limit exceeded.

   h3. Acceptance Criteria
   # Implement token bucket rate limiting algorithm
   # Limit: 100 requests per minute per API key
   # Return HTTP 429 when limit exceeded
   # Include Retry-After header in 429 response
   # Add rate limit headers to all responses (X-RateLimit-Limit, X-RateLimit-Remaining)
   # Add monitoring metrics for rate limit hits

   h3. Additional Context
   See original Slack thread for full discussion history and technical details.
   EOF

5. Create Jira issue:
   python3 /path/to/jira-integration/scripts/jira_create.py \
     --project GS \
     --summary "Add rate limiting to API" \
     --description-file /tmp/jira_desc.txt \
     --type Story \
     --assignee jdoe \
     --priority High \
     --components API

6. Reply to thread:
   slack_reply_to_thread({
     "channel_id": "C12345678",
     "thread_ts": "1234567890.123456",
     "text": "Created Jira ticket: https://jira.corp.adobe.com/browse/GS-12345"
   })
```

**Best Practices**:
- Always include link to original Slack thread in Jira description
- List thread participants for context
- Summarize discussion, don't copy entire conversation
- Extract actionable acceptance criteria from discussion
- Follow Jira description best practices (see `/jira-integration` skill)
- Reply back to Slack thread with Jira ticket link for traceability

### 6. Common Workflow Patterns

#### Pattern: Monitor Channel for Keywords

```
Use Case: Track mentions of "incident", "outage", "down" in #alerts channel

1. Search recent messages:
   slack_search_messages({
     "query": "incident OR outage OR down",
     "channel_names": ["alerts"],
     "count": 20
   })

2. Filter results by time (last 24 hours)

3. For each incident:
   - Check if Jira ticket already exists
   - If not, create ticket with context
   - Reply to thread with ticket link
```

#### Pattern: Daily Standup Summary

```
Use Case: Summarize #engineering channel activity for standup

1. Get channel history:
   slack_get_channel_history({
     "channel_id": "C12345678",
     "limit": 100
   })

2. Filter messages from last 24 hours

3. Categorize by topic:
   - Issues/blockers
   - Completed work
   - Questions/discussions

4. Post summary to #standup channel
```

#### Pattern: Bug Report from Slack to Jira

```
Use Case: User reports bug in #bugs channel

1. User provides message link:
   "https://adobe.slack.com/archives/C12345678/p1234567890123456"

2. Parse URL and fetch message/thread

3. Extract bug details:
   - Error description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment info

4. Create Jira bug with extracted info:
   - Type: Bug
   - Priority: Based on severity mentioned
   - Include Slack link for context

5. Reply with Jira ticket link
```

#### Pattern: Feature Request Triage

```
Use Case: Triage feature requests from #feature-requests

1. Search for unprocessed requests:
   slack_search_messages({
     "query": "feature request",
     "channel_names": ["feature-requests"],
     "count": 50
   })

2. For each request without ✅ reaction:
   - Read full thread
   - Assess feasibility and scope
   - Create Jira story if approved
   - Add ✅ reaction to mark as processed
```

## Available Scripts Reference

All scripts are located in `./scripts/` directory and are executable Python scripts.

### Reading Content
- `slack_get_channel_history.py` - Get recent messages from channel
- `slack_get_thread_replies.py` - Get all replies in a thread
- `slack_search_messages.py` - Search messages across channels (requires user token)

### Channel & User Info
- `slack_list_channels.py` - List public channels
- `slack_get_channel_info.py` - Get channel details
- `slack_get_users.py` - List workspace users
- `slack_get_user_profile.py` - Get user profile details
- `slack_lookup_user.py` - Find user by email/username/ID (auto-detection)
- `slack_search_users.py` - Search for users by name
- `slack_get_user_by_email.py` - Get user by email address
- `slack_list_usergroups.py` - List user groups
- `slack_get_usergroup_members.py` - Get members of user group

### Writing Content
- `slack_post_message.py` - Post message to channel
- `slack_send_dm.py` - Send direct message
- `slack_send_group_dm.py` - Send group DM (2-8 users)
- `slack_reply_to_thread.py` - Reply to thread
- `slack_add_reaction.py` - Add emoji reaction
- `slack_update_message.py` - Update existing message

### Utilities
- `parse_slack_url.py` - Parse Slack URLs to extract channel_id and thread_ts
- `slack_api_client.py` - Shared API client module (imported by all scripts)

**Usage**: All scripts support `--help` for detailed parameter information:
```bash
./scripts/slack_get_channel_history.py --help
```

## Integration with Other Skills

### Jira Integration (`/jira-integration`)
- Create tickets from Slack threads
- Link Slack threads in Jira descriptions
- Update Jira tickets based on Slack discussions
- Query Jira and post updates to Slack

**Example**: Create ticket and link back to Slack
```bash
# 1. Create Jira ticket
python3 /path/to/jira-integration/scripts/jira_create.py \
  --project GS --summary "..." --description-file desc.txt

# 2. Link Jira to Slack thread
python3 /path/to/jira-integration/scripts/jira_link.py GS-12345 \
  --url "https://adobe.slack.com/archives/..." "Slack Discussion"

# 3. Reply to Slack with Jira link
./scripts/slack_reply_to_thread.py --channel-id C123 --thread-ts 1234567890.123456 \
  --text "Created Jira ticket: https://jira.corp.adobe.com/browse/GS-12345"
```

### Confluence Wiki (`/confluence-wiki`)
- Create wiki pages from Slack discussions
- Link wiki pages in Slack for reference
- Post wiki page summaries to Slack channels

### Workflow Orchestration (`/orchestrate`)
- Automate multi-step Slack → Jira → Wiki workflows
- Coordinate responses across multiple channels
- Manage complex approval processes via Slack

## Workflow Decision Tree

```
Slack operation needed
    │
    ├─ Read Slack content?
    │   ├─ Have URL?
    │   │   ├─ Parse URL to extract channel_id, thread_ts
    │   │   └─ Use slack_get_thread_replies or slack_get_channel_history
    │   │
    │   └─ Need to search?
    │       └─ Use slack_search_messages
    │
    ├─ Create Jira from Slack?
    │   ├─ 1. Parse Slack URL
    │   ├─ 2. Fetch thread with slack_get_thread_replies
    │   ├─ 3. Analyze and summarize content
    │   ├─ 4. Format description (Wiki syntax, include Slack link)
    │   ├─ 5. Create Jira with /jira-integration
    │   └─ 6. Reply to Slack with Jira link
    │
    ├─ Post to Slack?
    │   ├─ New message → slack_post_message
    │   ├─ Reply to thread → slack_reply_to_thread
    │   └─ Add reaction → slack_add_reaction
    │
    ├─ Find user/channel?
    │   ├─ Channel → slack_list_channels or slack_get_channel_info
    │   └─ User → slack_lookup_user or slack_search_users
    │
    └─ Complex workflow?
        └─ Use /orchestrate for multi-step operations
```

## Resources

### references/
- `slack_url_parsing.md` - Slack URL format reference and parsing logic
- `workflow_patterns.md` - Common Slack workflow patterns and examples
- `jira_integration_patterns.md` - Patterns for Slack → Jira workflows

### scripts/
- `parse_slack_url.py` - Utility script to parse Slack URLs
- `slack_to_jira.py` - End-to-end script for creating Jira from Slack thread

### assets/
- `jira_description_templates.txt` - Templates for Jira descriptions from Slack content

## Troubleshooting

### "No tokens configured" Error

**Problem**: Scripts cannot find Slack tokens.

**Solution**:
1. Check if tokens are set: `echo $SLACK_BOT_TOKEN`
2. If empty, add to `~/.zshrc` or `~/.bashrc`:
   ```bash
   export SLACK_BOT_TOKEN="xoxb-..."
   export SLACK_USER_TOKEN="xoxp-..."
   ```
3. Reload shell: `source ~/.zshrc`
4. Verify: `echo $SLACK_BOT_TOKEN` (should show token)

### Authentication Errors

**Problem**: `invalid_auth` or token expired errors.

**Solution**:
- Verify tokens at https://api.slack.com/apps
- Check token format: `xoxb-` for bot, `xoxp-` for user
- Regenerate tokens if expired (OAuth & Permissions page)
- Reinstall app to workspace if needed

### Permission Errors

**Problem**: `missing_scope` or permission denied errors.

**Solution**:
- Check bot has all required scopes (see [Detailed Token Setup](#step-2-configure-bot-token-scopes))
- Add missing scopes in app settings
- **Important**: Reinstall app after adding scopes
- For private channels: invite bot with `/invite @your-bot-name`

### Channel Access Issues

**Problem**: `channel_not_found` errors.

**Solution**:
- Verify channel ID format (starts with C, D, or G)
- Bot must be invited to private channels
- Use `parse_slack_url.py` to extract correct channel ID from URL
- Test with a public channel first

### Search Not Working

**Problem**: `search:read` permission error or no results.

**Solution**:
- Search requires **User Token** (`SLACK_USER_TOKEN`)
- Add `search:read` scope to User Token Scopes
- Reinstall app to workspace
- Export user token: `export SLACK_USER_TOKEN="xoxp-..."`

### Thread Replies Empty

**Problem**: `slack_get_thread_replies.py` returns empty or only parent message.

**Solution**:
- Verify `--thread-ts` is correct (timestamp of parent message)
- If URL has `thread_ts=` parameter, use that value
- Some messages may not have replies (check parent message first)

### ImportError: slack_api_client

**Problem**: Scripts cannot import `slack_api_client` module.

**Solution**:
- Run scripts from `skills/slack-integration/scripts/` directory
- Or add to PYTHONPATH: `export PYTHONPATH=/path/to/skills/slack-integration/scripts`

### Rate Limit Errors

**Problem**: `rate_limited` errors from Slack API.

**Solution**:
- Scripts automatically retry with exponential backoff
- If persists, reduce request frequency
- Check Slack API tier limits at https://api.slack.com/docs/rate-limits

### URL Parsing Failures

**Problem**: Cannot extract channel_id or timestamp from URL.

**Solution**:
- Test with: `./scripts/parse_slack_url.py "your-url"`
- Verify URL format matches expected patterns:
  - `https://adobe.slack.com/archives/C123/p1234567890123456`
  - `https://adobe.slack.com/archives/C123`
- Check for URL encoding issues

## Technical Details

### Architecture

This skill uses **direct Slack API access** via Python scripts:

- **No MCP server required** - Scripts call Slack API directly using `curl`
- **Zero external dependencies** - Uses Python stdlib + curl only
- **Token fallback** - Automatically retries with alternate token on auth errors
- **Rate limiting** - Exponential backoff for rate limit handling
- **Error classification** - 6 error types with helpful messages
- **JSON output** - Structured responses for easy parsing

### File Structure

```
slack-integration/
├── SKILL.md                              # This file
├── scripts/
│   ├── slack_api_client.py               # Shared API client (core module)
│   ├── parse_slack_url.py                # URL parsing utility
│   │
│   ├── slack_list_channels.py            # List public channels
│   ├── slack_get_channel_info.py         # Get channel details
│   ├── slack_get_channel_history.py      # Read channel messages
│   ├── slack_get_thread_replies.py       # Read thread replies
│   │
│   ├── slack_post_message.py             # Post message to channel
│   ├── slack_reply_to_thread.py          # Reply to thread
│   ├── slack_send_dm.py                  # Send direct message
│   ├── slack_send_group_dm.py            # Send group DM
│   ├── slack_update_message.py           # Update existing message
│   ├── slack_add_reaction.py             # Add emoji reaction
│   ├── slack_search_messages.py          # Search messages (requires user token)
│   │
│   ├── slack_get_users.py                # List all users
│   ├── slack_get_user_profile.py         # Get user details
│   ├── slack_get_user_by_email.py        # Get user by email
│   ├── slack_search_users.py             # Search users
│   ├── slack_lookup_user.py              # Lookup user (auto-detects type)
│   │
│   ├── slack_list_usergroups.py          # List user groups
│   ├── slack_get_usergroup_members.py    # Get usergroup members
│   │
│   └── test_slack_api_client.py          # Test suite
│
├── references/
│   └── slack_url_parsing.md              # URL format reference
└── assets/
    └── jira_description_templates.txt    # Jira description templates
```

### Core Module: slack_api_client.py

All scripts import the `slack_api_client` module which provides:

**Functions**:
- `call_slack_api()` - Make API calls with error handling and retry logic
- `get_token()` - Retrieve appropriate token (bot/user) with fallback
- `parse_error()` - Classify Slack API errors into actionable categories

**Error Handling**:
- Automatic retry with exponential backoff for rate limits
- Token fallback (try bot token, then user token)
- Clear error messages with resolution guidance
- Graceful handling of missing tokens

**API Methods Supported**:
- All standard Slack Web API methods via `curl`
- Automatic JSON parsing of responses
- Support for pagination cursors

## Security Notes

**Token Protection**:
- Never commit Slack tokens to version control
- Store tokens in environment variables or secure secret management
- Use bot tokens with minimal required scopes
- Rotate tokens periodically

**Data Privacy**:
- Slack content may contain sensitive information
- Follow Adobe's data handling policies when extracting content
- Be mindful when posting automated messages to channels
- Consider privacy when creating public Jira tickets from private Slack channels

**Access Control**:
- Bot must be invited to private channels to read messages
- User token has access to all channels the user can see
- Respect channel membership and privacy settings
- Don't expose private channel content in public Jira tickets without review

## Examples

### Example 1: Simple Thread to Jira

```
User: "Create a Jira ticket from this thread: https://adobe.slack.com/archives/C12345678/p1234567890123456"

Agent:
1. Parse URL: channel_id=C12345678, thread_ts=1234567890.123456
2. Fetch thread: slack_get_thread_replies({"channel_id": "C12345678", "thread_ts": "1234567890.123456"})
3. Summarize: "Discussion about adding dark mode to dashboard"
4. Create Jira: GS-12345 with description including Slack link
5. Reply to thread: "Created GS-12345: https://jira.corp.adobe.com/browse/GS-12345"
```

### Example 2: Search and Triage

```
User: "Find all bug reports in #engineering from today and create Jira tickets"

Agent:
1. Search messages: slack_search_messages({"query": "bug", "channel_names": ["engineering"]})
2. Filter by today's date
3. For each bug report:
   - Parse details from message
   - Check if already has Jira link (skip if exists)
   - Create Jira bug ticket
   - Reply with ticket link
   - Add ✅ reaction
```

### Example 3: User Lookup

```
User: "Who is jane.doe@adobe.com in Slack?"

Agent:
1. Look up user: slack_lookup_user({"identifier": "jane.doe@adobe.com"})
2. Display profile: name, username, title, team, timezone
```

### Example 4: Channel Summary

```
User: "Summarize #team-updates from the last week"

Agent:
1. Get channel history: slack_get_channel_history({"channel_id": "C12345678", "limit": 200})
2. Filter messages from last 7 days
3. Categorize by topic
4. Generate summary with key points
5. Optionally post summary back to channel
```

## Best Practices

1. **Always parse URLs carefully** - Extract channel_id and thread_ts correctly
2. **Include Slack links in Jira** - Maintain traceability between systems
3. **Summarize, don't copy** - Extract key points, don't paste entire threads
4. **Reply back to Slack** - Close the loop by posting Jira links to original thread
5. **Follow Jira description practices** - Use Wiki syntax, ELI5 summaries, clear acceptance criteria
6. **Respect privacy** - Be careful with private channel content
7. **Use appropriate token** - Bot token for automation, user token when acting as user
8. **Handle errors gracefully** - Check for empty threads, missing channels, auth errors
9. **Batch operations** - When processing multiple messages, do it efficiently
10. **Add reactions** - Use emoji reactions to mark processed messages (✅, 📝, 🎫)

## Organization-Wide Usage

This skill is designed for org-wide use at Adobe. Any team member can:
- Create Jira tickets from Slack discussions
- Search Slack for relevant information
- Post automated updates to channels
- Integrate Slack with Jira workflows

**For admins**: Ensure team members have access to:
- Slack app tokens (shared bot token or individual user tokens) configured as environment variables
- Jira access for ticket creation
- This skill documentation
- Python 3.7+ (already available on macOS)

**For users**: Simply provide Slack URLs and describe what you want to do. The skill handles the technical details through Python scripts.
