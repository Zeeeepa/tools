"""HTML Code Extractor package."""

from zeeeepa.tools.html_code_extractor.extractor import (
    extract_code_from_html,
    preview_code_from_html,
    HTMLParsingError,
    FileCreationError,
)

__all__ = [
    "extract_code_from_html",
    "preview_code_from_html",
    "HTMLParsingError",
    "FileCreationError",
]
