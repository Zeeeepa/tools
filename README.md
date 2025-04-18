# Zeeeepa Tools

[![Python Package](https://github.com/Zeeeepa/tools/actions/workflows/python-package.yml/badge.svg)](https://github.com/Zeeeepa/tools/actions/workflows/python-package.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A collection of useful tools for developers.

## Tools

### HTML Code Extractor

A powerful GUI tool that extracts code blocks from HTML files and creates the corresponding file structure.

#### Features

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

### HTML Code Extractor

#### Command Line

```bash
html-extractor --help
```

#### As a Python Module

```python
from zeeeepa.tools.html_code_extractor import extract_code_from_html

# Extract code from an HTML file
files_created = extract_code_from_html(
    html_file_path="path/to/file.html",
    output_dir="path/to/output",
    selectors={
        "file_path_class": "text-sm text-zinc-400 mb-2 font-mono",
        "code_table_class": "syntax-highlight",
        "code_line_class": "line added"
    },
    encoding="utf-8"
)

print(f"Created {len(files_created)} files")
```

#### GUI Application

```bash
html-extractor-gui
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/Zeeeepa/tools.git
cd tools

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Testing

```bash
pytest
```

### Linting

```bash
# Run all linters
pre-commit run --all-files

# Run individual linters
black .
isort .
flake8 .
mypy .
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
