#!/usr/bin/env python3
"""
Get Slack user group members

Get members of a specific user group by its ID.
"""

import sys
import json
import argparse
import time
from slack_api_client import SlackAPIClient, SlackError, format_error_output, format_success_output


def main():
    parser = argparse.ArgumentParser(description='Get members of a Slack user group')
    parser.add_argument('--usergroup-id', type=str, required=True,
                       help='The ID of the user group (e.g., S12345678)')

    args = parser.parse_args()

    params = {
        'usergroup': args.usergroup_id
    }

    start_time = time.time()
    try:
        client = SlackAPIClient()
        response = client.request('usergroups.users.list', params)

        execution_time = int((time.time() - start_time) * 1000)
        output = format_success_output(response, execution_time)
        print(json.dumps(output, indent=2))
        sys.exit(0)

    except SlackError as e:
        error_output = format_error_output(e, 'usergroups.users.list', params)
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        error_output = {
            'ok': False,
            'error_type': 'UnexpectedError',
            'message': str(e),
            'method': 'usergroups.users.list'
        }
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(3)


if __name__ == '__main__':
    main()
