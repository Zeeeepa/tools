# Contributing to Zeeeepa Tools

Thank you for considering contributing to Zeeeepa Tools! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project.

## How to Contribute

1. Fork the repository
2. Create a new branch for your feature or bugfix
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## Development Environment Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/tools.git
cd tools

# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## Code Style

This project uses:
- [Black](https://github.com/psf/black) for code formatting
- [isort](https://github.com/PyCQA/isort) for import sorting
- [flake8](https://github.com/PyCQA/flake8) for linting
- [mypy](https://github.com/python/mypy) for type checking

Before submitting a pull request, please run:

```bash
# Format code
black .
isort .

# Check code
flake8 .
mypy .

# Or run all checks with pre-commit
pre-commit run --all-files
```

## Testing

Please add tests for any new features or bug fixes. Run the tests with:

```bash
pytest
```

## Pull Request Process

1. Update the README.md with details of changes if appropriate
2. Update the CHANGELOG.md with details of changes
3. The PR should work for Python 3.7 and above
4. Ensure all tests pass and code style checks pass
5. Your PR will be reviewed by maintainers

## Documentation

Please update documentation when necessary. This includes:
- Code docstrings
- README.md
- Other documentation files

## Reporting Bugs

When reporting bugs, please include:
- A clear and descriptive title
- Steps to reproduce the bug
- Expected behavior
- Actual behavior
- Screenshots if applicable
- Your environment (OS, Python version, etc.)

## Feature Requests

Feature requests are welcome. Please provide:
- A clear and descriptive title
- A detailed description of the proposed feature
- Any relevant examples or use cases

## Questions?

If you have any questions, please open an issue with the "question" label.
