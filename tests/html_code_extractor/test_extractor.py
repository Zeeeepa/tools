"""Tests for the HTML Code Extractor module."""

import os
import tempfile
from typing import Dict, List

import pytest

from zeeeepa.tools.html_code_extractor import (
    extract_code_from_html,
    preview_code_from_html,
    HTMLParsingError,
    FileCreationError,
)


def create_test_html(content: str) -> str:
    """Create a temporary HTML file for testing.

    Args:
        content: HTML content to write to the file

    Returns:
        Path to the temporary HTML file
    """
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as f:
        f.write(content.encode("utf-8"))
        return f.name


def test_extract_code_from_html_empty_file() -> None:
    """Test extracting code from an empty HTML file."""
    html_file = create_test_html("")
    try:
        output_dir = tempfile.mkdtemp()
        files_created = extract_code_from_html(html_file, output_dir)
        assert len(files_created) == 0
    finally:
        os.unlink(html_file)


def test_extract_code_from_html_no_code_blocks() -> None:
    """Test extracting code from an HTML file with no code blocks."""
    html_content = """
    <html>
    <body>
        <h1>Test</h1>
        <p>This is a test</p>
    </body>
    </html>
    """
    html_file = create_test_html(html_content)
    try:
        output_dir = tempfile.mkdtemp()
        files_created = extract_code_from_html(html_file, output_dir)
        assert len(files_created) == 0
    finally:
        os.unlink(html_file)


def test_extract_code_from_html_with_code_blocks() -> None:
    """Test extracting code from an HTML file with code blocks."""
    html_content = """
    <html>
    <body>
        <div class="text-sm text-zinc-400 mb-2 font-mono">test.py:</div>
        <table class="syntax-highlight">
            <tr class="line added"><td>print("Hello, World!")</td></tr>
            <tr class="line added"><td>print("This is a test")</td></tr>
        </table>
        
        <div class="text-sm text-zinc-400 mb-2 font-mono">folder/test2.py:</div>
        <table class="syntax-highlight">
            <tr class="line added"><td>def test_function():</td></tr>
            <tr class="line added"><td>    return "Test"</td></tr>
        </table>
    </body>
    </html>
    """
    html_file = create_test_html(html_content)
    try:
        output_dir = tempfile.mkdtemp()
        files_created = extract_code_from_html(html_file, output_dir)
        assert len(files_created) == 2
        assert "test.py" in files_created
        assert "folder/test2.py" in files_created
        
        # Check file contents
        with open(os.path.join(output_dir, "test.py"), "r") as f:
            content = f.read()
            assert 'print("Hello, World!")' in content
            assert 'print("This is a test")' in content
        
        with open(os.path.join(output_dir, "folder/test2.py"), "r") as f:
            content = f.read()
            assert "def test_function():" in content
            assert "    return \"Test\"" in content
    finally:
        os.unlink(html_file)


def test_preview_code_from_html() -> None:
    """Test previewing code from an HTML file."""
    html_content = """
    <html>
    <body>
        <div class="text-sm text-zinc-400 mb-2 font-mono">test.py:</div>
        <table class="syntax-highlight">
            <tr class="line added"><td>print("Hello, World!")</td></tr>
            <tr class="line added"><td>print("This is a test")</td></tr>
        </table>
    </body>
    </html>
    """
    html_file = create_test_html(html_content)
    try:
        code_blocks = preview_code_from_html(html_file)
        assert len(code_blocks) == 1
        assert "test.py" in code_blocks
        assert len(code_blocks["test.py"]) == 2
        assert code_blocks["test.py"][0] == 'print("Hello, World!")'
        assert code_blocks["test.py"][1] == 'print("This is a test")'
    finally:
        os.unlink(html_file)


def test_file_not_found() -> None:
    """Test handling of non-existent HTML file."""
    with pytest.raises(FileNotFoundError):
        extract_code_from_html("non_existent_file.html")


def test_custom_selectors() -> None:
    """Test using custom CSS selectors."""
    html_content = """
    <html>
    <body>
        <div class="file-path">test.py:</div>
        <table class="code-table">
            <tr class="code-line"><td>print("Hello, World!")</td></tr>
        </table>
    </body>
    </html>
    """
    html_file = create_test_html(html_content)
    try:
        output_dir = tempfile.mkdtemp()
        selectors = {
            "file_path_class": "file-path",
            "code_table_class": "code-table",
            "code_line_class": "code-line",
        }
        files_created = extract_code_from_html(html_file, output_dir, selectors)
        assert len(files_created) == 1
        assert "test.py" in files_created
        
        # Check file contents
        with open(os.path.join(output_dir, "test.py"), "r") as f:
            content = f.read()
            assert 'print("Hello, World!")' in content
    finally:
        os.unlink(html_file)
