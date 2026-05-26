#!/usr/bin/env python3
"""
List Slack channels

Lists public channels in the workspace with pagination support.
"""

import sys
import json
import argparse
import time
from slack_api_client import SlackAPIClient, SlackError, format_error_output, format_success_output


def main():
    parser = argparse.ArgumentParser(description='List public channels in Slack workspace')
    parser.add_argument('--limit', type=int, default=100,
                       help='Maximum number of channels to return (default: 100, max: 200)')
    parser.add_argument('--cursor', type=str,
                       help='Pagination cursor for next page of results')
    parser.add_argument('--exclude-archived', action='store_true', default=True,
                       help='Exclude archived channels (default: True)')
    parser.add_argument('--include-archived', action='store_false', dest='exclude_archived',
                       help='Include archived channels')
    parser.add_argument('--types', type=str, default='public_channel',
                       help='Comma-separated channel types: public_channel,private_channel,mpim,im (default: public_channel)')

    args = parser.parse_args()

    # Build parameters
    params = {
        'limit': min(args.limit, 200),
        'exclude_archived': args.exclude_archived,
        'types': args.types,
    }

    if args.cursor:
        params['cursor'] = args.cursor

    # Execute request
    start_time = time.time()
    try:
        client = SlackAPIClient()
        response = client.request('conversations.list', params)

        execution_time = int((time.time() - start_time) * 1000)
        output = format_success_output(response, execution_time)
        print(json.dumps(output, indent=2))
        sys.exit(0)

    except SlackError as e:
        error_output = format_error_output(e, 'conversations.list', params)
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        error_output = {
            'ok': False,
            'error_type': 'UnexpectedError',
            'message': str(e),
            'method': 'conversations.list'
        }
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(3)


if __name__ == '__main__':
    main()
