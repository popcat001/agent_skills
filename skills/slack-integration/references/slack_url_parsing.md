# Slack URL Parsing Reference

## Overview

Slack URLs contain encoded information about channels, messages, and threads. This guide explains how to parse these URLs to extract the identifiers needed for MCP tool calls.

## URL Formats

### 1. Channel Message URL

**Format**: `https://adobe.slack.com/archives/{CHANNEL_ID}/p{TIMESTAMP}`

**Example**: `https://adobe.slack.com/archives/C12345678/p1234567890123456`

**Components**:
- `C12345678` - Channel ID (starts with C for public channels)
- `p1234567890123456` - Encoded timestamp (16 digits)

**Conversion**:
- Timestamp format: `p{10 digits}{6 digits}` → `{10 digits}.{6 digits}`
- Example: `p1234567890123456` → `1234567890.123456`

### 2. Thread URL (with thread_ts parameter)

**Format**: `https://adobe.slack.com/archives/{CHANNEL_ID}/p{TIMESTAMP}?thread_ts={THREAD_TS}`

**Example**: `https://adobe.slack.com/archives/C12345678/p1234567890123456?thread_ts=1234567890.123456`

**Components**:
- `C12345678` - Channel ID
- `p1234567890123456` - Reply message timestamp (converted to 1234567890.123456)
- `thread_ts=1234567890.123456` - Parent message timestamp (already in correct format)

**Important**: When `thread_ts` parameter is present, it represents the parent message. The `p{TIMESTAMP}` part is a specific reply in the thread.

### 3. Channel URL

**Format**: `https://adobe.slack.com/archives/{CHANNEL_ID}`

**Example**: `https://adobe.slack.com/archives/C12345678`

**Components**:
- `C12345678` - Channel ID only

### 4. Deep Link Format

**Format**: `slack://channel?team={TEAM_ID}&id={CHANNEL_ID}`

**Example**: `slack://channel?team=T12345678&id=C12345678`

**Components**:
- `T12345678` - Team/Workspace ID
- `C12345678` - Channel ID

## Channel ID Prefixes

Different types of Slack conversations have different ID prefixes:

| Prefix | Type | Description |
|--------|------|-------------|
| `C` | Public Channel | Open channels anyone can join |
| `D` | Direct Message | 1-on-1 DM |
| `G` | Private Channel/Group DM | Private channels or multi-person DMs |

**Examples**:
- `C12345678` - Public channel like #engineering
- `D12345678` - Direct message with one person
- `G12345678` - Private channel or group DM

## Timestamp Format

Slack timestamps are Unix timestamps with microsecond precision:

**Format**: `{unix_seconds}.{microseconds}`

**Example**: `1234567890.123456`
- Unix seconds: `1234567890` (10 digits)
- Microseconds: `123456` (6 digits)

**URL Encoding**: Timestamps in URLs are encoded by removing the decimal point and prepending `p`:
- Timestamp: `1234567890.123456`
- URL format: `p1234567890123456`

## Parsing Logic

### Python Implementation

