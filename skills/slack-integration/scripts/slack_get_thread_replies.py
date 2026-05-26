#!/usr/bin/env python3
"""
Get Slack thread replies

Get all replies in a message thread.
"""

import sys
import json
import argparse
import time
from slack_api_client import SlackAPIClient, SlackError, format_error_output, format_success_output


def main():
    parser = argparse.ArgumentParser(description='Get all replies in a Slack thread')
    parser.add_argument('--channel-id', type=str, required=True,
                       help='The ID of the channel containing the thread')
    parser.add_argument('--thread-ts', type=str, required=True,
                       help='The timestamp of the parent message (e.g., 1234567890.123456)')
    parser.add_argument('--cursor', type=str,
                       help='Pagination cursor for next page of results')
    parser.add_argument('--limit', type=int,
                       help='Maximum number of replies to return')

    args = parser.parse_args()

    params = {
        'channel': args.channel_id,
        'ts': args.thread_ts
    }

    if args.cursor:
        params['cursor'] = args.cursor
    if args.limit:
        params['limit'] = args.limit

    start_time = time.time()
    try:
        client = SlackAPIClient()
        response = client.request('conversations.replies', params)

        execution_time = int((time.time() - start_time) * 1000)
        output = format_success_output(response, execution_time)
        print(json.dumps(output, indent=2))
        sys.exit(0)

    except SlackError as e:
        error_output = format_error_output(e, 'conversations.replies', params)
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        error_output = {
            'ok': False,
            'error_type': 'UnexpectedError',
            'message': str(e),
            'method': 'conversations.replies'
        }
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(3)


if __name__ == '__main__':
    main()
