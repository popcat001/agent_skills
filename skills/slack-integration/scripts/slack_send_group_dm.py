#!/usr/bin/env python3
"""
Send group direct message

Send a message to a group direct message with multiple users (2-8 users).
"""

import sys
import json
import argparse
import time
from slack_api_client import SlackAPIClient, SlackError, format_error_output, format_success_output


def main():
    parser = argparse.ArgumentParser(description='Send a message to a group DM')
    parser.add_argument('--user-ids', type=str, required=True,
                       help='Comma-separated list of user IDs (2-8 users, e.g., U123,U456,U789)')
    parser.add_argument('--text', type=str, required=True,
                       help='The message text to send')
    parser.add_argument('--json-input', action='store_true',
                       help='Read JSON input from stdin (for blocks/attachments)')

    args = parser.parse_args()

    # Parse user IDs
    user_ids = [uid.strip() for uid in args.user_ids.split(',')]

    if len(user_ids) < 2 or len(user_ids) > 8:
        print(json.dumps({
            'ok': False,
            'error_type': 'ValidationError',
            'message': 'Group DM requires 2-8 users'
        }, indent=2), file=sys.stderr)
        sys.exit(4)

    start_time = time.time()
    try:
        client = SlackAPIClient()

        # Open a multi-party DM channel
        open_params = {'users': ','.join(user_ids)}
        dm_response = client.request('conversations.open', open_params, use_user_token=True)

        if not dm_response.get('ok') or 'channel' not in dm_response:
            raise SlackError('Failed to open group DM channel')

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
        response = client.request('chat.postMessage', params)

        execution_time = int((time.time() - start_time) * 1000)
        output = format_success_output(response, execution_time)
        print(json.dumps(output, indent=2))
        sys.exit(0)

    except SlackError as e:
        error_output = format_error_output(e, 'chat.postMessage (Group DM)', {'user_ids': user_ids})
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        error_output = {
            'ok': False,
            'error_type': 'UnexpectedError',
            'message': str(e),
            'method': 'chat.postMessage (Group DM)'
        }
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(3)


if __name__ == '__main__':
    main()
