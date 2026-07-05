from unittest.mock import MagicMock, patch

from domain.model.pdf_resource import PDFResource
from infrastructure.adapter.external.pdf_converter.impl.pymupdf_pdf_converter import (
    PyMuPDFPDFConverter,
)


class TestPyMuPDFPDFConverter:
    def test_given_pdf_resource_when_convert_then_returns_markdown(self):
        document = MagicMock()

        with (
            patch(
                "infrastructure.adapter.external.pdf_converter.impl.pymupdf_pdf_converter.Document",
                return_value=document,
            ) as document_class,
            patch(
                "infrastructure.adapter.external.pdf_converter.impl.pymupdf_pdf_converter.pymupdf4llm"
            ) as pymupdf4llm,
        ):
            pymupdf4llm.to_markdown.return_value = "markdown"
            result = PyMuPDFPDFConverter().convert(PDFResource(content=b"pdf"))

        assert result == "markdown"
        document_class.assert_called_once()
        pymupdf4llm.to_markdown.assert_called_once_with(
            document,
            header=False,
            use_ocr=False,
            show_progress=True,
            write_images=False,
        )
