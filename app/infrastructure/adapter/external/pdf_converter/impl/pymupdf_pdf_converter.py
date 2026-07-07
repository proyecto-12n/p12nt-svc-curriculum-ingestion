"""
NextProject 2026

This file is part of the NP Collector Curriculum project.
Unauthorized copying of this file, via any medium is strictly prohibited.
"""

from io import BytesIO
from pathlib import PurePosixPath
from urllib.parse import urlparse

from fitz import Document
import pymupdf4llm
from domain.port.outbound.pdf_converter import PDFConverter
from domain.model.pdf_resource import PDFResource
from app.utils import log_execution_time


class PyMuPDFPDFConverter(PDFConverter):
    """
    Concrete implementation of PDFConverter using the pymupdf4llm library.
    """

    @log_execution_time
    def convert(self, resource: PDFResource) -> str:
        doc = Document(stream=BytesIO(resource.content), filetype="pdf")
        chunks = pymupdf4llm.to_markdown(
            doc,
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
        return self._with_page_metadata(chunks, resource.source_name)

    def _with_page_metadata(self, chunks, source_name: str) -> str:
        source = self._source_basename(source_name)
        if isinstance(chunks, str):
            return f"<!-- source: {source} | page: 1 -->\n\n{chunks}"

        pages = []
        for index, chunk in enumerate(chunks, start=1):
            text = chunk.get("text", "") if isinstance(chunk, dict) else str(chunk)
            pages.append(f"<!-- source: {source} | page: {index} -->\n\n{text}")
        return "\n\n".join(pages)

    def _source_basename(self, source_name: str) -> str:
        path = urlparse(source_name).path or source_name
        return PurePosixPath(path).name or source_name
