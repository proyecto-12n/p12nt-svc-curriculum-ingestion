# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from unittest.mock import MagicMock
import pytest

from application.usecase.convert_pdf_to_markdown_usecase import (
    ConvertPDFToMarkdownUseCaseImpl,
)
from domain.model.pdf_resource import PDFResource


@pytest.mark.asyncio
async def test_convert_pdf_to_markdown_basic_and_caching():
    # Arrange
    mock_converter = MagicMock()
    mock_converter.convert.return_value = "# Markdown Content"

    mock_provider = MagicMock()
    mock_provider.get_converter.return_value = mock_converter

    usecase = ConvertPDFToMarkdownUseCaseImpl(mock_provider)
    pdf_resource = PDFResource(content=b"Sample PDF bytes")

    # Act - First call (Cache Miss)
    markdown_1 = await usecase.execute(pdf_resource)

    # Assert - First call
    assert markdown_1 == "# Markdown Content"
    mock_provider.get_converter.assert_called_once_with(None)
    mock_converter.convert.assert_called_once_with(pdf_resource)

    # Reset mock call counters to verify second call behavior
    mock_provider.get_converter.reset_mock()
    mock_converter.convert.reset_mock()

    # Act - Second call with identical content (Cache Hit)
    markdown_2 = await usecase.execute(pdf_resource)

    # Assert - Second call
    assert markdown_2 == "# Markdown Content"
    mock_provider.get_converter.assert_not_called()
    mock_converter.convert.assert_not_called()


@pytest.mark.asyncio
async def test_convert_pdf_to_markdown_with_provider_name():
    # Arrange
    mock_converter = MagicMock()
    mock_converter.convert.return_value = "# Spec Markdown"

    mock_provider = MagicMock()
    mock_provider.get_converter.return_value = mock_converter

    usecase = ConvertPDFToMarkdownUseCaseImpl(mock_provider)
    pdf_resource = PDFResource(content=b"Different bytes")

    # Act
    markdown = await usecase.execute(pdf_resource, provider_name="pymupdf")

    # Assert
    assert markdown == "# Spec Markdown"
    mock_provider.get_converter.assert_called_once_with("pymupdf")
    mock_converter.convert.assert_called_once_with(pdf_resource)
