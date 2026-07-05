"""
NextProject 2026

This file is part of the NP Collector Curriculum project.
Unauthorized copying of this file, via any medium is strictly prohibited.
"""

try:
    from infrastructure.adapter.external.pdf_converter.impl.pymupdf_pdf_converter import (
        PyMuPDFPDFConverter,
    )
except ImportError:
    PyMuPDFPDFConverter = None

try:
    from infrastructure.adapter.external.pdf_converter.impl.markitdown_pdf_converter import (
        MarkItDownPDFConverter,
    )
except ImportError:
    MarkItDownPDFConverter = None

__all__ = [
    "MarkItDownPDFConverter",
    "PyMuPDFPDFConverter",
]
