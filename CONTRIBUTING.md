# Contributing to Zeeeepa Tools

Thank you for considering contributing to Zeeeepa Tools! This document provides guidelines and instructions for contributing to this project.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We aim to foster an inclusive and welcoming community.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with the following information:

- A clear, descriptive title
- A detailed description of the bug
- Steps to reproduce the bug
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment information (OS, Python version, etc.)

### Suggesting Features

If you have an idea for a new feature, please create an issue on GitHub with the following information:

- A clear, descriptive title
- A detailed description of the feature
- Why the feature would be useful
- Any implementation ideas you have

### Pull Requests

1. Fork the repository
2. Create a new branch for your changes
3. Make your changes
4. Run tests and linters to ensure your changes don't break anything
5. Submit a pull request

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Zeeeepa/tools.git
   cd tools
   ```

2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

3. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Code Style

We follow the [Black](https://black.readthedocs.io/en/stable/) code style. Please ensure your code is formatted with Black before submitting a pull request.

We also use:
- [isort](https://pycqa.github.io/isort/) for sorting imports
- [flake8](https://flake8.pycqa.org/en/latest/) for linting
- [mypy](https://mypy.readthedocs.io/en/stable/) for type checking

You can run all of these tools with the pre-commit hooks:
```bash
pre-commit run --all-files
```

## Testing

Please write tests for any new features or bug fixes. We use [pytest](https://docs.pytest.org/en/stable/) for testing.

Run tests with:
```bash
pytest
```

## Documentation

Please update the documentation when adding or modifying features. This includes:

- Docstrings for new functions, classes, and methods
- Updates to the README.md file
- Updates to the CHANGELOG.md file

## Versioning

We use [Semantic Versioning](https://semver.org/). Please update the version number in setup.py according to the following rules:

- MAJOR version when you make incompatible API changes
- MINOR version when you add functionality in a backwards compatible manner
- PATCH version when you make backwards compatible bug fixes

## License

By contributing to this project, you agree that your contributions will be licensed under the project's MIT license.