```python
import re
from typing import Dict, Optional

def parse_slack_url(url: str) -> Dict[str, str]:
    """
    Parse Slack URL to extract channel_id, timestamp, and thread_ts.

    Args:
        url: Slack URL in various formats

    Returns:
        Dictionary with parsed components:
        - channel_id: Channel identifier (C*, D*, or G*)
        - timestamp: Message timestamp (if present)
        - thread_ts: Thread parent timestamp (if present)
        - url_type: Type of URL (channel, message, thread)

    Examples:
        >>> parse_slack_url("https://adobe.slack.com/archives/C123/p1234567890123456")
        {'channel_id': 'C123', 'timestamp': '1234567890.123456',
         'thread_ts': '1234567890.123456', 'url_type': 'message'}

        >>> parse_slack_url("https://adobe.slack.com/archives/C123/p1234567890123456?thread_ts=1234567890.111111")
        {'channel_id': 'C123', 'timestamp': '1234567890.123456',
         'thread_ts': '1234567890.111111', 'url_type': 'thread'}
    """
    result = {}

    # Extract channel ID (C, D, or G prefix followed by alphanumeric)
    channel_match = re.search(r'/archives/([CDG][A-Z0-9]+)', url)
    if channel_match:
        result['channel_id'] = channel_match.group(1)

    # Extract timestamp from p-format (p1234567890123456)
    ts_match = re.search(r'/p(\d{10})(\d{6})', url)
    if ts_match:
        timestamp = f"{ts_match.group(1)}.{ts_match.group(2)}"
        result['timestamp'] = timestamp
        # If no separate thread_ts param, this message IS the thread parent
        result['thread_ts'] = timestamp

    # Extract thread_ts parameter if present (overrides derived thread_ts)
    thread_param_match = re.search(r'thread_ts=(\d+\.\d+)', url)
    if thread_param_match:
        result['thread_ts'] = thread_param_match.group(1)
        result['url_type'] = 'thread'  # This is a reply in a thread
    elif ts_match:
        result['url_type'] = 'message'  # This is a top-level message
    elif channel_match:
        result['url_type'] = 'channel'  # Just a channel link

    return result


def validate_channel_id(channel_id: str) -> bool:
    """Validate Slack channel ID format."""
    return bool(re.match(r'^[CDG][A-Z0-9]{8,}$', channel_id))


def validate_timestamp(timestamp: str) -> bool:
    """Validate Slack timestamp format."""
    return bool(re.match(r'^\d{10}\.\d{6}$', timestamp))


def format_timestamp_for_url(timestamp: str) -> str:
    """Convert timestamp to URL format."""
    # Remove decimal point and prepend 'p'
    return 'p' + timestamp.replace('.', '')


def format_url_timestamp(url_timestamp: str) -> str:
    """Convert URL timestamp to standard format."""
    # Remove 'p' prefix and add decimal point
    clean_ts = url_timestamp.lstrip('p')
    if len(clean_ts) == 16:
        return f"{clean_ts[:10]}.{clean_ts[10:]}"
    return clean_ts
```

### JavaScript Implementation

```javascript
/**
 * Parse Slack URL to extract components
 * @param {string} url - Slack URL
 * @returns {Object} Parsed components
 */
function parseSlackUrl(url) {
    const result = {};

    // Extract channel ID
    const channelMatch = url.match(/\/archives\/([CDG][A-Z0-9]+)/);
    if (channelMatch) {
        result.channel_id = channelMatch[1];
    }

    // Extract timestamp from p-format
    const tsMatch = url.match(/\/p(\d{10})(\d{6})/);
    if (tsMatch) {
        const timestamp = `${tsMatch[1]}.${tsMatch[2]}`;
        result.timestamp = timestamp;
        result.thread_ts = timestamp;
    }

    // Extract thread_ts parameter if present
    const threadMatch = url.match(/thread_ts=(\d+\.\d+)/);
    if (threadMatch) {
        result.thread_ts = threadMatch[1];
        result.url_type = 'thread';
    } else if (tsMatch) {
        result.url_type = 'message';
    } else if (channelMatch) {
        result.url_type = 'channel';
    }

    return result;
}
```

## Usage Examples

### Example 1: Parse Message URL

```python
url = "https://adobe.slack.com/archives/C12345678/p1234567890123456"
parsed = parse_slack_url(url)

print(parsed)
# Output:
# {
#   'channel_id': 'C12345678',
#   'timestamp': '1234567890.123456',
#   'thread_ts': '1234567890.123456',
#   'url_type': 'message'
# }

# Use with MCP tool
slack_get_thread_replies({
    "channel_id": parsed['channel_id'],
    "thread_ts": parsed['thread_ts']
})
```

### Example 2: Parse Thread Reply URL

```python
url = "https://adobe.slack.com/archives/C12345678/p1234567890999999?thread_ts=1234567890.123456"
parsed = parse_slack_url(url)

print(parsed)
# Output:
# {
#   'channel_id': 'C12345678',
#   'timestamp': '1234567890.999999',  # This specific reply
#   'thread_ts': '1234567890.123456',  # Parent message
#   'url_type': 'thread'
# }

# Fetch the entire thread (all replies to parent)
slack_get_thread_replies({
    "channel_id": parsed['channel_id'],
    "thread_ts": parsed['thread_ts']  # Use parent timestamp
})
```

### Example 3: Parse Channel URL

