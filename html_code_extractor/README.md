# HTML Code Extractor

A powerful GUI tool that extracts code blocks from HTML files and creates the corresponding file structure.

## Overview

This tool is designed to extract code blocks from HTML files that have a specific structure, particularly those with code blocks marked with the class "line added" and file paths identified by the class "text-sm text-zinc-400 mb-2 font-mono".

It's perfect for extracting code examples from documentation, tutorials, or any HTML page that contains structured code blocks.

## Tools Included

This package includes three main tools:

1. **HTML Code Extractor (Basic)**: Simple tool for extracting code from HTML files
2. **HTML Code Extractor (Enhanced)**: Advanced tool with more features and customization options
   - Now includes a tabbed interface with extraction, settings, and preview tabs
   - Supports command-line usage with customizable CSS selectors
   - Specifically designed for HTML files with code blocks marked with the class "line added" and file paths identified by the class "text-sm text-zinc-400 mb-2 font-mono"
3. **HTML Code Saver**: Tool for saving HTML files with metadata for later extraction
4. **HTML Archive Extractor**: Tool for extracting code from saved HTML archives

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

### HTML Code Extractor (Basic)

1. Run the basic script:
   ```
   python html_extractor.py
   ```

2. Use the GUI to:
   - Click "Browse..." to select your HTML file
   - The output directory is automatically set to "WEB-CODES" on your desktop
   - Click "Extract Code" to start the extraction process

### HTML Code Extractor (Enhanced)

1. Run the enhanced script:
   ```
   python html_extractor_enhanced.py
   ```

2. Use the GUI to:
   - **Extract Tab**: Select HTML files, set output directory, and choose encoding
   - **Settings Tab**: Customize CSS selectors for file paths, code tables, and code lines
   - **Preview Tab**: Preview files before extraction
   - Click "Preview" to see what will be extracted without creating files
   - Click "Extract Code" to create the files

3. Command-line usage:
   ```
   python html_extractor_enhanced.py path/to/your/file.html -o output/directory
   ```

   Available options:
   ```
   usage: html_extractor_enhanced.py [-h] [-o OUTPUT_DIR] [--file-path-selector FILE_PATH_SELECTOR]
                                [--code-table-selector CODE_TABLE_SELECTOR]
                                [--code-line-selector CODE_LINE_SELECTOR] [-v] [--v2]
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
     --v2                  Use the v2 interface
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

## Features

- **Code Extraction**: Extract code blocks from HTML files
- **File Structure Creation**: Create the corresponding file structure based on file paths in the HTML
- **Customizable Selectors**: Configure CSS selectors to match different HTML structures
- **Preview Mode**: Preview files before extraction
- **Multiple Encodings**: Support for different file encodings
- **Progress Tracking**: Real-time progress bar during extraction
- **Multi-threaded**: Background processing keeps the UI responsive
- **Command-line Interface**: Use the tools from the command line for automation
- **Tabbed Interface**: Enhanced version includes tabs for extraction, settings, and preview

## Requirements

- Python 3.6 or higher
- BeautifulSoup4 (`pip install beautifulsoup4`)
- Tkinter (included with most Python installations)

## License

MIT
