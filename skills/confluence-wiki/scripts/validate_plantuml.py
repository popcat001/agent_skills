#!/usr/bin/env python3
"""
PlantUML Syntax Validator for Confluence

Validates PlantUML diagram syntax before submission to avoid wiki rendering errors.
Common issues: multi-line arrow labels, unclosed blocks, invalid syntax.

Usage:
    python3 validate_plantuml.py diagram.plantuml
    cat diagram.plantuml | python3 validate_plantuml.py
"""

import re
import sys


def validate_plantuml(content: str) -> tuple[bool, list[str]]:
    """
    Validate PlantUML syntax for common errors.

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    lines = content.split('\n')

    # Check 1: Must start with @startuml
    if not any(line.strip().startswith('@startuml') for line in lines):
        errors.append("Missing @startuml at start of diagram")

    # Check 2: Must end with @enduml
    if not any(line.strip().startswith('@enduml') for line in lines):
        errors.append("Missing @enduml at end of diagram")

    # Check 3: Check for multi-line arrow labels (common error)
    in_multiline_arrow = False
    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Arrow pattern: ->  or -->  or ->>  etc.
        if re.search(r'(->|-->|->>|<<-|<--)', stripped):
            # Check if arrow label ends with colon but no complete message
            if ':' in stripped:
                # This is okay - inline label
                pass
            else:
                # Arrow without label - check next line for orphaned text
                if i < len(lines) and lines[i].strip() and not lines[i].strip().startswith(('note', 'activate', 'deactivate', 'alt', 'else', 'end', 'par', '@')):
                    errors.append(f"Line {i}: Possible multi-line arrow label. Arrow labels must be inline, not on next line")

    # Check 4: Unclosed blocks
    block_stack = []
    block_keywords = {
        'alt': 'end',
        'par': 'end',
        'loop': 'end',
        'opt': 'end',
        'note': 'end note',
        'group': 'end',
        'box': 'end box'
    }

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Check for block starts
        for keyword in block_keywords:
            if stripped.startswith(keyword + ' ') or stripped == keyword:
                block_stack.append((keyword, i))

        # Check for block ends
        if stripped in ('end', 'end note', 'end box'):
            if block_stack:
                block_stack.pop()
            else:
                errors.append(f"Line {i}: 'end' without matching block start")

    # Check for unclosed blocks
    for keyword, line_num in block_stack:
        errors.append(f"Line {line_num}: Unclosed '{keyword}' block")

    # Check 5: Invalid participant/actor names
    for i, line in enumerate(lines, 1):
        if re.match(r'(participant|actor)\s+"[^"]*$', line.strip()):
            errors.append(f"Line {i}: Unclosed quote in participant/actor name")

    return (len(errors) == 0, errors)


def suggest_fixes(content: str) -> str:
    """
    Suggest fixes for common PlantUML issues.
    """
    suggestions = []

    lines = content.split('\n')

    # Suggestion 1: Look for possible multi-line arrow patterns
    for i, line in enumerate(lines):
        if re.search(r'(->|-->|->>)', line.strip()):
            if ':' not in line and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line and not next_line.startswith(('note', 'activate', 'deactivate', '@')):
                    suggestions.append(f"Consider merging lines {i+1} and {i+2}:")
                    suggestions.append(f"  Current: {line.strip()}")
                    suggestions.append(f"           {next_line}")
                    suggestions.append(f"  Suggested: {line.strip()}: {next_line}")

    return '\n'.join(suggestions) if suggestions else "No automatic suggestions available"


def main():
    """Main entry point for CLI usage."""
    if len(sys.argv) > 1:
        # File mode
        input_file = sys.argv[1]
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        # Pipe mode
        content = sys.stdin.read()

    is_valid, errors = validate_plantuml(content)

    if is_valid:
        print("✅ PlantUML syntax is valid")
        sys.exit(0)
    else:
        print("❌ PlantUML syntax errors found:\n")
        for error in errors:
            print(f"   {error}")

        print("\n💡 Suggestions:")
        print(suggest_fixes(content))

        sys.exit(1)


if __name__ == '__main__':
    main()
