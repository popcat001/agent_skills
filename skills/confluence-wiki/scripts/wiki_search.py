#!/usr/bin/env python3
"""
Search Confluence wiki pages using CQL (Confluence Query Language).

Uses the correct /rest/api/search endpoint that works with Personal Access Tokens.

Examples:
    # Search by text
    python3 wiki_search.py --query "text~'agent evaluation'"

    # Search in specific space
    python3 wiki_search.py --query "space=GenStudio AND text~'architecture'"

    # Search by title
    python3 wiki_search.py --title "Page Title"

    # Limit results
    python3 wiki_search.py --query "text~'ATS'" --limit 5
"""

import os
import sys
import json
import re
import argparse
import urllib.parse
import urllib.request

WIKI_BASE_URL = "https://wiki.corp.adobe.com"
WIKI_TOKEN = os.environ.get("WIKI_TOKEN")

def validate_token():
    """Validate that WIKI_TOKEN is set"""
    if not WIKI_TOKEN:
        print("ERROR: WIKI_TOKEN environment variable not set", file=sys.stderr)
        print("Get token at: https://wiki.corp.adobe.com/plugins/personalaccesstokens/usertokens.action", file=sys.stderr)
        sys.exit(1)

def search_wiki(cql_query, limit=10):
    """
    Search wiki using CQL query.

    Args:
        cql_query: CQL query string (e.g., "text~'keyword'")
        limit: Maximum number of results to return

    Returns:
        Dictionary with search results
    """
    # URL-encode the CQL query
    encoded_query = urllib.parse.quote(cql_query)

    # CRITICAL: Use /rest/api/search NOT /rest/api/content/search
    # The latter doesn't work with Personal Access Tokens in older Confluence versions
    url = f"{WIKI_BASE_URL}/rest/api/search?cql={encoded_query}&limit={limit}"

    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Bearer {WIKI_TOKEN}")
    req.add_header("Accept", "application/json")

    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"ERROR: HTTP {e.code} - {e.reason}", file=sys.stderr)
        print(f"Response: {error_body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        sys.exit(1)

def format_results(data, format_type="summary"):
    """Format search results for display"""
    if format_type == "json":
        print(json.dumps(data, indent=2))
        return

    # Summary format (default)
    total = data.get('totalSize', 0)
    results = data.get('results', [])

    print(f"\nFound {total} results (showing {len(results)})")
    print("=" * 80)

    for idx, result in enumerate(results, 1):
        content = result.get('content', {})
        title = content.get('title', 'No title')
        page_id = content.get('id', 'unknown')
        url = result.get('url', '')
        excerpt = result.get('excerpt', '').replace('@@@hl@@@', '**').replace('@@@endhl@@@', '**')

        print(f"\n{idx}. {title}")
        print(f"   ID: {page_id}")
        print(f"   URL: {WIKI_BASE_URL}{url}")
        if excerpt:
            # Truncate long excerpts
            if len(excerpt) > 200:
                excerpt = excerpt[:200] + "..."
            print(f"   Excerpt: {excerpt}")

    print("\n" + "=" * 80)

def main():
    parser = argparse.ArgumentParser(
        description="Search Confluence wiki using CQL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Text search
  %(prog)s --query "text~'agent evaluation'"

  # Search in space
  %(prog)s --query "space=GenStudio AND text~'architecture'"

  # Search by title (shorthand)
  %(prog)s --title "Page Title"

  # Complex query
  %(prog)s --query "space=GenStudio AND (text~'agent' OR title~'agent')" --limit 5

  # JSON output
  %(prog)s --query "text~'ATS'" --format json

CQL Operators:
  text~'keyword'         - Full-text search
  title~'keyword'        - Title search
  space=SpaceKey         - Filter by space
  type=page              - Filter by type
  AND, OR                - Combine conditions
        """
    )

    parser.add_argument('--query', help='CQL query string')
    parser.add_argument('--title', help='Search by title (shorthand for title~\'...\')')
    parser.add_argument('--space', help='Limit to specific space (e.g., GenStudio)')
    parser.add_argument('--limit', type=int, default=10, help='Maximum results (default: 10)')
    parser.add_argument('--format', choices=['summary', 'json'], default='summary',
                       help='Output format (default: summary)')

    args = parser.parse_args()

    # Build CQL query
    if args.title:
        query = f"title~'{args.title}'"
    elif args.query:
        query = args.query
    else:
        parser.print_help()
        sys.exit(1)

    # Validate token (after usage check so missing-arg errors show help, not token error)
    validate_token()

    # Add space filter if specified — use word-boundary regex to avoid false matches
    # e.g. a query containing 'namespace=foo' must not suppress the space filter
    if args.space and not re.search(r'\bspace\s*=', query, re.IGNORECASE):
        query = f"space={args.space} AND ({query})"

    # Execute search
    results = search_wiki(query, args.limit)

    # Display results
    format_results(results, args.format)

if __name__ == "__main__":
    main()
