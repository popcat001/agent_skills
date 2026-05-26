#!/usr/bin/env python3
"""
Get Slack users

Get a list of all users in the workspace with their basic profile information.
"""

import sys
import json
import argparse
import time
from slack_api_client import SlackAPIClient, SlackError, format_error_output, format_success_output


def main():
    parser = argparse.ArgumentParser(description='Get list of users in Slack workspace')
    parser.add_argument('--limit', type=int, default=100,
                       help='Maximum number of users to return (default: 100, max: 200)')
    parser.add_argument('--cursor', type=str,
                       help='Pagination cursor for next page of results')

    args = parser.parse_args()

    params = {
        'limit': min(args.limit, 200)
    }

    if args.cursor:
        params['cursor'] = args.cursor

    start_time = time.time()
    try:
        client = SlackAPIClient()
        response = client.request('users.list', params)

        execution_time = int((time.time() - start_time) * 1000)
        output = format_success_output(response, execution_time)
        print(json.dumps(output, indent=2))
        sys.exit(0)

    except SlackError as e:
        error_output = format_error_output(e, 'users.list', params)
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        error_output = {
            'ok': False,
            'error_type': 'UnexpectedError',
            'message': str(e),
            'method': 'users.list'
        }
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(3)


if __name__ == '__main__':
    main()
