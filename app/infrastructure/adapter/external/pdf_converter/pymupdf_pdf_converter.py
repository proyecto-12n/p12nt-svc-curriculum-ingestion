"""
NextProject 2026

This file is part of the NP Collector Curriculum project.
Unauthorized copying of this file, via any medium is strictly prohibited.
"""

from io import BytesIO
from fitz import Document
import pymupdf4llm
from app.domain.port.outbound.pdf_converter import PDFConverter
from app.domain.model.pdf_resource import PDFResource
from app.utils import log_execution_time


class PyMuPDFPDFConverter(PDFConverter):
    """
    Concrete implementation of PDFConverter using the pymupdf4llm library.
    """

    @log_execution_time
    def convert(self, resource: PDFResource) -> str:
        doc = Document(stream=BytesIO(resource.content), filetype="pdf")
        return pymupdf4llm.to_markdown(
            doc, header=False, use_ocr=False, show_progress=True, write_images=False
        )
