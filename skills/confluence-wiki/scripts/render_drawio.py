#!/usr/bin/env python3
"""
Draw.io validation and rendering script.

Validates draw.io XML files and generates PNG previews using either
drawio-exporter (Cargo) or Docker fallback.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def check_tool_availability() -> tuple[str, str]:
    """
    Check which rendering tool is available.

    Returns:
        tuple of (tool_name, tool_path or docker_image)
    """
    # Check for drawio-exporter in PATH
    try:
        result = subprocess.run(
            ["which", "drawio-exporter"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            return "drawio-exporter", result.stdout.strip()
    except Exception:
        pass

    # Check for Docker
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            # Check if Docker daemon is running
            daemon_check = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if daemon_check.returncode == 0:
                return "docker", "rlespinasse/drawio-export"
    except Exception:
        pass

    return None, None


def render_with_exporter(input_file: Path, output_dir: Path, output_format: str) -> tuple[bool, str, list[str]]:
    """
    Render using drawio-exporter.

    Returns:
        tuple of (success, preview_path, errors)
    """
    errors = []
    output_dir.mkdir(parents=True, exist_ok=True)

    output_filename = f"{input_file.stem}.{output_format}"
    output_path = output_dir / output_filename

    try:
        result = subprocess.run(
            [
                "drawio-exporter",
                "--format", output_format,
                "--output", str(output_path),
                str(input_file)
            ],
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode != 0:
            errors.append(f"Rendering failed with exit code {result.returncode}")
            if result.stderr:
                errors.append(result.stderr.strip())
            return False, "", errors

        if not output_path.exists():
            errors.append(f"Expected output file not found: {output_path}")
            return False, "", errors

        return True, str(output_path), errors

    except subprocess.TimeoutExpired:
        errors.append("Rendering timed out after 60 seconds")
        return False, "", errors
    except Exception as e:
        errors.append(f"Unexpected error: {str(e)}")
        return False, "", errors


def render_with_docker(input_file: Path, output_dir: Path, output_format: str) -> tuple[bool, str, list[str]]:
    """
    Render using Docker container.

    Returns:
        tuple of (success, preview_path, errors)
    """
    errors = []
    output_dir.mkdir(parents=True, exist_ok=True)

    # Docker requires absolute paths for volume mounts
    input_abs = input_file.absolute()
    output_abs = output_dir.absolute()

    output_filename = f"{input_file.stem}.{output_format}"
    output_path = output_dir / output_filename

    try:
        # First, try to pull the image if not present
        subprocess.run(
            ["docker", "pull", "rlespinasse/drawio-export"],
            capture_output=True,
            timeout=120
        )

        # Run the export
        result = subprocess.run(
            [
                "docker", "run", "--rm",
                "-v", f"{input_abs.parent}:/data/input",
                "-v", f"{output_abs}:/data/output",
                "rlespinasse/drawio-export",
                "--format", output_format,
                "--output", f"/data/output/{output_filename}",
                f"/data/input/{input_file.name}"
            ],
            capture_output=True,
            text=True,
            timeout=90
        )

        if result.returncode != 0:
            errors.append(f"Docker rendering failed with exit code {result.returncode}")
            if result.stderr:
                errors.append(result.stderr.strip())
            return False, "", errors

        if not output_path.exists():
            errors.append(f"Expected output file not found: {output_path}")
            return False, "", errors

        return True, str(output_path), errors

    except subprocess.TimeoutExpired:
        errors.append("Docker rendering timed out")
        return False, "", errors
    except Exception as e:
        errors.append(f"Unexpected error with Docker: {str(e)}")
        return False, "", errors


def validate_xml(input_file: Path) -> tuple[bool, list[str], list[str]]:
    """
    Basic XML validation for draw.io files.

    Returns:
        tuple of (is_valid, errors, warnings)
    """
    errors = []
    warnings = []

    try:
        content = input_file.read_text(encoding='utf-8')

        # Check for required draw.io elements
        if '<mxfile' not in content:
            errors.append("Not a valid draw.io file: missing <mxfile> root element")
            return False, errors, warnings

        if '<diagram' not in content:
            warnings.append("No <diagram> element found - file may be empty")

        if '<mxGraphModel' not in content:
            warnings.append("No <mxGraphModel> found - diagram may be empty")

        # Check for common issues
        if 'id=""' in content:
            warnings.append("Found empty ID attributes - may cause rendering issues")

        return len(errors) == 0, errors, warnings

    except UnicodeDecodeError:
        errors.append("File is not valid UTF-8 encoded text")
        return False, errors, warnings
    except Exception as e:
        errors.append(f"Error reading file: {str(e)}")
        return False, errors, warnings


def main():
    parser = argparse.ArgumentParser(
        description="Validate draw.io files and generate image previews"
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Path to draw.io file. IMPORTANT: Render and inspect before uploading to wiki!"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory for preview output"
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["png", "svg", "pdf"],
        default="png",
        help="Output format (default: png)"
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
            "rendering_success": False,
            "preview_path": "",
            "tool_used": None,
            "errors": [f"Input file not found: {args.input}"],
            "warnings": []
        }
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"ERROR: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Step 1: Basic XML validation
    xml_valid, xml_errors, xml_warnings = validate_xml(args.input)

    if not xml_valid:
        result = {
            "status": "error",
            "rendering_success": False,
            "preview_path": "",
            "tool_used": None,
            "errors": xml_errors,
            "warnings": xml_warnings
        }
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Draw.io Validation: {args.input}")
            print("=" * 60)
            print("XML Validation: ✗ FAILED")
            for error in xml_errors:
                print(f"  ✗ {error}")
        sys.exit(1)

    # Step 2: Check tool availability
    tool, tool_path = check_tool_availability()

    if not tool:
        result = {
            "status": "error",
            "rendering_success": False,
            "preview_path": "",
            "tool_used": None,
            "errors": [
                "No rendering tool available.",
                "Install options:",
                "  1. cargo install drawio-exporter (requires Rust edition 2024)",
                "  2. docker pull rlespinasse/drawio-export (requires Docker daemon running)"
            ],
            "warnings": xml_warnings
        }
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Draw.io Validation: {args.input}")
            print("=" * 60)
            print("✗ No rendering tool available")
            print("\nInstall one of:")
            print("  1. cargo install drawio-exporter")
            print("  2. docker pull rlespinasse/drawio-export")
        sys.exit(1)

    # Step 3: Render
    if tool == "drawio-exporter":
        rendering_success, preview_path, render_errors = render_with_exporter(
            args.input, args.output_dir, args.format
        )
    else:  # docker
        rendering_success, preview_path, render_errors = render_with_docker(
            args.input, args.output_dir, args.format
        )

    # Combine results
    all_errors = xml_errors + render_errors
    overall_success = xml_valid and rendering_success

    result = {
        "status": "success" if overall_success else "error",
        "rendering_success": rendering_success,
        "preview_path": preview_path,
        "tool_used": tool,
        "errors": all_errors,
        "warnings": xml_warnings,
        "reminder": "Before uploading: Visually inspect PNG for lines cutting through boxes. See references/drawio-layout-best-practices.md"
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        # Human-readable output
        print(f"Draw.io Validation: {args.input}")
        print("=" * 60)
        print(f"XML Valid: {'✓' if xml_valid else '✗'}")
        print(f"Rendering Success: {'✓' if rendering_success else '✗'}")
        print(f"Tool Used: {tool}")

        if preview_path:
            print(f"Preview: {preview_path}")

        if xml_warnings:
            print(f"\nWarnings ({len(xml_warnings)}):")
            for warning in xml_warnings:
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
