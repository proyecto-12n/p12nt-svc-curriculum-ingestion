import pytest

from infrastructure.adapter.external.pdf_converter.pdf_converter_provider import (
    PDFConverterProvider,
)
from infrastructure.adapter.external.pdf_converter.impl.markitdown_pdf_converter import (
    MarkItDownPDFConverter,
)
from infrastructure.adapter.external.pdf_converter.impl.pymupdf_pdf_converter import (
    PyMuPDFPDFConverter,
)


class TestPDFConverterProvider:
    def setup_method(self):
        self.provider = PDFConverterProvider()

    def test_given_pymupdf_name_when_get_converter_then_returns_pymupdf_converter(self):
        assert isinstance(
            self.provider.get_converter("pymupdf4llm"), PyMuPDFPDFConverter
        )

    def test_given_markitdown_name_when_get_converter_then_returns_markitdown_converter(
        self,
    ):
        assert isinstance(
            self.provider.get_converter("markitdown"), MarkItDownPDFConverter
        )

    def test_given_unknown_name_when_get_converter_then_raises_value_error(self):
        with pytest.raises(ValueError, match="No PDF converter found"):
            self.provider.get_converter("unknown")
