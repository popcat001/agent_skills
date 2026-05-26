#!/usr/bin/env python3
"""
Parse Slack URLs to extract channel_id, timestamp, and thread_ts.

Usage:
    python3 parse_slack_url.py <slack_url>

Examples:
    python3 parse_slack_url.py "https://adobe.slack.com/archives/C12345678/p1234567890123456"
    python3 parse_slack_url.py "https://adobe.slack.com/archives/C12345678/p1234567890123456?thread_ts=1234567890.123456"
"""

import re
import sys
import json
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


def main():
    """Main entry point for CLI usage."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    url = sys.argv[1]

    # Parse the URL
    parsed = parse_slack_url(url)

    if not parsed:
        print(f"Error: Could not parse Slack URL: {url}", file=sys.stderr)
        sys.exit(1)

    # Validate components
    if 'channel_id' in parsed and not validate_channel_id(parsed['channel_id']):
        print(f"Warning: Invalid channel ID format: {parsed['channel_id']}", file=sys.stderr)

    if 'timestamp' in parsed and not validate_timestamp(parsed['timestamp']):
        print(f"Warning: Invalid timestamp format: {parsed['timestamp']}", file=sys.stderr)

    if 'thread_ts' in parsed and not validate_timestamp(parsed['thread_ts']):
        print(f"Warning: Invalid thread_ts format: {parsed['thread_ts']}", file=sys.stderr)

    # Output results
    print(json.dumps(parsed, indent=2))

    # Print usage hints
    print("\n# Usage with MCP tools:", file=sys.stderr)
    if parsed.get('url_type') == 'channel':
        print(f"# Get channel info:", file=sys.stderr)
        print(f'#   slack_get_channel_info({{\"channel_id\": \"{parsed["channel_id"]}\"}})', file=sys.stderr)
        print(f"# Get channel history:", file=sys.stderr)
        print(f'#   slack_get_channel_history({{\"channel_id\": \"{parsed["channel_id"]}\", \"limit\": 50}})', file=sys.stderr)
    elif 'thread_ts' in parsed:
        print(f"# Get thread replies:", file=sys.stderr)
        print(f'#   slack_get_thread_replies({{\"channel_id\": \"{parsed["channel_id"]}\", \"thread_ts\": \"{parsed["thread_ts"]}\"}})', file=sys.stderr)


if __name__ == '__main__':
    main()
