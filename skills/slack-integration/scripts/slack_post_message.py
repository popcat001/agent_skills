#!/usr/bin/env python3
"""
Post message to Slack channel

Post a new message to a Slack channel.
"""

import sys
import json
import argparse
import time
from slack_api_client import SlackAPIClient, SlackError, format_error_output, format_success_output


def main():
    parser = argparse.ArgumentParser(description='Post a message to a Slack channel')
    parser.add_argument('--channel-id', type=str, required=True,
                       help='The ID of the channel (e.g., C12345678)')
    parser.add_argument('--text', type=str, required=True,
                       help='The message text to post')
    parser.add_argument('--thread-ts', type=str,
                       help='Thread timestamp to reply to (makes this a thread reply)')
    parser.add_argument('--use-user-token', action='store_true',
                       help='Send as your Slack user (default: use bot token)')
    parser.add_argument('--json-input', action='store_true',
                       help='Read JSON input from stdin (for blocks/attachments)')

    args = parser.parse_args()

    # Build parameters
    if args.json_input:
        # Read JSON from stdin for complex parameters
        try:
            params = json.load(sys.stdin)
        except json.JSONDecodeError as e:
            print(json.dumps({
                'ok': False,
                'error_type': 'ValidationError',
                'message': f'Invalid JSON input: {e}'
            }, indent=2), file=sys.stderr)
            sys.exit(4)
    else:
        params = {
            'channel': args.channel_id,
            'text': args.text
        }

        if args.thread_ts:
            params['thread_ts'] = args.thread_ts

    start_time = time.time()
    try:
        client = SlackAPIClient()
        response = client.request('chat.postMessage', params, use_user_token=args.use_user_token)

        execution_time = int((time.time() - start_time) * 1000)
        output = format_success_output(response, execution_time)
        print(json.dumps(output, indent=2))
        sys.exit(0)

    except SlackError as e:
        error_output = format_error_output(e, 'chat.postMessage', params)
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        error_output = {
            'ok': False,
            'error_type': 'UnexpectedError',
            'message': str(e),
            'method': 'chat.postMessage'
        }
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(3)


if __name__ == '__main__':
    main()
