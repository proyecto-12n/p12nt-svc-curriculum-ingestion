# -*- coding: utf-8 -*-
"""
NextProject © 2026
"""

from typing import Protocol
from app.domain.port.outbound.pdf_converter import PDFConverter


class PDFConverterProvider(Protocol):
    def get_converter(self, provider_name: str) -> PDFConverter:
        """
        Retrieves a PDFConverter implementation by provider name.
        """
        ...
