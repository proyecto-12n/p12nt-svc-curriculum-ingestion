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
            pymupdf4llm.to_markdown.return_value = [{"text": "## Unidad 1"}]
            result = PyMuPDFPDFConverter().convert(
                PDFResource(
                    content=b"pdf",
                    source_name="https://example.cl/articles-20710_programa.pdf",
                )
            )

        assert (
            result == "<!-- source: articles-20710_programa.pdf | page: 1 -->\n\n"
            "## Unidad 1"
        )
        document_class.assert_called_once()
        pymupdf4llm.to_markdown.assert_called_once_with(
            document,
            page_chunks=True,
            header=False,
            footer=False,
            use_ocr=True,
            force_ocr=False,
            ocr_language="spa",
            page_separators=True,
            table_strategy="lines_strict",
            show_progress=True,
            write_images=False,
        )

    def test_given_string_markdown_when_convert_then_adds_source_metadata(self):
        document = MagicMock()

        with (
            patch(
                "infrastructure.adapter.external.pdf_converter.impl.pymupdf_pdf_converter.Document",
                return_value=document,
            ),
            patch(
                "infrastructure.adapter.external.pdf_converter.impl.pymupdf_pdf_converter.pymupdf4llm"
            ) as pymupdf4llm,
        ):
            pymupdf4llm.to_markdown.return_value = "# Program"
            result = PyMuPDFPDFConverter().convert(
                PDFResource(content=b"pdf", source_name="programa.pdf")
            )

        assert result == "<!-- source: programa.pdf | page: 1 -->\n\n# Program"

    def test_given_multiple_page_chunks_when_convert_then_keeps_page_order(self):
        document = MagicMock()

        with (
            patch(
                "infrastructure.adapter.external.pdf_converter.impl.pymupdf_pdf_converter.Document",
                return_value=document,
            ),
            patch(
                "infrastructure.adapter.external.pdf_converter.impl.pymupdf_pdf_converter.pymupdf4llm"
            ) as pymupdf4llm,
        ):
            pymupdf4llm.to_markdown.return_value = [
                {"text": "page one"},
                {"text": "page two"},
            ]
            result = PyMuPDFPDFConverter().convert(
                PDFResource(content=b"pdf", source_name="/tmp/mineduc.pdf")
            )

        assert result == (
            "<!-- source: mineduc.pdf | page: 1 -->\n\n"
            "page one\n\n"
            "<!-- source: mineduc.pdf | page: 2 -->\n\n"
            "page two"
        )

    def test_given_non_dict_chunk_when_convert_then_casts_chunk_to_text(self):
        document = MagicMock()

        with (
            patch(
                "infrastructure.adapter.external.pdf_converter.impl.pymupdf_pdf_converter.Document",
                return_value=document,
            ),
            patch(
                "infrastructure.adapter.external.pdf_converter.impl.pymupdf_pdf_converter.pymupdf4llm"
            ) as pymupdf4llm,
        ):
            pymupdf4llm.to_markdown.return_value = ["plain page"]
            result = PyMuPDFPDFConverter().convert(
                PDFResource(content=b"pdf", source_name="folder/programa.pdf")
            )

        assert result == "<!-- source: programa.pdf | page: 1 -->\n\nplain page"

    def test_given_empty_source_name_when_convert_then_uses_original_source(self):
        document = MagicMock()

        with (
            patch(
                "infrastructure.adapter.external.pdf_converter.impl.pymupdf_pdf_converter.Document",
                return_value=document,
            ),
            patch(
                "infrastructure.adapter.external.pdf_converter.impl.pymupdf_pdf_converter.pymupdf4llm"
            ) as pymupdf4llm,
        ):
            pymupdf4llm.to_markdown.return_value = "# Program"
            result = PyMuPDFPDFConverter().convert(
                PDFResource(content=b"pdf", source_name="")
            )

        assert result == "<!-- source:  | page: 1 -->\n\n# Program"
