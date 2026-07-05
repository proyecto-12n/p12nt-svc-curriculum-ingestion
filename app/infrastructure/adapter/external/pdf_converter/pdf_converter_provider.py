"""
NextProject 2026

This file is part of the NP Collector Curriculum project.
Unauthorized copying of this file, via any medium is strictly prohibited.
"""

import logging

from domain.port.outbound.pdf_converter import PDFConverter
from domain.port.outbound.pdf_converter_provider import (
    PDFConverterProvider as PDFConverterProviderPort,
)

logger = logging.getLogger(__name__)


class PDFConverterProvider(PDFConverterProviderPort):
    """
    Provider implementation that registers and provides PDF converters.
    """

    def get_converter(self, provider_name: str | None = None) -> PDFConverter:
        if provider_name is None:
            from app.config import settings

            provider_name = settings.pdf_converter

        name = provider_name.lower()
        if name == "pymupdf4llm":
            from infrastructure.adapter.external.pdf_converter.impl.pymupdf_pdf_converter import (
                PyMuPDFPDFConverter,
            )

            converter_class = PyMuPDFPDFConverter
        elif name == "markitdown":
            from infrastructure.adapter.external.pdf_converter.impl.markitdown_pdf_converter import (
                MarkItDownPDFConverter,
            )

            converter_class = MarkItDownPDFConverter
        else:
            raise ValueError(f"No PDF converter found with name: {provider_name}")

        logger.info(
            f"Using PDF converter: {converter_class.__name__} "
            f"(provider name: {provider_name})"
        )
        return converter_class()
