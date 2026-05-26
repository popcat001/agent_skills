#!/usr/bin/env python3
"""
Add reaction to Slack message

Add an emoji reaction to a message.
"""

import sys
import json
import argparse
import time
from slack_api_client import SlackAPIClient, SlackError, format_error_output, format_success_output


def main():
    parser = argparse.ArgumentParser(description='Add emoji reaction to a Slack message')
    parser.add_argument('--channel-id', type=str, required=True,
                       help='The ID of the channel containing the message')
    parser.add_argument('--timestamp', type=str, required=True,
                       help='The timestamp of the message to react to (e.g., 1234567890.123456)')
    parser.add_argument('--reaction', type=str, required=True,
                       help='The name of the emoji reaction without colons (e.g., thumbsup, white_check_mark)')
    parser.add_argument('--use-user-token', action='store_true',
                       help='React as your Slack user (default: use bot token)')

    args = parser.parse_args()

    # Remove colons if user included them
    reaction_name = args.reaction.strip(':')

    params = {
        'channel': args.channel_id,
        'timestamp': args.timestamp,
        'name': reaction_name
    }

    start_time = time.time()
    try:
        client = SlackAPIClient()
        response = client.request('reactions.add', params, use_user_token=args.use_user_token)

        execution_time = int((time.time() - start_time) * 1000)
        output = format_success_output(response, execution_time)
        print(json.dumps(output, indent=2))
        sys.exit(0)

    except SlackError as e:
        error_output = format_error_output(e, 'reactions.add', params)
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        error_output = {
            'ok': False,
            'error_type': 'UnexpectedError',
            'message': str(e),
            'method': 'reactions.add'
        }
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(3)


if __name__ == '__main__':
    main()
