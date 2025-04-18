#!/usr/bin/env python3
"""Setup script for the zeeeepa.tools package."""

from setuptools import find_namespace_packages, setup

setup(
    name="zeeeepa-tools",
    version="0.1.0",
    description="A collection of useful tools for various tasks",
    author="Zeeeepa",
    author_email="info@zeeeepa.com",
    url="https://github.com/Zeeeepa/tools",
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    install_requires=[
        "beautifulsoup4>=4.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.10.0",
            "black>=20.8b1",
            "flake8>=3.8.0",
            "mypy>=0.800",
            "isort>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "html-code-extractor=zeeeepa.tools.html_code_extractor.cli:main",
            "html-code-extractor-gui=zeeeepa.tools.html_code_extractor.gui:main",
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
    python_requires=">=3.7",
)
