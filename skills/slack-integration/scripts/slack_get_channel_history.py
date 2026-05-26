#!/usr/bin/env python3
"""
Get Slack channel message history

Get recent messages from a channel with pagination support.
"""

import sys
import json
import argparse
import time
from slack_api_client import SlackAPIClient, SlackError, format_error_output, format_success_output


def main():
    parser = argparse.ArgumentParser(description='Get recent messages from a Slack channel')
    parser.add_argument('--channel-id', type=str, required=True,
                       help='The ID of the channel (e.g., C12345678)')
    parser.add_argument('--limit', type=int, default=10,
                       help='Number of messages to retrieve (default: 10)')
    parser.add_argument('--cursor', type=str,
                       help='Pagination cursor for next page of results')
    parser.add_argument('--oldest', type=str,
                       help='Only messages after this timestamp (e.g., 1234567890.123456)')
    parser.add_argument('--latest', type=str,
                       help='Only messages before this timestamp (e.g., 1234567890.123456)')

    args = parser.parse_args()

    params = {
        'channel': args.channel_id,
        'limit': args.limit
    }

    if args.cursor:
        params['cursor'] = args.cursor
    if args.oldest:
        params['oldest'] = args.oldest
    if args.latest:
        params['latest'] = args.latest

    start_time = time.time()
    try:
        client = SlackAPIClient()
        response = client.request('conversations.history', params)

        execution_time = int((time.time() - start_time) * 1000)
        output = format_success_output(response, execution_time)
        print(json.dumps(output, indent=2))
        sys.exit(0)

    except SlackError as e:
        error_output = format_error_output(e, 'conversations.history', params)
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        error_output = {
            'ok': False,
            'error_type': 'UnexpectedError',
            'message': str(e),
            'method': 'conversations.history'
        }
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(3)


if __name__ == '__main__':
    main()
