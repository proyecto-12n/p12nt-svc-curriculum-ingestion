"""
NextProject 2026

This file is part of the NP Collector Curriculum project.
Unauthorized copying of this file, via any medium is strictly prohibited.
"""

try:
    from app.infrastructure.adapter.external.pdf_converter.docling_pdf_converter import (
        DoclingPDFConverter,
    )
except ImportError:
    DoclingPDFConverter = None

try:
    from app.infrastructure.adapter.external.pdf_converter.pymupdf_pdf_converter import (
        PyMuPDFPDFConverter,
    )
except ImportError:
    PyMuPDFPDFConverter = None

__all__ = [
    "DoclingPDFConverter",
    "PyMuPDFPDFConverter",
]
