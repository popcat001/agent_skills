#!/usr/bin/env python3
"""
Confluence Wiki Page Retriever

Fetch Confluence wiki pages by URL or page ID.

Usage:
    python3 wiki_get_page.py --url "https://wiki.corp.adobe.com/display/GenStudio/Page+Title"
    python3 wiki_get_page.py --page-id 3647578884
    python3 wiki_get_page.py --url "..." --format json
"""

import os
import sys
import json
import subprocess
from typing import Optional, Dict, Any


def get_wiki_token() -> str:
    """Get WIKI_TOKEN from environment with validation."""
    token = os.environ.get('WIKI_TOKEN')
    if not token:
        print("ERROR: WIKI_TOKEN environment variable not set", file=sys.stderr)
        print("Get token at: https://wiki.corp.adobe.com/plugins/personalaccesstokens/usertokens.action", file=sys.stderr)
        sys.exit(1)
    return token


def validate_token(token: str) -> bool:
    """
    Validate that the WIKI_TOKEN is valid and can authenticate.

    Returns:
        True if token is valid, False otherwise
    """
    cmd = [
        'curl', '-s',
        '-H', f'Authorization: Bearer {token}',
        'https://wiki.corp.adobe.com/rest/api/user/current'
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        return False

    try:
        user_data = json.loads(result.stdout)
        if user_data.get('type') == 'anonymous':
            print("ERROR: WIKI_TOKEN is invalid or expired (anonymous access)", file=sys.stderr)
            print("Get new token at: https://wiki.corp.adobe.com/plugins/personalaccesstokens/usertokens.action", file=sys.stderr)
            return False

        print(f"✓ Authenticated as: {user_data.get('displayName', 'Unknown')}", file=sys.stderr)
        return True
    except json.JSONDecodeError:
        print(f"ERROR: Failed to parse auth response: {result.stdout}", file=sys.stderr)
        return False


def extract_page_id_from_url(url: str, token: str) -> Optional[str]:
    """
    Extract page ID by fetching the HTML page and parsing the meta tag.

    This is more deterministic than searching by title.

    Args:
        url: Full Confluence URL (e.g., https://wiki.corp.adobe.com/display/Space/Page+Title)
        token: Authentication token

    Returns:
        Page ID if found, None otherwise
    """
    print(f"✓ Fetching HTML from URL to extract page ID", file=sys.stderr)

    cmd = [
        'curl', '-s',
        '-H', f'Authorization: Bearer {token}',
        url
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"ERROR: Failed to fetch HTML: {result.stderr}", file=sys.stderr)
        return None

    # Look for meta tag: <meta name="ajs-page-id" content="3647578884">
    import re
    match = re.search(r'<meta\s+name="ajs-page-id"\s+content="(\d+)"', result.stdout)

    if match:
        page_id = match.group(1)
        print(f"✓ Extracted page ID from HTML: {page_id}", file=sys.stderr)
        return page_id

    print(f"ERROR: Could not find page ID in HTML (meta tag not found)", file=sys.stderr)
    return None


def get_page_by_id(page_id: str, token: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a page by its ID.

    Args:
        page_id: Page ID
        token: Authentication token

    Returns:
        Page data as dict, or None on failure
    """
    cmd = [
        'curl', '-s',
        '-H', f'Authorization: Bearer {token}',
        f'https://wiki.corp.adobe.com/rest/api/content/{page_id}?expand=body.storage,version,space'
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"ERROR: Failed to fetch page: {result.stderr}", file=sys.stderr)
        return None

    try:
        page_data = json.loads(result.stdout)

        # Check for error response
        if 'statusCode' in page_data:
            print(f"ERROR: {page_data.get('message', 'Unknown error')}", file=sys.stderr)
            return None

        print(f"✓ Fetched page: '{page_data.get('title')}' (version {page_data.get('version', {}).get('number')})", file=sys.stderr)
        return page_data

    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse page data: {e}", file=sys.stderr)
        print(f"Response: {result.stdout}", file=sys.stderr)
        return None


def format_output(page_data: Dict[str, Any], output_format: str) -> str:
    """
    Format page data for output.

    Args:
        page_data: Page data from API
        output_format: One of 'json', 'html', 'summary'

    Returns:
        Formatted output string
    """
    if output_format == 'json':
        return json.dumps(page_data, indent=2)

    elif output_format == 'html':
        storage = page_data.get('body', {}).get('storage', {})
        return storage.get('value', '')

    elif output_format == 'summary':
        title = page_data.get('title', 'Unknown')
        page_id = page_data.get('id', 'Unknown')
        version = page_data.get('version', {}).get('number', 'Unknown')
        space = page_data.get('space', {}).get('name', 'Unknown')
        webui = page_data.get('_links', {}).get('webui', '')
        url = f"https://wiki.corp.adobe.com{webui}" if webui else "Unknown"

        output = []
        output.append("=" * 80)
        output.append(f"Title: {title}")
        output.append(f"Page ID: {page_id}")
        output.append(f"Space: {space}")
        output.append(f"Version: {version}")
        output.append(f"URL: {url}")
        output.append("=" * 80)

        # Add content preview
        storage = page_data.get('body', {}).get('storage', {})
        content = storage.get('value', '')
        if content:
            # Simple text extraction (remove HTML tags)
            import re
            text_content = re.sub(r'<[^>]+>', '', content)
            preview = text_content[:500].strip()
            if preview:
                output.append("\nContent Preview:")
                output.append("-" * 80)
                output.append(preview)
                if len(text_content) > 500:
                    output.append("\n[... content truncated ...]")

        return '\n'.join(output)

    else:
        return json.dumps(page_data, indent=2)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Fetch Confluence wiki pages')
    parser.add_argument('--url', help='Confluence page URL')
    parser.add_argument('--page-id', help='Page ID')
    parser.add_argument('--format', choices=['json', 'html', 'summary'], default='summary',
                        help='Output format (default: summary)')

    args = parser.parse_args()

    if not args.url and not args.page_id:
        parser.error("Either --url or --page-id is required")

    if args.url and args.page_id:
        parser.error("Cannot specify both --url and --page-id")

    token = get_wiki_token()

    if not validate_token(token):
        sys.exit(1)

    # Get page ID
    if args.url:
        # Extract page ID directly from HTML meta tag (more reliable than search)
        page_id = extract_page_id_from_url(args.url, token)
        if not page_id:
            sys.exit(1)
    else:
        page_id = args.page_id

    # Fetch page data
    page_data = get_page_by_id(page_id, token)
    if not page_data:
        sys.exit(1)

    # Output
    output = format_output(page_data, args.format)
    print(output)


if __name__ == '__main__':
    main()
