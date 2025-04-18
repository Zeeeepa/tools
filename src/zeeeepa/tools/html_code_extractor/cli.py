#!/usr/bin/env python3
"""Command-line interface for HTML Code Extractor."""

import argparse
import logging
import os
import sys
from typing import Dict, Optional

from .extractor import extract_code_from_html, preview_code_from_html

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Extract code blocks from HTML files and create corresponding files."
    )
    parser.add_argument(
        "html_file", help="Path to the HTML file containing code blocks"
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        help="Directory to save extracted files (default: current directory)",
        default=os.getcwd(),
    )
    parser.add_argument(
        "-e",
        "--encoding",
        help="Encoding of the HTML file (default: utf-8)",
        default="utf-8",
    )
    parser.add_argument(
        "-p",
        "--preview",
        help="Preview files without creating them",
        action="store_true",
    )
    parser.add_argument(
        "--file-path-class",
        help="CSS class for file path elements (default: text-sm text-zinc-400 mb-2 font-mono)",
        default="text-sm text-zinc-400 mb-2 font-mono",
    )
    parser.add_argument(
        "--code-table-class",
        help="CSS class for code table elements (default: syntax-highlight)",
        default="syntax-highlight",
    )
    parser.add_argument(
        "--code-line-class",
        help="CSS class for code line elements (default: line added)",
        default="line added",
    )
    parser.add_argument(
        "-v", "--verbose", help="Enable verbose output", action="store_true"
    )
    return parser.parse_args()


def main() -> int:
    """Main entry point for the CLI.

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    args = parse_args()

    # Set up logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Validate input file
    if not os.path.exists(args.html_file):
        logger.error(f"HTML file does not exist: {args.html_file}")
        return 1

    # Set up selectors
    selectors: Dict[str, str] = {
        "file_path_class": args.file_path_class,
        "code_table_class": args.code_table_class,
        "code_line_class": args.code_line_class,
    }

    try:
        if args.preview:
            # Preview files without creating them
            code_blocks = preview_code_from_html(
                args.html_file, selectors=selectors, encoding=args.encoding
            )
            
            if not code_blocks:
                logger.warning("No code blocks found in the HTML file.")
                return 0
            
            # Print preview
            print(f"Found {len(code_blocks)} file(s) in the HTML:")
            for file_path, code_lines in code_blocks.items():
                print(f"- {file_path} ({len(code_lines)} lines)")
        else:
            # Extract code and create files
            files_created = extract_code_from_html(
                args.html_file,
                output_dir=args.output_dir,
                selectors=selectors,
                encoding=args.encoding,
            )
            
            if not files_created:
                logger.warning("No files were created.")
                return 0
            
            # Print summary
            print(f"Successfully extracted {len(files_created)} file(s) to {args.output_dir}:")
            for file_path in files_created:
                print(f"- {file_path}")
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
