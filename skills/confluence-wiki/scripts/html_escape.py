#!/usr/bin/env python3
"""
HTML Entity Escaping for Confluence Storage Format

This script safely escapes special characters in Confluence page content
to prevent "Error parsing xhtml" errors when submitting to the Confluence API.

Usage:
    python3 html_escape.py input.html output.html
    cat input.html | python3 html_escape.py > output.html
"""

import re
import sys


def escape_confluence_html(content: str) -> str:
    """
    Escape HTML entities for Confluence storage format.

    Rules:
    1. Escape & that aren't already part of entities (&lt;, &gt;, &amp;, etc.)
    2. Escape < and > in text context (NOT in HTML tags)
    3. Preserve all HTML tags intact

    Args:
        content: Raw HTML content with potential unescaped entities

    Returns:
        Properly escaped HTML safe for Confluence API submission
    """

    # Step 1: Escape & that aren't already part of entities
    # Match & not followed by a valid HTML entity (named or numeric)
    # Named entities: &mdash; &rarr; &amp; &lt; etc. (any sequence of letters followed by ;)
    # Numeric entities: &#123; or &#x1F4A9;
    content = re.sub(
        r'&(?![a-zA-Z]+;|#\d+;|#x[0-9a-fA-F]+;)',
        r'&amp;',
        content
    )

    # Step 2: Escape < in specific text contexts (NOT in HTML tags)
    # Pattern: space < space digit (e.g., "score < 4")
    content = re.sub(r' < (\d)', r' &lt; \1', content)

    # Pattern: specific phrases like "score <", "threshold <", "value <"
    content = re.sub(
        r'(score|threshold|value|number|count|rating) < ',
        r'\1 &lt; ',
        content
    )

    # Step 3: Escape > in specific text contexts
    # Pattern: space > space digit (e.g., "value > 0")
    content = re.sub(r' > (\d)', r' &gt; \1', content)

    # Pattern: specific phrases like "score >", "threshold >", "value >"
    content = re.sub(
        r'(score|threshold|value|number|count|rating) > ',
        r'\1 &gt; ',
        content
    )

    return content


def validate_escaping(content: str) -> list[str]:
    """
    Validate that content is properly escaped for Confluence.

    Returns:
        List of warnings about potentially unescaped content
    """
    warnings = []

    # Check for common unescaped patterns
    if re.search(r' < \d', content):
        warnings.append("Found potential unescaped '<' before digit")

    if re.search(r' > \d', content):
        warnings.append("Found potential unescaped '>' before digit")

    # Check for & not part of entity (but allow any valid named/numeric entity)
    if re.search(r'&(?![a-zA-Z]+;|#\d+;|#x[0-9a-fA-F]+;)', content):
        warnings.append("Found potential unescaped '&' not part of entity")

    # Check for common phrases that need escaping
    phrases = ['score <', 'threshold <', 'value <', 'Hook &', 'Setup &']
    for phrase in phrases:
        if phrase in content and '&lt;' not in content and '&amp;' not in content:
            warnings.append(f"Found phrase '{phrase}' that may need escaping")

    return warnings


def main():
    """Main entry point for CLI usage."""
    if len(sys.argv) > 1:
        # File-based mode
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None

        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        escaped = escape_confluence_html(content)
        warnings = validate_escaping(escaped)

        if warnings:
            print("⚠️  Validation warnings:", file=sys.stderr)
            for warning in warnings:
                print(f"   - {warning}", file=sys.stderr)

        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(escaped)
            print(f"✅ Escaped content written to {output_file}", file=sys.stderr)
        else:
            print(escaped)
    else:
        # Pipe mode: read from stdin, write to stdout
        content = sys.stdin.read()
        escaped = escape_confluence_html(content)
        print(escaped)


if __name__ == '__main__':
    main()
