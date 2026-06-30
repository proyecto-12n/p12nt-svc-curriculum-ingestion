"""
NextProject 2026

This file is part of the NP Collector Curriculum project.
Unauthorized copying of this file, via any medium is strictly prohibited.
"""

import logging

from app.domain.port.outbound.pdf_converter import PDFConverter
from app.domain.port.outbound.pdf_converter_provider import (
    PDFConverterProvider as PDFConverterProviderPort,
)
from app.infrastructure.adapter.external.pdf_converter.markitdown_pdf_converter import (
    MarkItDownPDFConverter,
)
from app.infrastructure.adapter.external.pdf_converter.docling_pdf_converter import (
    DoclingPDFConverter,
)
from app.infrastructure.adapter.external.pdf_converter.pymupdf_pdf_converter import (
    PyMuPDFPDFConverter,
)

logger = logging.getLogger(__name__)


class PDFConverterProvider(PDFConverterProviderPort):
    """
    Provider implementation that registers and provides PDF converters.
    """

    def __init__(self):
        self._converters = {
            "docling": DoclingPDFConverter,
            "markitdown": MarkItDownPDFConverter,
            "pymupdf4llm": PyMuPDFPDFConverter,
        }

    def get_converter(self, provider_name: str) -> PDFConverter:
        converter = self._converters.get(provider_name.lower())
        if not converter:
            raise ValueError(f"No PDF converter found with name: {provider_name}")
        logger.info(
            f"Using PDF converter: {converter.__class__.__name__} "
            f"(provider name: {provider_name})"
        )
        return converter()
