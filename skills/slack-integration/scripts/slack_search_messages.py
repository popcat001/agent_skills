#!/usr/bin/env python3
"""
Search Slack messages

Search for messages in Slack, optionally filtered by channel names.
"""

import sys
import json
import argparse
import time
from slack_api_client import SlackAPIClient, SlackError, format_error_output, format_success_output


def main():
    parser = argparse.ArgumentParser(description='Search for messages in Slack')
    parser.add_argument('--query', type=str, required=True,
                       help='The search query to use for finding messages')
    parser.add_argument('--channel-names', type=str,
                       help='Comma-separated list of channel names to search in (without #)')
    parser.add_argument('--count', type=int, default=20,
                       help='Number of results to return (default: 20, max: 100)')
    parser.add_argument('--page', type=int, default=1,
                       help='Page number for pagination (default: 1)')

    args = parser.parse_args()

    # Build search query
    query = args.query

    # Add channel filter if specified
    if args.channel_names:
        channel_names = [ch.strip() for ch in args.channel_names.split(',')]
        channel_filter = ' '.join([f'in:#{ch}' for ch in channel_names])
        query = f'{args.query} {channel_filter}'

    params = {
        'query': query,
        'count': min(args.count, 100),
        'page': args.page
    }

    start_time = time.time()
    try:
        client = SlackAPIClient()
        # search.messages always requires user token
        response = client.request('search.messages', params, use_user_token=True)

        execution_time = int((time.time() - start_time) * 1000)
        output = format_success_output(response, execution_time)
        print(json.dumps(output, indent=2))
        sys.exit(0)

    except SlackError as e:
        error_output = format_error_output(e, 'search.messages', params)
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        error_output = {
            'ok': False,
            'error_type': 'UnexpectedError',
            'message': str(e),
            'method': 'search.messages'
        }
        print(json.dumps(error_output, indent=2), file=sys.stderr)
        sys.exit(3)


if __name__ == '__main__':
    main()
