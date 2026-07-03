# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Protocol
from app.domain.model.pdf_resource import PDFResource


class ConvertPDFToMarkdownUseCase(Protocol):
    """
    Inbound port (Use Case) definition for converting a PDFResource to Markdown.
    """

    async def execute(
        self, resource: PDFResource, provider_name: str | None = None
    ) -> str:
        """
        Converts the given PDFResource to Markdown text.
        Returns cached results if the PDF content has been processed previously.
        """
        ...
