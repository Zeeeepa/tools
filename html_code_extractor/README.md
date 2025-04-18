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

### Basic Version

1. Run the basic script:
   ```
   python html_extractor.py
   ```

2. Use the GUI to:
   - Click "Browse..." to select your HTML file
   - The output directory is automatically set to "WEB-CODES" on your desktop
   - Click "Extract Code" to start the extraction process

### Enhanced Version

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

3. Check the "WEB-CODES" folder on your desktop for the extracted files

## How It Works

The tool works by:

1. Parsing the HTML file using BeautifulSoup
2. Finding all elements with class "text-sm text-zinc-400 mb-2 font-mono" which contain file paths
3. For each file path, finding the associated code blocks with class "line added"
4. Creating the necessary directory structure and files with the extracted code

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
