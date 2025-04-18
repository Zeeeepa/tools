#!/usr/bin/env python3
"""Setup script for zeeeepa-tools."""

from setuptools import setup, find_namespace_packages

setup(
    name="zeeeepa-tools",
    version="0.1.0",
    description="A collection of useful tools for developers",
    author="Zeeeepa",
    author_email="info@zeeeepa.com",
    url="https://github.com/Zeeeepa/tools",
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.7",
    install_requires=[
        "beautifulsoup4>=4.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=21.5b2",
            "isort>=5.9.1",
            "mypy>=0.812",
            "flake8>=3.9.2",
            "pre-commit>=2.13.0",
            "pytest-cov>=2.12.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "html-extractor=zeeeepa.tools.html_code_extractor.cli:main",
            "html-extractor-gui=zeeeepa.tools.html_code_extractor.gui:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
