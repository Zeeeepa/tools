#!/usr/bin/env python3
"""HTML Code Extractor module for extracting code blocks from HTML files."""

import logging
import os
import re
from typing import Dict, List, Optional, Callable

from bs4 import BeautifulSoup

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class HTMLParsingError(Exception):
    """Exception raised when there is an error parsing HTML."""

    pass


class FileCreationError(Exception):
    """Exception raised when there is an error creating files."""

    pass


def extract_code_from_html(
    html_file_path: str,
    output_dir: Optional[str] = None,
    selectors: Optional[Dict[str, str]] = None,
    encoding: str = "utf-8",
    progress_callback: Optional[Callable[[float], None]] = None,
) -> List[str]:
    """Extract code blocks from HTML file and create corresponding files.

    Args:
        html_file_path: Path to the HTML file
        output_dir: Directory to save extracted files. Defaults to current directory.
        selectors: Dictionary of CSS selectors for finding elements
        encoding: File encoding
        progress_callback: Callback for progress updates

    Returns:
        List of created file paths

    Raises:
        FileNotFoundError: If the HTML file does not exist
        HTMLParsingError: If there is an error parsing the HTML
        FileCreationError: If there is an error creating files
    """
    # Validate input
    if not os.path.exists(html_file_path):
        raise FileNotFoundError(f"HTML file does not exist: {html_file_path}")

    # Set default output directory if not provided
    if output_dir is None:
        output_dir = os.getcwd()

    # Set default selectors if not provided
    if selectors is None:
        selectors = {
            "file_path_class": "text-sm text-zinc-400 mb-2 font-mono",
            "code_table_class": "syntax-highlight",
            "code_line_class": "line added",
        }

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Read HTML file
    try:
        with open(html_file_path, "r", encoding=encoding) as file:
            html_content = file.read()
    except UnicodeDecodeError:
        # Try with different encoding if the specified one fails
        try:
            with open(html_file_path, "r", encoding="latin-1") as file:
                html_content = file.read()
            logger.warning(f"Fallback to latin-1 encoding for {html_file_path}")
        except Exception as e:
            raise HTMLParsingError(f"Error reading HTML file: {e}")
    except Exception as e:
        raise HTMLParsingError(f"Error reading HTML file: {e}")

    # Parse HTML
    try:
        soup = BeautifulSoup(html_content, "html.parser")
    except Exception as e:
        raise HTMLParsingError(f"Error parsing HTML: {e}")

    # Find all code blocks
    code_blocks: Dict[str, List[str]] = {}
    current_file = None

    # Find all elements with the specified class for file paths
    file_path_class = selectors["file_path_class"]
    code_table_class = selectors["code_table_class"]
    code_line_class = selectors["code_line_class"]

    file_headers = soup.find_all(class_=re.compile(file_path_class))

    if not file_headers:
        logger.warning(
            "No file headers found. Check if the HTML structure matches the expected pattern."
        )

    total_headers = len(file_headers)

    for i, header in enumerate(file_headers):
        # Update progress
        if progress_callback:
            progress_callback(i / total_headers * 100)

        # Extract file path from the header text
        file_path = header.get_text().strip()

        # Clean up the file path
        if file_path.endswith(":"):
            file_path = file_path[:-1]  # Remove trailing colon

        # Skip empty file paths
        if not file_path:
            continue

        current_file = file_path
        code_blocks[current_file] = []

        # Find the next table with the specified class
        table = header.find_next("table", class_=code_table_class)
        if table:
            # Find all rows with the specified class
            added_lines = table.find_all("tr", class_=code_line_class)

            for line in added_lines:
                # Extract code from the line
                code_text = line.get_text().strip()
                code_blocks[current_file].append(code_text)

    # Create files with extracted code
    files_created: List[str] = []
    for file_path, code_lines in code_blocks.items():
        if not code_lines:
            continue

        # Create full path
        full_path = os.path.join(output_dir, file_path)

        try:
            # Create directory structure
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            # Write code to file
            with open(full_path, "w", encoding=encoding) as file:
                file.write("\n".join(code_lines))

            files_created.append(file_path)
            logger.info(f"Created file: {file_path}")
        except Exception as e:
            logger.error(f"Error creating file {file_path}: {e}")
            raise FileCreationError(f"Error creating file {file_path}: {e}")

    # Final progress update
    if progress_callback:
        progress_callback(100)

    return files_created


def preview_code_from_html(
    html_file_path: str,
    selectors: Optional[Dict[str, str]] = None,
    encoding: str = "utf-8",
) -> Dict[str, List[str]]:
    """Preview code blocks from HTML file without creating files.

    Args:
        html_file_path: Path to the HTML file
        selectors: Dictionary of CSS selectors for finding elements
        encoding: File encoding

    Returns:
        Dictionary of file paths and code lines

    Raises:
        FileNotFoundError: If the HTML file does not exist
        HTMLParsingError: If there is an error parsing the HTML
    """
    # Validate input
    if not os.path.exists(html_file_path):
        raise FileNotFoundError(f"HTML file does not exist: {html_file_path}")

    # Set default selectors if not provided
    if selectors is None:
        selectors = {
            "file_path_class": "text-sm text-zinc-400 mb-2 font-mono",
            "code_table_class": "syntax-highlight",
            "code_line_class": "line added",
        }

    # Read HTML file
    try:
        with open(html_file_path, "r", encoding=encoding) as file:
            html_content = file.read()
    except UnicodeDecodeError:
        # Try with different encoding if the specified one fails
        try:
            with open(html_file_path, "r", encoding="latin-1") as file:
                html_content = file.read()
            logger.warning(f"Fallback to latin-1 encoding for {html_file_path}")
        except Exception as e:
            raise HTMLParsingError(f"Error reading HTML file: {e}")
    except Exception as e:
        raise HTMLParsingError(f"Error reading HTML file: {e}")

    # Parse HTML
    try:
        soup = BeautifulSoup(html_content, "html.parser")
    except Exception as e:
        raise HTMLParsingError(f"Error parsing HTML: {e}")

    # Find all code blocks
    code_blocks: Dict[str, List[str]] = {}
    current_file = None

    # Find all elements with the specified class for file paths
    file_path_class = selectors["file_path_class"]
    code_table_class = selectors["code_table_class"]
    code_line_class = selectors["code_line_class"]

    file_headers = soup.find_all(class_=re.compile(file_path_class))

    if not file_headers:
        logger.warning(
            "No file headers found. Check if the HTML structure matches the expected pattern."
        )

    for header in file_headers:
        # Extract file path from the header text
        file_path = header.get_text().strip()

        # Clean up the file path
        if file_path.endswith(":"):
            file_path = file_path[:-1]  # Remove trailing colon

        # Skip empty file paths
        if not file_path:
            continue

        current_file = file_path
        code_blocks[current_file] = []

        # Find the next table with the specified class
        table = header.find_next("table", class_=code_table_class)
        if table:
            # Find all rows with the specified class
            added_lines = table.find_all("tr", class_=code_line_class)

            for line in added_lines:
                # Extract code from the line
                code_text = line.get_text().strip()
                code_blocks[current_file].append(code_text)

    return code_blocks
