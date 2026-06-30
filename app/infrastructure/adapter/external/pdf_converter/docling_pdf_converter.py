"""
NextProject 2026

This file is part of the NP Collector Curriculum project.
Unauthorized copying of this file, via any medium is strictly prohibited.
"""

import os
from tempfile import NamedTemporaryFile

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption

from app.domain.port.outbound.pdf_converter import PDFConverter
from app.domain.model.pdf_resource import PDFResource
from app.utils import log_execution_time


class DoclingPDFConverter(PDFConverter):
    """
    Concrete implementation of PDFConverter using the Docling library.
    """

    def __init__(self):

        # do_ocr = False
        pipeline_options = PdfPipelineOptions(
            generate_page_images=False, generate_picture_images=False
        )

        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )

    @log_execution_time
    def convert(self, resource: PDFResource) -> str:
        temp_pdf = NamedTemporaryFile(suffix=".pdf", delete=False)
        try:
            temp_pdf.write(resource.content)
            temp_pdf.close()

            converter_result = self.converter.convert(temp_pdf.name)
            return converter_result.document.export_to_markdown()
        finally:
            os.unlink(temp_pdf.name)
