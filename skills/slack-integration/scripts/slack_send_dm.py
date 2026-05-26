#!/usr/bin/env python3
"""
Send direct message to Slack user

Send a direct message to a Slack user.
"""

import sys
import json
import argparse
import time
from slack_api_client import SlackAPIClient, SlackError, format_error_output, format_success_output


def main():
    parser = argparse.ArgumentParser(description='Send a direct message to a Slack user')
    parser.add_argument('--user-id', type=str, required=True,
                       help='The ID of the user to send the message to (e.g., U12345678)')
    parser.add_argument('--text', type=str, required=True,
                       help='The message text to send')
    parser.add_argument('--use-user-token', action='store_true',
                       help='Send as your Slack user (default: use bot token)')
    parser.add_argument('--json-input', action='store_true',
                       help='Read JSON input from stdin (for blocks/attachments)')

    args = parser.parse_args()

    start_time = time.time()
    try:
        client = SlackAPIClient()

        # First, open a DM channel with the user
        open_params = {'users': args.user_id}
        dm_response = client.request('conversations.open', open_params, use_user_token=True)

        if not dm_response.get('ok') or 'channel' not in dm_response:
            raise SlackError('Failed to open DM channel')

        channel_id = dm_response['channel']['id']

        # Build message parameters
        if args.json_input:
            try:
                params = json.load(sys.stdin)
                params['channel'] = channel_id
            except json.JSONDecodeError as e:
                print(json.dumps({
                    'ok': False,
                    'error_type': 'ValidationError',
                    'message': f'Invalid JSON input: {e}'
                }, indent=2), file=sys.stderr)
                sys.exit(4)
        else:
            params = {
                'channel': channel_id,
                'text': args.text
            }

        # Send the message
        response = client.request('chat.postMessage', params, use_user_token=args.use_user_token)

        execution_time = int((time.time() - start_time) * 1000)
        output = format_success_output(response, execution_time)
        print(json.dumps(output, indent=2))
        sys.exit(0)

    except SlackError as e:
        error_output = format_error_output(e, 'chat.postMessage (DM)', {'user_id': args.user_id})
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        error_output = {
            'ok': False,
            'error_type': 'UnexpectedError',
            'message': str(e),
            'method': 'chat.postMessage (DM)'
        }
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(3)


if __name__ == '__main__':
    main()
