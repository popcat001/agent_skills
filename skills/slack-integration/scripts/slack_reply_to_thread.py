#!/usr/bin/env python3
"""
Reply to Slack thread

Reply to a specific message thread in Slack.
"""

import sys
import json
import argparse
import time
from slack_api_client import SlackAPIClient, SlackError, format_error_output, format_success_output


def main():
    parser = argparse.ArgumentParser(description='Reply to a Slack thread')
    parser.add_argument('--channel-id', type=str, required=True,
                       help='The ID of the channel containing the thread')
    parser.add_argument('--thread-ts', type=str, required=True,
                       help='The timestamp of the parent message (e.g., 1234567890.123456)')
    parser.add_argument('--text', type=str, required=True,
                       help='The reply text')
    parser.add_argument('--use-user-token', action='store_true',
                       help='Reply as your Slack user (default: use bot token)')

    args = parser.parse_args()

    params = {
        'channel': args.channel_id,
        'text': args.text,
        'thread_ts': args.thread_ts
    }

    start_time = time.time()
    try:
        client = SlackAPIClient()
        response = client.request('chat.postMessage', params, use_user_token=args.use_user_token)

        execution_time = int((time.time() - start_time) * 1000)
        output = format_success_output(response, execution_time)
        print(json.dumps(output, indent=2))
        sys.exit(0)

    except SlackError as e:
        error_output = format_error_output(e, 'chat.postMessage (thread reply)', params)
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        error_output = {
            'ok': False,
            'error_type': 'UnexpectedError',
            'message': str(e),
            'method': 'chat.postMessage (thread reply)'
        }
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(3)


if __name__ == '__main__':
    main()
