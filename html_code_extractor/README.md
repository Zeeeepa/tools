# HTML Code Extractor

A simple GUI tool that extracts code blocks from HTML files and creates the corresponding file structure.

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

1. Run the script:
   ```
   python html_extractor.py
   ```

2. Use the GUI to:
   - Click "Browse..." to select your HTML file
   - The output directory is automatically set to "WEB-CODES" on your desktop
   - Click "Extract Code" to start the extraction process

3. Check the "WEB-CODES" folder on your desktop for the extracted files

## How It Works

The tool works by:

1. Parsing the HTML file using BeautifulSoup
2. Finding all elements with class "text-sm text-zinc-400 mb-2 font-mono" which contain file paths
3. For each file path, finding the associated code blocks with class "line added"
4. Creating the necessary directory structure and files with the extracted code

## Customization

If you need to extract code from HTML files with a different structure, you can modify these parts of the script:

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
