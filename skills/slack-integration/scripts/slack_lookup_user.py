#!/usr/bin/env python3
"""
Lookup Slack user

Lookup a user by email, username, or user ID with auto-detection.
"""

import sys
import json
import argparse
import time
from slack_api_client import SlackAPIClient, SlackError, format_error_output, format_success_output


def main():
    parser = argparse.ArgumentParser(description='Lookup a Slack user by email, username, or user ID')
    parser.add_argument('--identifier', type=str, required=True,
                       help='Email address, username, or user ID to lookup')
    parser.add_argument('--type', type=str, choices=['email', 'username', 'user_id', 'auto'],
                       default='auto',
                       help='Type of identifier (default: auto-detect)')

    args = parser.parse_args()

    identifier = args.identifier
    lookup_type = args.type

    # Auto-detect type if not specified
    if lookup_type == 'auto':
        if '@' in identifier:
            lookup_type = 'email'
        elif identifier.startswith('U'):
            lookup_type = 'user_id'
        else:
            lookup_type = 'username'

    start_time = time.time()
    try:
        client = SlackAPIClient()

        if lookup_type == 'email':
            # Use lookupByEmail API
            params = {'email': identifier}
            response = client.request('users.lookupByEmail', params)

        elif lookup_type == 'user_id':
            # Use users.info API
            params = {'user': identifier}
            response = client.request('users.info', params)

        else:  # username
            # Search all users for matching username
            response = client.request('users.list', {'limit': 1000})

            if not response.get('ok') or 'members' not in response:
                raise SlackError('Failed to retrieve users')

            # Find user by username
            user_found = None
            for user in response['members']:
                if user.get('name') == identifier:
                    user_found = user
                    break

            if not user_found:
                raise SlackError(f'User not found with username: {identifier}')

            response = {
                'ok': True,
                'user': user_found
            }

        execution_time = int((time.time() - start_time) * 1000)
        output = format_success_output(response, execution_time)
        print(json.dumps(output, indent=2))
        sys.exit(0)

    except SlackError as e:
        error_output = format_error_output(e, 'user lookup', {'identifier': identifier, 'type': lookup_type})
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        error_output = {
            'ok': False,
            'error_type': 'UnexpectedError',
            'message': str(e),
            'method': 'user lookup'
        }
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(3)


if __name__ == '__main__':
    main()
