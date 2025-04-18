# HTML Code Extractor v2

A powerful GUI tool that extracts code blocks from HTML files and creates the corresponding file structure. This version is specifically designed to work with HTML files that have code blocks marked with the class "line added" and file paths identified by the class "text-sm text-zinc-400 mb-2 font-mono".

## Overview

This tool is designed to extract code blocks from HTML files that have a specific structure, particularly those with code blocks marked with the class "line added" and file paths identified by the class "text-sm text-zinc-400 mb-2 font-mono".

It's perfect for extracting code examples from documentation, tutorials, or any HTML page that contains structured code blocks.

## Features

- **Enhanced GUI Interface**: User-friendly tabbed interface for better organization
- **Automatic Output Directory**: Creates a "WEB-CODES" folder on your desktop by default
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

### HTML Code Extractor v2

1. Run the script:
   ```
   python html_code_extractor_v2.py
   ```

2. Use the GUI to:
   - **Extract Tab**: Select HTML files, set output directory, and choose encoding
   - **Settings Tab**: Customize CSS selectors for file paths, code tables, and code lines
   - **Preview Tab**: Preview files before extraction
   - Click "Preview" to see what will be extracted without creating files
   - Click "Extract Code" to create the files

## How It Works

The tool works by:

1. Parsing the HTML file using BeautifulSoup
2. Finding all elements with class "text-sm text-zinc-400 mb-2 font-mono" which contain file paths
3. For each file path, finding the associated code blocks with class "line added"
4. Creating the necessary directory structure and files with the extracted code

## Customization

You can customize the CSS selectors directly in the UI:

1. Go to the "Settings" tab
2. Modify the selectors for file paths, code tables, and code lines
3. Click "Save Settings" to save your changes

Default selectors:
- File Path Class: `text-sm text-zinc-400 mb-2 font-mono`
- Code Table Class: `syntax-highlight`
- Code Line Class: `line added`

## Requirements

- Python 3.6 or higher
- BeautifulSoup4 (`pip install beautifulsoup4`)
- Tkinter (included with most Python installations)

## License

MIT
