#!/usr/bin/env python3
"""
HTML Code Extractor v2 - Enhanced version with tabbed interface
This is a wrapper script that calls the enhanced version with the v2 flag.
"""
import sys
import os

# Get the directory of this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Import the enhanced version
sys.path.insert(0, script_dir)
import html_extractor_enhanced

if __name__ == "__main__":
    # Add the v2 flag to the command line arguments
    if len(sys.argv) == 1:
        sys.argv.append("--v2")
    else:
        sys.argv.append("--v2")
    
    # Run the main function from the enhanced version
    html_extractor_enhanced.main()
