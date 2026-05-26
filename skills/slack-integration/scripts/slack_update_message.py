#!/usr/bin/env python3
"""
Update Slack message

Update an existing message in a channel or DM.
"""

import sys
import json
import argparse
import time
from slack_api_client import SlackAPIClient, SlackError, format_error_output, format_success_output


def main():
    parser = argparse.ArgumentParser(description='Update an existing Slack message')
    parser.add_argument('--channel-id', type=str, required=True,
                       help='The ID of the channel containing the message')
    parser.add_argument('--timestamp', type=str, required=True,
                       help='The timestamp of the message to update (e.g., 1234567890.123456)')
    parser.add_argument('--text', type=str, required=True,
                       help='The updated message text')
    parser.add_argument('--use-user-token', action='store_true',
                       help='Update as your Slack user (default: use bot token)')
    parser.add_argument('--json-input', action='store_true',
                       help='Read JSON input from stdin (for blocks/attachments)')

    args = parser.parse_args()

    # Build parameters
    if args.json_input:
        try:
            params = json.load(sys.stdin)
            params['channel'] = args.channel_id
            params['ts'] = args.timestamp
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
            'ts': args.timestamp,
            'text': args.text
        }

    start_time = time.time()
    try:
        client = SlackAPIClient()
        response = client.request('chat.update', params, use_user_token=args.use_user_token)

        execution_time = int((time.time() - start_time) * 1000)
        output = format_success_output(response, execution_time)
        print(json.dumps(output, indent=2))
        sys.exit(0)

    except SlackError as e:
        error_output = format_error_output(e, 'chat.update', params)
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        error_output = {
            'ok': False,
            'error_type': 'UnexpectedError',
            'message': str(e),
            'method': 'chat.update'
        }
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(3)


if __name__ == '__main__':
    main()
