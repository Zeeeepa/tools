# HTML Code Extractor

A powerful GUI tool that extracts code blocks from HTML files and creates the corresponding file structure.

## Overview

This tool is designed to extract code blocks from HTML files that have a specific structure, particularly those with code blocks marked with the class "line added" and file paths identified by the class "text-sm text-zinc-400 mb-2 font-mono".

It's perfect for extracting code examples from documentation, tutorials, or any HTML page that contains structured code blocks.

## Features

- **Simple GUI Interface**: Easy-to-use interface for selecting HTML files
- **Automatic Output Directory**: Creates a "WEB-CODES" folder on your desktop
- **Code Extraction**: Extracts code blocks with class "line added" from the HTML file
- **File Structure Creation**: Creates the corresponding file structure based on file paths in the HTML
- **Status Updates**: Shows the status of the extraction process
- **Error Handling**: Provides error messages for common issues
- **Preview Mode**: Preview files before extraction
- **Custom Settings**: Configure CSS selectors to match different HTML structures
- **Multiple Encodings**: Support for different file encodings
- **Progress Tracking**: Real-time progress bar during extraction
- **Multi-threaded**: Background processing keeps the UI responsive
- **Supports both .html and .htm files**: Works with all HTML file extensions
- **Archive Support**: Save HTML files for later extraction with metadata

## Tools Included

This package includes five main tools:

1. **HTML Code Extractor (Basic)**: Simple tool for extracting code from HTML files
2. **HTML Code Extractor (Enhanced)**: Advanced tool with more features and customization options
3. **HTML Code Extractor v2**: New version specifically designed for HTML files with code blocks marked with the class "line added" and file paths identified by the class "text-sm text-zinc-400 mb-2 font-mono"
4. **HTML Code Extractor CLI**: Command-line version of the HTML Code Extractor v2
5. **HTML Code Saver**: Tool for saving HTML files with metadata for later extraction
6. **HTML Archive Extractor**: Tool for extracting code from saved HTML archives

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/Zeeeepa/tools.git
   cd tools/html_code_extractor
   ```

2. Install the required dependencies:
   ```
   pip install beautifulsoup4
   ```

## Usage

### Basic HTML Code Extractor

1. Run the basic script:
   ```
   python html_extractor.py
   ```

2. Use the GUI to:
   - Click "Browse..." to select your HTML file
   - The output directory is automatically set to "WEB-CODES" on your desktop
   - Click "Extract Code" to start the extraction process

### Enhanced HTML Code Extractor

1. Run the enhanced script:
   ```
   python html_extractor_enhanced.py
   ```

2. Use the enhanced GUI with additional features:
   - **Extract Tab**: Select HTML files, set output directory, and choose encoding
   - **Settings Tab**: Customize CSS selectors and UI settings
   - **Preview Tab**: Preview files before extraction
   - Click "Preview" to see what will be extracted without creating files
   - Click "Extract Code" to create the files

### HTML Code Extractor v2

1. Run the v2 script:
   ```
   python html_code_extractor_v2.py
   ```

2. Use the GUI to:
   - **Extract Tab**: Select HTML files, set output directory, and choose encoding
   - **Settings Tab**: Customize CSS selectors for file paths, code tables, and code lines
   - **Preview Tab**: Preview files before extraction
   - Click "Preview" to see what will be extracted without creating files
   - Click "Extract Code" to create the files

### HTML Code Extractor CLI

1. Run the CLI script:
   ```
   python html_code_extractor_cli.py path/to/your/file.html -o output/directory
   ```

2. Available options:
   ```
   usage: html_code_extractor_cli.py [-h] [-o OUTPUT_DIR] [--file-path-selector FILE_PATH_SELECTOR]
                                  [--code-table-selector CODE_TABLE_SELECTOR]
                                  [--code-line-selector CODE_LINE_SELECTOR] [-v]
                                  html_file

   Extract code blocks from HTML files and create corresponding files.

   positional arguments:
     html_file             Path to the HTML file

   optional arguments:
     -h, --help            show this help message and exit
     -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                           Directory to save extracted files. Defaults to current directory.
     --file-path-selector FILE_PATH_SELECTOR
                           CSS selector for file paths. Defaults to "text-sm text-zinc-400 mb-2 font-mono".
     --code-table-selector CODE_TABLE_SELECTOR
                           CSS selector for code tables. Defaults to "syntax-highlight".
     --code-line-selector CODE_LINE_SELECTOR
                           CSS selector for code lines. Defaults to "line added".
     -v, --verbose         Enable verbose output
   ```

### HTML Code Saver

1. Run the HTML Code Saver:
   ```
   python html_code_saver.py
   ```

2. Use the GUI to:
   - Click "Browse..." to select your HTML file
   - Set the archive location (defaults to "HTML-ARCHIVES" on your desktop)
   - Optionally provide a custom archive name
   - Click "Generate Preview" to see what files will be extracted
   - Click "Save Archive" to save the HTML file with metadata for later extraction

### HTML Archive Extractor

1. Run the HTML Archive Extractor:
   ```
   python html_archive_extractor.py
   ```

2. Use the GUI to:
   - Browse and select a previously saved HTML archive
   - View information about the archive, including a preview of extractable files
   - Set the output directory for extracted files
   - Click "Extract Code" to extract the code from the archive

## How It Works

The tool works by:

1. Parsing the HTML file using BeautifulSoup
2. Finding all elements with class "text-sm text-zinc-400 mb-2 font-mono" which contain file paths
3. For each file path, finding the associated code blocks with class "line added"
4. Creating the necessary directory structure and files with the extracted code

## Saving for Later Extraction

The HTML Code Saver creates a self-contained archive that includes:

1. The original HTML file
2. A metadata.json file with information about the HTML file and extraction settings
3. A preview.txt file showing what files will be extracted

This allows you to save HTML files for later extraction, even if the original HTML file is modified or deleted.

## Customization

The enhanced version allows you to customize the CSS selectors directly in the UI:

1. Go to the "Settings" tab
2. Modify the selectors for file paths, code tables, and code lines
3. Click "Save Settings" to save your changes

For the basic version, you can modify these parts of the script:

1. To change the file path identifier class:
   ```python
   file_headers = soup.find_all(class_=re.compile(r"text-sm text-zinc-400 mb-2 font-mono"))
   ```

2. To change the code block identifier class:
   ```python
   added_lines = table.find_all('tr', class_='line added')
   ```

## Requirements

- Python 3.6 or higher
- BeautifulSoup4 (`pip install beautifulsoup4`)
- Tkinter (included with most Python installations)

## License

MIT
