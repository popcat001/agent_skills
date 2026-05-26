#!/usr/bin/env python3
"""
Confluence Wiki Attachment Uploader

Upload or update attachments on Confluence pages.

Usage:
    python3 wiki_attach_file.py --page-id 3650098119 --file diagram.drawio --comment "Architecture diagram"
    python3 wiki_attach_file.py --page-id 3650098119 --file diagram.drawio --update
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


def upload_attachment(page_id: str, file_path: str, comment: Optional[str] = None, update: bool = False) -> Dict[str, Any]:
    """
    Upload a file as an attachment to a Confluence page.

    Args:
        page_id: Page ID to attach to
        file_path: Path to file to upload
        comment: Optional comment for the attachment
        update: If True, update existing attachment instead of creating new version

    Returns:
        JSON response from API
    """
    token = get_wiki_token()

    if not validate_token(token):
        sys.exit(1)

    if not os.path.exists(file_path):
        print(f"ERROR: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    file_name = os.path.basename(file_path)

    # Build curl command
    # For Confluence Server/Data Center, use /rest/api/content/{id}/child/attachment
    url = f"https://wiki.corp.adobe.com/rest/api/content/{page_id}/child/attachment"

    cmd = [
        'curl', '-s',
        '-X', 'POST' if not update else 'PUT',
        '-H', f'Authorization: Bearer {token}',
        '-H', 'X-Atlassian-Token: nocheck',  # Required to prevent CSRF errors
        '-F', f'file=@{file_path}'
    ]

    # Add comment if provided
    if comment:
        cmd.extend(['-F', f'comment={comment}'])

    # Add minorEdit parameter for updates
    if update:
        cmd.extend(['-F', 'minorEdit=true'])

    cmd.append(url)

    print(f"Uploading {file_name} to page {page_id}...", file=sys.stderr)

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"ERROR: curl command failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    try:
        response = json.loads(result.stdout)

        # Check for error response
        if 'statusCode' in response and response.get('statusCode') >= 400:
            print(f"ERROR: API returned error: {response.get('message', 'Unknown error')}", file=sys.stderr)
            print(f"Full response: {json.dumps(response, indent=2)}", file=sys.stderr)
            sys.exit(1)

        return response
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse JSON response: {e}", file=sys.stderr)
        print(f"Response: {result.stdout}", file=sys.stderr)
        sys.exit(1)


def list_attachments(page_id: str) -> Dict[str, Any]:
    """
    List all attachments on a Confluence page.

    Args:
        page_id: Page ID to query

    Returns:
        JSON response with attachments list
    """
    token = get_wiki_token()

    if not validate_token(token):
        sys.exit(1)

    url = f"https://wiki.corp.adobe.com/rest/api/content/{page_id}/child/attachment"

    cmd = [
        'curl', '-s',
        '-H', f'Authorization: Bearer {token}',
        url
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"ERROR: curl command failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse JSON response: {e}", file=sys.stderr)
        print(f"Response: {result.stdout}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Upload attachments to Confluence pages')
    parser.add_argument('--page-id', required=True, help='Page ID to attach to')
    parser.add_argument('--file', help='File to upload')
    parser.add_argument('--comment', help='Attachment comment (optional)')
    parser.add_argument('--update', action='store_true', help='Update existing attachment')
    parser.add_argument('--list', action='store_true', help='List attachments on page')

    args = parser.parse_args()

    if args.list:
        print(f"Fetching attachments for page {args.page_id}...", file=sys.stderr)
        response = list_attachments(args.page_id)

        attachments = response.get('results', [])
        print(f"\n✅ Found {len(attachments)} attachment(s):", file=sys.stderr)
        for att in attachments:
            print(f"  - {att.get('title')} (ID: {att.get('id')})", file=sys.stderr)

        print("\nFull response:")
        print(json.dumps(response, indent=2))
    else:
        if not args.file:
            parser.error("--file is required unless using --list")

        response = upload_attachment(args.page_id, args.file, args.comment, args.update)

        # Extract attachment info from response
        if 'results' in response:
            # Multiple attachments returned (typical response)
            for att in response['results']:
                att_id = att.get('id', 'unknown')
                att_title = att.get('title', 'unknown')
                print(f"✅ Uploaded: {att_title} (ID: {att_id})")
        elif 'id' in response:
            # Single attachment returned
            att_id = response.get('id', 'unknown')
            att_title = response.get('title', 'unknown')
            print(f"✅ Uploaded: {att_title} (ID: {att_id})")
        else:
            print("✅ Upload completed")

        print("\nFull response:")
        print(json.dumps(response, indent=2))


if __name__ == '__main__':
    main()
