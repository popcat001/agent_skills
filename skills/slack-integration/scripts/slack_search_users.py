#!/usr/bin/env python3
"""
Search Slack users

Search for users by name, display name, or username.
"""

import sys
import json
import argparse
import time
from slack_api_client import SlackAPIClient, SlackError, format_error_output, format_success_output


def main():
    parser = argparse.ArgumentParser(description='Search for Slack users by name, display name, or username')
    parser.add_argument('--query', type=str, required=True,
                       help='Search query to find users')
    parser.add_argument('--limit', type=int, default=10,
                       help='Maximum number of users to return (default: 10, max: 50)')

    args = parser.parse_args()

    start_time = time.time()
    try:
        client = SlackAPIClient()

        # Get all users (Slack doesn't have direct search API)
        response = client.request('users.list', {'limit': 1000})

        if not response.get('ok') or 'members' not in response:
            raise SlackError('Failed to retrieve users')

        # Filter users based on query
        query = args.query.lower()
        limit = min(args.limit, 50)

        filtered_users = []
        for user in response['members']:
            if user.get('deleted') or user.get('is_bot'):
                continue

            name = (user.get('name') or '').lower()
            real_name = (user.get('real_name') or '').lower()
            display_name = (user.get('profile', {}).get('display_name') or '').lower()
            email = (user.get('profile', {}).get('email') or '').lower()

            if (query in name or query in real_name or
                query in display_name or query in email):
                filtered_users.append(user)

            if len(filtered_users) >= limit:
                break

        execution_time = int((time.time() - start_time) * 1000)
        output = format_success_output({
            'ok': True,
            'users': filtered_users,
            'query': args.query
        }, execution_time)
        print(json.dumps(output, indent=2))
        sys.exit(0)

    except SlackError as e:
        error_output = format_error_output(e, 'users.list (search)', {'query': args.query})
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        error_output = {
            'ok': False,
            'error_type': 'UnexpectedError',
            'message': str(e),
            'method': 'users.list (search)'
        }
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(3)


if __name__ == '__main__':
    main()
