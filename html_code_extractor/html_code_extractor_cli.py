#!/usr/bin/env python3
"""
HTML Code Extractor CLI - Command-line interface for HTML Code Extractor
This is a wrapper script that calls the enhanced version with CLI arguments.
"""
import sys
import os

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Import the enhanced version
sys.path.insert(0, script_dir)
from html_extractor_enhanced import main

if __name__ == "__main__":
    # Run the main function from the enhanced version
    main()
