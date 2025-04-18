#!/usr/bin/env python3
"""Tests for the HTML Code Extractor module."""

import os
import tempfile
import unittest
from pathlib import Path
from typing import Dict, List

from zeeeepa.tools.html_code_extractor import extract_code_from_html, preview_code_from_html


class TestHTMLCodeExtractor(unittest.TestCase):
    """Test cases for the HTML Code Extractor module."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        # Create a temporary directory for test files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.output_dir = self.temp_dir.name

        # Create a sample HTML file with code blocks
        self.html_content = """
        <html>
        <head>
            <title>Test HTML</title>
        </head>
        <body>
            <div class="text-sm text-zinc-400 mb-2 font-mono">test_file.py:</div>
            <table class="syntax-highlight">
                <tr class="line added">
                    <td>def test_function():</td>
                </tr>
                <tr class="line added">
                    <td>    return "Hello, World!"</td>
                </tr>
            </table>
            
            <div class="text-sm text-zinc-400 mb-2 font-mono">another_file.py:</div>
            <table class="syntax-highlight">
                <tr class="line added">
                    <td>def another_function():</td>
                </tr>
                <tr class="line added">
                    <td>    return "Another function"</td>
                </tr>
            </table>
        </body>
        </html>
        """
        
        self.html_file_path = os.path.join(self.output_dir, "test.html")
        with open(self.html_file_path, "w", encoding="utf-8") as f:
            f.write(self.html_content)

    def tearDown(self) -> None:
        """Tear down test fixtures."""
        self.temp_dir.cleanup()

    def test_extract_code_from_html(self) -> None:
        """Test extracting code from HTML file."""
        # Extract code
        files_created = extract_code_from_html(self.html_file_path, self.output_dir)
        
        # Check that the correct number of files were created
        self.assertEqual(len(files_created), 2)
        
        # Check that the files were created with the correct content
        test_file_path = os.path.join(self.output_dir, "test_file.py")
        another_file_path = os.path.join(self.output_dir, "another_file.py")
        
        self.assertTrue(os.path.exists(test_file_path))
        self.assertTrue(os.path.exists(another_file_path))
        
        with open(test_file_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertEqual(content, "def test_function():\n    return \"Hello, World!\"")
        
        with open(another_file_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertEqual(content, "def another_function():\n    return \"Another function\"")

    def test_preview_code_from_html(self) -> None:
        """Test previewing code from HTML file."""
        # Preview code
        code_blocks = preview_code_from_html(self.html_file_path)
        
        # Check that the correct number of files were found
        self.assertEqual(len(code_blocks), 2)
        
        # Check that the code blocks have the correct content
        self.assertIn("test_file.py", code_blocks)
        self.assertIn("another_file.py", code_blocks)
        
        self.assertEqual(len(code_blocks["test_file.py"]), 2)
        self.assertEqual(len(code_blocks["another_file.py"]), 2)
        
        self.assertEqual(code_blocks["test_file.py"][0], "def test_function():")
        self.assertEqual(code_blocks["test_file.py"][1], "    return \"Hello, World!\"")
        
        self.assertEqual(code_blocks["another_file.py"][0], "def another_function():")
        self.assertEqual(code_blocks["another_file.py"][1], "    return \"Another function\"")

    def test_custom_selectors(self) -> None:
        """Test using custom CSS selectors."""
        # Create a sample HTML file with different CSS classes
        custom_html_content = """
        <html>
        <head>
            <title>Test HTML</title>
        </head>
        <body>
            <div class="file-path">custom_file.py:</div>
            <table class="code-table">
                <tr class="code-line">
                    <td>def custom_function():</td>
                </tr>
                <tr class="code-line">
                    <td>    return "Custom function"</td>
                </tr>
            </table>
        </body>
        </html>
        """
        
        custom_html_file_path = os.path.join(self.output_dir, "custom.html")
        with open(custom_html_file_path, "w", encoding="utf-8") as f:
            f.write(custom_html_content)
        
        # Define custom selectors
        selectors = {
            "file_path_class": "file-path",
            "code_table_class": "code-table",
            "code_line_class": "code-line",
        }
        
        # Extract code with custom selectors
        files_created = extract_code_from_html(
            custom_html_file_path, self.output_dir, selectors=selectors
        )
        
        # Check that the file was created with the correct content
        self.assertEqual(len(files_created), 1)
        
        custom_file_path = os.path.join(self.output_dir, "custom_file.py")
        self.assertTrue(os.path.exists(custom_file_path))
        
        with open(custom_file_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertEqual(content, "def custom_function():\n    return \"Custom function\"")

    def test_empty_html(self) -> None:
        """Test handling empty HTML file."""
        # Create an empty HTML file
        empty_html_file_path = os.path.join(self.output_dir, "empty.html")
        with open(empty_html_file_path, "w", encoding="utf-8") as f:
            f.write("<html><body></body></html>")
        
        # Extract code
        files_created = extract_code_from_html(empty_html_file_path, self.output_dir)
        
        # Check that no files were created
        self.assertEqual(len(files_created), 0)
        
        # Preview code
        code_blocks = preview_code_from_html(empty_html_file_path)
        
        # Check that no code blocks were found
        self.assertEqual(len(code_blocks), 0)

    def test_html_without_code_blocks(self) -> None:
        """Test handling HTML file without code blocks."""
        # Create an HTML file without code blocks
        no_code_html_content = """
        <html>
        <head>
            <title>Test HTML</title>
        </head>
        <body>
            <div class="text-sm text-zinc-400 mb-2 font-mono">test_file.py:</div>
            <p>This is not a code block</p>
        </body>
        </html>
        """
        
        no_code_html_file_path = os.path.join(self.output_dir, "no_code.html")
        with open(no_code_html_file_path, "w", encoding="utf-8") as f:
            f.write(no_code_html_content)
        
        # Extract code
        files_created = extract_code_from_html(no_code_html_file_path, self.output_dir)
        
        # Check that no files were created
        self.assertEqual(len(files_created), 0)
        
        # Preview code
        code_blocks = preview_code_from_html(no_code_html_file_path)
        
        # Check that a file path was found but no code blocks
        self.assertEqual(len(code_blocks), 1)
        self.assertIn("test_file.py", code_blocks)
        self.assertEqual(len(code_blocks["test_file.py"]), 0)


if __name__ == "__main__":
    unittest.main()
