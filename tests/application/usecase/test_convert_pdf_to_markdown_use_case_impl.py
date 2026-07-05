from unittest.mock import MagicMock

from application.usecase.convert_pdf_to_markdown_usecase import (
    ConvertPDFToMarkdownUseCaseImpl,
)
from domain.model.pdf_resource import PDFResource


class TestConvertPDFToMarkdownUseCaseImpl:
    async def test_given_uncached_pdf_when_execute_then_uses_provider_converter_and_returns_markdown(
        self,
    ):
        converter = MagicMock()
        converter.convert.return_value = "# Markdown"
        provider = MagicMock()
        provider.get_converter.return_value = converter
        use_case = ConvertPDFToMarkdownUseCaseImpl(provider)
        resource = PDFResource(content=b"pdf")

        result = await use_case.execute(resource)

        assert result == "# Markdown"
        provider.get_converter.assert_called_once_with(None)
        converter.convert.assert_called_once_with(resource)

    async def test_given_same_pdf_when_execute_twice_then_second_call_uses_cache(self):
        converter = MagicMock()
        converter.convert.return_value = "# Markdown"
        provider = MagicMock()
        provider.get_converter.return_value = converter
        use_case = ConvertPDFToMarkdownUseCaseImpl(provider)
        resource = PDFResource(content=b"pdf")

        await use_case.execute(resource)
        provider.get_converter.reset_mock()
        converter.convert.reset_mock()
        result = await use_case.execute(resource)

        assert result == "# Markdown"
        provider.get_converter.assert_not_called()
        converter.convert.assert_not_called()

    async def test_given_provider_name_when_execute_then_requests_named_converter(self):
        converter = MagicMock()
        converter.convert.return_value = "# Markdown"
        provider = MagicMock()
        provider.get_converter.return_value = converter
        use_case = ConvertPDFToMarkdownUseCaseImpl(provider)

        result = await use_case.execute(
            PDFResource(content=b"other"), provider_name="pymupdf"
        )

        assert result == "# Markdown"
        provider.get_converter.assert_called_once_with("pymupdf")
