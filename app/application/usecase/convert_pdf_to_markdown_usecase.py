# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import asyncio
from hashlib import sha256
from typing import Dict

from app.domain.model.pdf_resource import PDFResource
from app.domain.port.inbound.convert_pdf_to_markdown_use_case import (
    ConvertPDFToMarkdownUseCase,
)
from app.domain.port.outbound.pdf_converter_provider import PDFConverterProvider


class ConvertPDFToMarkdownUseCaseImpl(ConvertPDFToMarkdownUseCase):
    """
    Concrete implementation of ConvertPDFToMarkdownUseCase with in-memory caching.
    """

    def __init__(self, pdf_converter_provider: PDFConverterProvider):
        self._pdf_converter_provider = pdf_converter_provider
        self._cache: Dict[str, str] = {}

    async def execute(
        self, resource: PDFResource, provider_name: str | None = None
    ) -> str:
        # Calculate SHA-256 of the content to act as the cache key
        checksum = sha256(resource.content).hexdigest()

        if checksum in self._cache:
            return self._cache[checksum]

        # Retrieve the specific PDFConverter from the provider
        converter = self._pdf_converter_provider.get_converter(provider_name)

        # Offload CPU-bound converter to a threadpool to remain asynchronous
        markdown = await asyncio.to_thread(converter.convert, resource)

        # Cache the result
        self._cache[checksum] = markdown
        return markdown