```python
url = "https://adobe.slack.com/archives/C12345678"
parsed = parse_slack_url(url)

print(parsed)
# Output:
# {
#   'channel_id': 'C12345678',
#   'url_type': 'channel'
# }

# Get channel info
slack_get_channel_info({
    "channel_id": parsed['channel_id']
})

# Or get recent history
slack_get_channel_history({
    "channel_id": parsed['channel_id'],
    "limit": 50
})
```

## Common Pitfalls

### Pitfall 1: Confusing timestamp with thread_ts

**Problem**: Using the wrong timestamp when thread_ts parameter is present.

**Wrong**:
```python
# URL: .../p1234567890999999?thread_ts=1234567890.123456
parsed = parse_slack_url(url)
slack_get_thread_replies({
    "channel_id": parsed['channel_id'],
    "thread_ts": parsed['timestamp']  # WRONG: This is a reply, not the parent
})
```

**Right**:
```python
slack_get_thread_replies({
    "channel_id": parsed['channel_id'],
    "thread_ts": parsed['thread_ts']  # CORRECT: Use the thread_ts field
})
```

### Pitfall 2: Not converting URL timestamp format

**Problem**: Using the p-format timestamp directly without conversion.

**Wrong**:
```python
slack_get_thread_replies({
    "channel_id": "C12345678",
    "thread_ts": "p1234567890123456"  # WRONG: MCP tools expect decimal format
})
```

**Right**:
```python
slack_get_thread_replies({
    "channel_id": "C12345678",
    "thread_ts": "1234567890.123456"  # CORRECT: Decimal format
})
```

### Pitfall 3: Assuming all messages have threads

**Problem**: Calling get_thread_replies on a message without replies.

**Solution**: Check if message has replies before fetching, or handle empty results gracefully.

```python
# Get thread replies (may return only parent message if no replies)
replies = slack_get_thread_replies({
    "channel_id": parsed['channel_id'],
    "thread_ts": parsed['thread_ts']
})

# Check if there are actual replies
if len(replies) > 1:
    print(f"Thread has {len(replies) - 1} replies")
else:
    print("Message has no replies")
```

## Testing Your Parser

### Test Cases

```python
test_urls = [
    # Message URL
    ("https://adobe.slack.com/archives/C12345678/p1234567890123456",
     {'channel_id': 'C12345678', 'timestamp': '1234567890.123456',
      'thread_ts': '1234567890.123456', 'url_type': 'message'}),

    # Thread reply URL
    ("https://adobe.slack.com/archives/C12345678/p1234567890999999?thread_ts=1234567890.123456",
     {'channel_id': 'C12345678', 'timestamp': '1234567890.999999',
      'thread_ts': '1234567890.123456', 'url_type': 'thread'}),

    # Channel URL
    ("https://adobe.slack.com/archives/C12345678",
     {'channel_id': 'C12345678', 'url_type': 'channel'}),

    # DM URL
    ("https://adobe.slack.com/archives/D12345678/p1234567890123456",
     {'channel_id': 'D12345678', 'timestamp': '1234567890.123456',
      'thread_ts': '1234567890.123456', 'url_type': 'message'}),

    # Private channel URL
    ("https://adobe.slack.com/archives/G12345678/p1234567890123456",
     {'channel_id': 'G12345678', 'timestamp': '1234567890.123456',
      'thread_ts': '1234567890.123456', 'url_type': 'message'}),
]

for url, expected in test_urls:
    result = parse_slack_url(url)
    assert result == expected, f"Failed for {url}"
    print(f"✓ {url[:60]}... → {result['channel_id']}")
```

## Quick Reference

**URL Component Extraction**:
- Channel ID: `/archives/([CDG][A-Z0-9]+)` → Direct match
- Timestamp: `/p(\d{10})(\d{6})` → `{group1}.{group2}`
- Thread TS: `thread_ts=(\d+\.\d+)` → Direct match (overrides timestamp)

**MCP Tool Input**:
- `channel_id`: Use extracted channel ID directly
- `thread_ts`: Use thread_ts parameter if present, otherwise use converted timestamp
- `timestamp`: For reactions, use converted timestamp

**Validation**:
- Channel ID must start with C, D, or G
- Timestamp must be 10 digits + dot + 6 digits
- URL must be from adobe.slack.com (or your workspace domain)
