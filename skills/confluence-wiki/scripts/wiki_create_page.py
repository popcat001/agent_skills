#!/usr/bin/env python3
"""
Confluence Wiki Page Creator

Create or update Confluence wiki pages with proper error handling and validation.

Usage:
    python3 wiki_create_page.py --title "Page Title" --space "GenStudio" --parent 3137163046 --file content.html
    python3 wiki_create_page.py --update 1234567 --file content.html --version 2
"""

import os
import sys
import json
import re
import subprocess
import tempfile
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


def create_page(title: str, space_key: str, content: str, parent_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new Confluence page.

    Args:
        title: Page title
        space_key: Space key (e.g., "GenStudio")
        content: HTML content in Confluence storage format
        parent_id: Optional parent page ID

    Returns:
        JSON response from API
    """
    token = get_wiki_token()

    if not validate_token(token):
        sys.exit(1)

    # Build payload
    payload = {
        "type": "page",
        "title": title,
        "space": {"key": space_key},
        "body": {
            "storage": {
                "value": content,
                "representation": "storage"
            }
        }
    }

    if parent_id:
        payload["ancestors"] = [{"id": parent_id}]

    # Write to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(payload, f, indent=2)
        payload_file = f.name

    try:
        cmd = [
            'curl', '-s',
            '-X', 'POST',
            '-H', f'Authorization: Bearer {token}',
            '-H', 'Content-Type: application/json',
            '-d', f'@{payload_file}',
            'https://wiki.corp.adobe.com/rest/api/content'
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
    finally:
        os.unlink(payload_file)


def extract_inline_comments(html: str) -> set:
    """Extract inline comment ac:ref values from HTML.

    Returns:
        Set of ac:ref values found in inline comment markers
    """
    pattern = r'<ac:inline-comment-marker[^>]*ac:ref="([^"]+)"[^>]*>'
    return set(re.findall(pattern, html))


def validate_markup_preservation(page_id: str, new_content: str) -> bool:
    """
    Validate that new content preserves markup from current page.

    Args:
        page_id: Page ID to validate
        new_content: New HTML content to validate

    Returns:
        True if validation passes, False otherwise
    """
    token = get_wiki_token()

    # Fetch current page HTML
    print("⏳ Validating markup preservation...", file=sys.stderr)
    get_cmd = [
        'curl', '-s',
        '-H', f'Authorization: Bearer {token}',
        f'https://wiki.corp.adobe.com/rest/api/content/{page_id}?expand=body.storage'
    ]

    result = subprocess.run(get_cmd, capture_output=True, text=True)

    try:
        data = json.loads(result.stdout)
        current_html = data['body']['storage']['value']
    except (json.JSONDecodeError, KeyError) as e:
        print(f"\n⚠️  WARNING: Could not fetch current page for validation: {e}", file=sys.stderr)
        print("This may indicate:", file=sys.stderr)
        print("  - Page ID is invalid", file=sys.stderr)
        print("  - VPN connection lost", file=sys.stderr)
        print("  - WIKI_TOKEN is invalid/expired", file=sys.stderr)
        print("\nWithout validation, inline comments and other markup may be lost!", file=sys.stderr)
        print("Recommendation: Fix the issue and retry, or use --skip-validation to force.", file=sys.stderr)
        return False  # Fail by default to prevent accidental markup loss

    # Improved validation: check that all original inline comments (by ac:ref) are preserved
    current_refs = extract_inline_comments(current_html)
    new_refs = extract_inline_comments(new_content)

    lost_refs = current_refs - new_refs
    if lost_refs:
        lost_count = len(lost_refs)
        preserved_count = len(current_refs & new_refs)
        print(f"\n⚠️  WARNING: Markup will be lost in this update!", file=sys.stderr)
        print(f"❌ Lost {lost_count} inline comment(s): {', '.join(sorted(lost_refs))}", file=sys.stderr)
        print(f"✓ Preserved {preserved_count} inline comment(s)", file=sys.stderr)
        return False

    if current_refs:
        print(f"✅ Markup validation passed ({len(current_refs)} inline comments preserved)", file=sys.stderr)
    return True


def update_page(page_id: str, content: str, version: int, skip_validation: bool = False) -> Dict[str, Any]:
    """
    Update an existing Confluence page with automatic markup validation.

    Args:
        page_id: Page ID to update
        content: New HTML content
        version: New version number (current version + 1)
        skip_validation: Skip markup validation (not recommended)

    Returns:
        JSON response from API
    """
    token = get_wiki_token()

    if not validate_token(token):
        sys.exit(1)

    # Validate markup preservation (unless explicitly skipped)
    if not skip_validation:
        if not validate_markup_preservation(page_id, content):
            print("\n❌ MARKUP VALIDATION FAILED", file=sys.stderr)
            print("⚠️  Updating this page will lose inline comments or other markup!", file=sys.stderr)
            print("\nOptions:", file=sys.stderr)
            print("  1. Fix the issue and try again (RECOMMENDED)", file=sys.stderr)
            print("  2. Use --skip-validation to force update (NOT RECOMMENDED)", file=sys.stderr)
            sys.exit(1)

    # Get current page info for title and space
    get_cmd = [
        'curl', '-s',
        '-H', f'Authorization: Bearer {token}',
        f'https://wiki.corp.adobe.com/rest/api/content/{page_id}'
    ]

    get_result = subprocess.run(get_cmd, capture_output=True, text=True)

    try:
        current_page = json.loads(get_result.stdout)
        title = current_page['title']
        space_key = current_page['space']['key']
    except (json.JSONDecodeError, KeyError) as e:
        print(f"ERROR: Failed to get current page info: {e}", file=sys.stderr)
        sys.exit(1)

    # Build update payload
    payload = {
        "id": page_id,
        "type": "page",
        "title": title,
        "space": {"key": space_key},
        "body": {
            "storage": {
                "value": content,
                "representation": "storage"
            }
        },
        "version": {
            "number": version,
            "minorEdit": False
        }
    }

    # Write to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(payload, f, indent=2)
        payload_file = f.name

    try:
        cmd = [
            'curl', '-s',
            '-X', 'PUT',
            '-H', f'Authorization: Bearer {token}',
            '-H', 'Content-Type: application/json',
            '-d', f'@{payload_file}',
            f'https://wiki.corp.adobe.com/rest/api/content/{page_id}'
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
    finally:
        os.unlink(payload_file)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Create or update Confluence wiki pages with automatic markup validation',
        epilog="""
Examples:
    # Create new page
    python3 wiki_create_page.py --title "Page Title" --space "GenStudio" --file content.html

    # Update existing page (with automatic validation)
    python3 wiki_create_page.py --update 3647578884 --version 42 --file content.html

    # Update without validation (NOT RECOMMENDED)
    python3 wiki_create_page.py --update 3647578884 --version 42 --file content.html --skip-validation
        """
    )
    parser.add_argument('--title', help='Page title (required for create)')
    parser.add_argument('--space', help='Space key (required for create, e.g., "GenStudio")')
    parser.add_argument('--parent', help='Parent page ID (optional)')
    parser.add_argument('--file', required=True, help='HTML content file (Confluence storage format)')
    parser.add_argument('--update', help='Update existing page by ID')
    parser.add_argument('--version', type=int, help='Version number for update')
    parser.add_argument('--skip-validation', action='store_true', help='Skip markup validation (not recommended)')

    args = parser.parse_args()

    # Read content from file
    try:
        with open(args.file, 'r') as f:
            content = f.read()
    except IOError as e:
        print(f"ERROR: Failed to read content file: {e}", file=sys.stderr)
        sys.exit(1)

    # Create or update
    if args.update:
        if not args.version:
            parser.error("--version is required for update")

        print(f"Updating page {args.update}...", file=sys.stderr)
        response = update_page(args.update, content, args.version, args.skip_validation)
        print(f"✅ Updated page {args.update} to version {args.version}")
    else:
        if not args.title or not args.space:
            parser.error("--title and --space are required for create")

        print(f"Creating page '{args.title}' in {args.space}...", file=sys.stderr)
        response = create_page(args.title, args.space, content, args.parent)
        page_id = response.get('id', 'unknown')
        webui = response.get('_links', {}).get('webui', '')
        print(f"✅ Created page ID: {page_id}")
        if webui:
            print(f"   URL: https://wiki.corp.adobe.com{webui}")

    # Print full response
    print(json.dumps(response, indent=2))


if __name__ == '__main__':
    main()
