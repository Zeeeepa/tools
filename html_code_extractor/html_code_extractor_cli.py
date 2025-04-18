#!/usr/bin/env python3
import os
import re
import argparse
from bs4 import BeautifulSoup
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def extract_code_from_html(html_file_path, output_dir=None, file_path_selector=None, code_table_selector=None, code_line_selector=None):
    """
    Extract code blocks from HTML file and create corresponding files.
    
    Args:
        html_file_path (str): Path to the HTML file
        output_dir (str, optional): Directory to save extracted files. Defaults to current directory.
        file_path_selector (str, optional): CSS selector for file paths. Defaults to "text-sm text-zinc-400 mb-2 font-mono".
        code_table_selector (str, optional): CSS selector for code tables. Defaults to "syntax-highlight".
        code_line_selector (str, optional): CSS selector for code lines. Defaults to "line added".
    
    Returns:
        list: List of created file paths
    """
    # Set default selectors if not provided
    if file_path_selector is None:
        file_path_selector = r"text-sm text-zinc-400 mb-2 font-mono"
    if code_table_selector is None:
        code_table_selector = r"syntax-highlight"
    if code_line_selector is None:
        code_line_selector = r"line added"
    
    # Set default output directory if not provided
    if output_dir is None:
        output_dir = os.getcwd()
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Read HTML file
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
    except UnicodeDecodeError:
        # Try with different encoding if utf-8 fails
        try:
            with open(html_file_path, 'r', encoding='latin-1') as file:
                html_content = file.read()
            logger.warning(f"Fallback to latin-1 encoding for {html_file_path}")
        except Exception as e:
            logger.error(f"Error reading HTML file: {e}")
            return []
    except Exception as e:
        logger.error(f"Error reading HTML file: {e}")
        return []
    
    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all code blocks
    code_blocks = {}
    current_file = None
    
    # Find all elements with the file path class
    file_headers = soup.find_all(class_=re.compile(file_path_selector))
    
    if not file_headers:
        logger.warning(f"No file headers found with class '{file_path_selector}'. Check if the HTML structure matches the expected pattern.")
    
    for header in file_headers:
        # Extract file path from the header text
        file_path = header.get_text().strip()
        
        # Clean up the file path
        if file_path.endswith(':'):
            file_path = file_path[:-1]  # Remove trailing colon
        
        # Skip empty file paths
        if not file_path:
            continue
        
        current_file = file_path
        code_blocks[current_file] = []
        
        # Find the next table with the code table class
        table = header.find_next('table', class_=code_table_selector)
        if table:
            # Find all rows with the code line class
            added_lines = table.find_all('tr', class_=code_line_selector)
            
            for line in added_lines:
                # Extract code from the line
                code_text = line.get_text().strip()
                code_blocks[current_file].append(code_text)
    
    # Create files with extracted code
    files_created = []
    for file_path, code_lines in code_blocks.items():
        if not code_lines:
            continue
        
        # Create full path
        full_path = os.path.join(output_dir, file_path)
        
        try:
            # Create directory structure
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            # Write code to file
            with open(full_path, 'w', encoding='utf-8') as file:
                file.write('\n'.join(code_lines))
            
            files_created.append(file_path)
            logger.info(f"Created file: {file_path}")
        except Exception as e:
            logger.error(f"Error creating file {file_path}: {e}")
    
    return files_created

def main():
    parser = argparse.ArgumentParser(description='Extract code blocks from HTML files and create corresponding files.')
    parser.add_argument('html_file', help='Path to the HTML file')
    parser.add_argument('-o', '--output-dir', help='Directory to save extracted files. Defaults to current directory.')
    parser.add_argument('--file-path-selector', help='CSS selector for file paths. Defaults to "text-sm text-zinc-400 mb-2 font-mono".')
    parser.add_argument('--code-table-selector', help='CSS selector for code tables. Defaults to "syntax-highlight".')
    parser.add_argument('--code-line-selector', help='CSS selector for code lines. Defaults to "line added".')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Set logging level based on verbose flag
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Extract code from HTML file
    files_created = extract_code_from_html(
        args.html_file,
        args.output_dir,
        args.file_path_selector,
        args.code_table_selector,
        args.code_line_selector
    )
    
    # Print summary
    if files_created:
        print(f"Successfully extracted {len(files_created)} files.")
        if args.verbose:
            print("Files created:")
            for file_path in files_created:
                print(f"  - {file_path}")
    else:
        print("No files were created. Check if the HTML structure matches the expected pattern.")

if __name__ == "__main__":
    main()
