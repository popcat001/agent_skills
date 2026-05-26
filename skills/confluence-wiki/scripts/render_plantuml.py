#!/usr/bin/env python3
"""
PlantUML validation and rendering script.

Validates PlantUML syntax and generates PNG previews for visual inspection
before uploading to Confluence.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def validate_syntax(input_file: Path) -> tuple[bool, list[str], list[str]]:
    """
    Validate PlantUML syntax using plantuml -checksyntax.

    Returns:
        tuple of (is_valid, errors, warnings)
    """
    errors = []
    warnings = []

    try:
        result = subprocess.run(
            ["plantuml", "-checksyntax", str(input_file)],
            capture_output=True,
            text=True,
            timeout=30
        )

        # PlantUML returns 0 for success, non-zero for errors
        if result.returncode != 0:
            # Parse error output to extract line numbers and messages
            for line in result.stdout.splitlines() + result.stderr.splitlines():
                line = line.strip()
                if line and not line.startswith("PlantUML"):
                    if "error" in line.lower() or "cannot" in line.lower():
                        errors.append(line)
                    elif "warning" in line.lower():
                        warnings.append(line)

        return result.returncode == 0, errors, warnings

    except subprocess.TimeoutExpired:
        errors.append("Syntax validation timed out after 30 seconds")
        return False, errors, warnings
    except FileNotFoundError:
        errors.append("plantuml command not found. Install with: brew install plantuml")
        return False, errors, warnings
    except Exception as e:
        errors.append(f"Unexpected error during syntax validation: {str(e)}")
        return False, errors, warnings


def render_png(input_file: Path, output_dir: Path) -> tuple[bool, str, list[str]]:
    """
    Render PlantUML diagram to PNG.

    Returns:
        tuple of (success, preview_path, errors)
    """
    errors = []
    preview_path = ""

    try:
        # Ensure output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)

        # Run plantuml to generate PNG
        result = subprocess.run(
            ["plantuml", "-tpng", "-o", str(output_dir.absolute()), str(input_file)],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            errors.append(f"Rendering failed with exit code {result.returncode}")
            for line in result.stdout.splitlines() + result.stderr.splitlines():
                line = line.strip()
                if line and not line.startswith("PlantUML"):
                    errors.append(line)
            return False, "", errors

        # Determine output filename (PlantUML names it based on input)
        stem = input_file.stem
        preview_path = str(output_dir / f"{stem}.png")

        if not Path(preview_path).exists():
            errors.append(f"Expected output file not found: {preview_path}")
            return False, "", errors

        return True, preview_path, errors

    except subprocess.TimeoutExpired:
        errors.append("Rendering timed out after 60 seconds")
        return False, "", errors
    except FileNotFoundError:
        errors.append("plantuml command not found. Install with: brew install plantuml")
        return False, "", errors
    except Exception as e:
        errors.append(f"Unexpected error during rendering: {str(e)}")
        return False, "", errors


def main():
    parser = argparse.ArgumentParser(
        description="Validate PlantUML syntax and generate PNG preview"
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Path to PlantUML file (.puml, .plantuml, or .txt)"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory for PNG preview output"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )

    args = parser.parse_args()

    # Verify input file exists
    if not args.input.exists():
        result = {
            "status": "error",
            "syntax_valid": False,
            "rendering_success": False,
            "preview_path": "",
            "errors": [f"Input file not found: {args.input}"],
            "warnings": []
        }
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"ERROR: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Step 1: Validate syntax
    syntax_valid, syntax_errors, syntax_warnings = validate_syntax(args.input)

    # Step 2: Render PNG (even if syntax validation failed, attempt render)
    rendering_success, preview_path, render_errors = render_png(args.input, args.output_dir)

    # Combine results
    all_errors = syntax_errors + render_errors
    overall_success = syntax_valid and rendering_success

    result = {
        "status": "success" if overall_success else "error",
        "syntax_valid": syntax_valid,
        "rendering_success": rendering_success,
        "preview_path": preview_path,
        "errors": all_errors,
        "warnings": syntax_warnings
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        # Human-readable output
        print(f"PlantUML Validation: {args.input}")
        print("=" * 60)
        print(f"Syntax Valid: {'✓' if syntax_valid else '✗'}")
        print(f"Rendering Success: {'✓' if rendering_success else '✗'}")

        if preview_path:
            print(f"Preview: {preview_path}")

        if syntax_warnings:
            print(f"\nWarnings ({len(syntax_warnings)}):")
            for warning in syntax_warnings:
                print(f"  ⚠ {warning}")

        if all_errors:
            print(f"\nErrors ({len(all_errors)}):")
            for error in all_errors:
                print(f"  ✗ {error}")

        if overall_success:
            print("\n✓ Validation complete - diagram ready for upload")
        else:
            print("\n✗ Validation failed - fix errors before uploading")

    sys.exit(0 if overall_success else 1)


if __name__ == "__main__":
    main()
