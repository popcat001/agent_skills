#!/usr/bin/env python3
"""
List Slack user groups

List all user groups (handle groups) in the workspace.
"""

import sys
import json
import argparse
import time
from slack_api_client import SlackAPIClient, SlackError, format_error_output, format_success_output


def main():
    parser = argparse.ArgumentParser(description='List all user groups in Slack workspace')
    parser.add_argument('--include-disabled', action='store_true',
                       help='Include disabled user groups (default: only active groups)')
    parser.add_argument('--include-count', action='store_true',
                       help='Include member count in results')
    parser.add_argument('--include-users', action='store_true',
                       help='Include user IDs of group members')

    args = parser.parse_args()

    params = {
        'include_disabled': args.include_disabled,
        'include_count': args.include_count,
        'include_users': args.include_users
    }

    start_time = time.time()
    try:
        client = SlackAPIClient()
        response = client.request('usergroups.list', params)

        execution_time = int((time.time() - start_time) * 1000)
        output = format_success_output(response, execution_time)
        print(json.dumps(output, indent=2))
        sys.exit(0)

    except SlackError as e:
        error_output = format_error_output(e, 'usergroups.list', params)
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        error_output = {
            'ok': False,
            'error_type': 'UnexpectedError',
            'message': str(e),
            'method': 'usergroups.list'
        }
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(3)


if __name__ == '__main__':
    main()
