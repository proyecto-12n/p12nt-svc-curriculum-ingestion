# -*- coding: utf-8 -*-
"""
NextProject © 2026
"""

from typing import Protocol
from app.domain.model.pdf_resource import PDFResource


class PDFConverter(Protocol):
    def convert(self, resource: PDFResource) -> str:
        """
        Converts a PDFResource to markdown text.
        """
        ...
