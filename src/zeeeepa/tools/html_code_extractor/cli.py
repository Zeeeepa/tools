#!/usr/bin/env python3
"""Command-line interface for HTML Code Extractor."""

import argparse
import logging
import os
import sys
from typing import Dict, List, Optional

from zeeeepa.tools.html_code_extractor.extractor import extract_code_from_html

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Extract code blocks from HTML files and create corresponding files."
    )
    parser.add_argument(
        "html_file",
        help="Path to the HTML file",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        default=os.path.join(os.path.expanduser("~"), "Desktop", "WEB-CODES"),
        help="Directory to save extracted files (default: ~/Desktop/WEB-CODES)",
    )
    parser.add_argument(
        "--file-path-class",
        default="text-sm text-zinc-400 mb-2 font-mono",
        help="CSS class for file path elements",
    )
    parser.add_argument(
        "--code-table-class",
        default="syntax-highlight",
        help="CSS class for code table elements",
    )
    parser.add_argument(
        "--code-line-class",
        default="line added",
        help="CSS class for code line elements",
    )
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="File encoding (default: utf-8)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    return parser.parse_args()


def main() -> int:
    """Run the HTML Code Extractor CLI.

    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    args = parse_args()

    # Set up logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Check if HTML file exists
    if not os.path.exists(args.html_file):
        logger.error(f"HTML file does not exist: {args.html_file}")
        return 1

    # Create selectors dictionary
    selectors: Dict[str, str] = {
        "file_path_class": args.file_path_class,
        "code_table_class": args.code_table_class,
        "code_line_class": args.code_line_class,
    }

    try:
        # Extract code
        files_created: List[str] = extract_code_from_html(
            html_file_path=args.html_file,
            output_dir=args.output_dir,
            selectors=selectors,
            encoding=args.encoding,
        )

        if files_created:
            logger.info(f"Successfully extracted {len(files_created)} files to {args.output_dir}")
            return 0
        else:
            logger.warning(
                "No files were created. Check if the HTML structure matches the expected pattern."
            )
            return 1
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
