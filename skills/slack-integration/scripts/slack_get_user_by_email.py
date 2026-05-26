#!/usr/bin/env python3
"""
Get Slack user by email

Get user information by email address.
"""

import sys
import json
import argparse
import time
from slack_api_client import SlackAPIClient, SlackError, format_error_output, format_success_output


def main():
    parser = argparse.ArgumentParser(description='Get Slack user information by email address')
    parser.add_argument('--email', type=str, required=True,
                       help='The email address of the user to find')

    args = parser.parse_args()

    params = {
        'email': args.email
    }

    start_time = time.time()
    try:
        client = SlackAPIClient()
        response = client.request('users.lookupByEmail', params)

        execution_time = int((time.time() - start_time) * 1000)
        output = format_success_output(response, execution_time)
        print(json.dumps(output, indent=2))
        sys.exit(0)

    except SlackError as e:
        error_output = format_error_output(e, 'users.lookupByEmail', params)
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        error_output = {
            'ok': False,
            'error_type': 'UnexpectedError',
            'message': str(e),
            'method': 'users.lookupByEmail'
        }
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(3)


if __name__ == '__main__':
    main()
