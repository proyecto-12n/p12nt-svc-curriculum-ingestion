from unittest.mock import MagicMock, patch

from domain.model.pdf_resource import PDFResource
from infrastructure.adapter.external.pdf_converter.impl.markitdown_pdf_converter import (
    MarkItDownPDFConverter,
)


class TestMarkItDownPDFConverter:
    def test_given_pdf_resource_when_convert_then_returns_markdown(self):
        markitdown = MagicMock()
        markitdown.convert_stream.return_value.markdown = "markdown"

        with patch(
            "infrastructure.adapter.external.pdf_converter.impl.markitdown_pdf_converter.MarkItDown",
            return_value=markitdown,
        ):
            converter = MarkItDownPDFConverter()
            result = converter.convert(PDFResource(content=b"pdf"))

        assert result == "markdown"
        markitdown.convert_stream.assert_called_once()
