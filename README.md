# Zeeeepa Tools

A collection of useful tools for various tasks.

## HTML Code Extractor

A powerful tool that extracts code blocks from HTML files and creates the corresponding file structure.

### Features

- **Simple CLI and GUI Interfaces**: Easy-to-use interfaces for selecting HTML files
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

## Installation

### From PyPI

```bash
pip install zeeeepa-tools
```

### From Source

```bash
git clone https://github.com/Zeeeepa/tools.git
cd tools
pip install -e .
```

## Usage

### Command Line Interface

```bash
# Basic usage
html-code-extractor path/to/html/file.html

# Specify output directory
html-code-extractor path/to/html/file.html -o /path/to/output/dir

# Preview files without creating them
html-code-extractor path/to/html/file.html -p

# Specify custom CSS selectors
html-code-extractor path/to/html/file.html --file-path-class "custom-file-path" --code-table-class "custom-table" --code-line-class "custom-line"

# Show help
html-code-extractor --help
```

### Graphical User Interface

```bash
# Launch the GUI
html-code-extractor-gui
```

### Python API

```python
from zeeeepa.tools.html_code_extractor import extract_code_from_html, preview_code_from_html

# Extract code from HTML file
files_created = extract_code_from_html(
    html_file_path="path/to/html/file.html",
    output_dir="path/to/output/dir",
    selectors={
        "file_path_class": "text-sm text-zinc-400 mb-2 font-mono",
        "code_table_class": "syntax-highlight",
        "code_line_class": "line added",
    },
    encoding="utf-8",
)

# Preview code from HTML file
code_blocks = preview_code_from_html(
    html_file_path="path/to/html/file.html",
    selectors={
        "file_path_class": "text-sm text-zinc-400 mb-2 font-mono",
        "code_table_class": "syntax-highlight",
        "code_line_class": "line added",
    },
    encoding="utf-8",
)
```

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/Zeeeepa/tools.git
cd tools

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Run Tests

```bash
pytest
```

### Run Linters

```bash
# Run flake8
flake8 src/ tests/

# Run mypy
mypy src/

# Run black
black src/ tests/

# Run isort
isort src/ tests/
```

## License

MIT
