from unittest.mock import MagicMock

from application.usecase.convert_pdf_to_markdown_usecase import (
    ConvertPDFToMarkdownUseCaseImpl,
)
from domain.model.pdf_resource import PDFResource


class TestConvertPDFToMarkdownUseCaseImpl:
    def setup_method(self):
        self.converter = MagicMock()
        self.converter.convert.return_value = "# Markdown"
        self.provider = MagicMock()
        self.provider.get_converter.return_value = self.converter
        self.use_case = ConvertPDFToMarkdownUseCaseImpl(self.provider)
        self.resource = PDFResource(content=b"pdf")

    async def test_given_uncached_pdf_when_execute_then_uses_provider_converter_and_returns_markdown(
        self,
    ):
        result = await self.use_case.execute(self.resource)

        assert result == "# Markdown"
        self.provider.get_converter.assert_called_once_with(None)
        self.converter.convert.assert_called_once_with(self.resource)

    async def test_given_same_pdf_when_execute_twice_then_second_call_uses_cache(self):
        await self.use_case.execute(self.resource)
        self.provider.get_converter.reset_mock()
        self.converter.convert.reset_mock()
        result = await self.use_case.execute(self.resource)

        assert result == "# Markdown"
        self.provider.get_converter.assert_not_called()
        self.converter.convert.assert_not_called()

    async def test_given_provider_name_when_execute_then_requests_named_converter(self):
        result = await self.use_case.execute(
            PDFResource(content=b"other"), provider_name="pymupdf"
        )

        assert result == "# Markdown"
        self.provider.get_converter.assert_called_once_with("pymupdf")
