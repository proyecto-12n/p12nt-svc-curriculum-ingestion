"""
NextProject 2026

This file is part of the NP Collector Curriculum project.
Unauthorized copying of this file, via any medium is strictly prohibited.
"""

from io import BytesIO

from markitdown import MarkItDown, StreamInfo

from domain.model.pdf_resource import PDFResource
from domain.port.outbound.pdf_converter import PDFConverter


class MarkItDownPDFConverter(PDFConverter):
    def __init__(self):
        self.converter = MarkItDown()

    def convert(self, resource: PDFResource) -> str:
        stream = BytesIO(resource.content)
        response = self.converter.convert_stream(
            stream,
            stream_info=StreamInfo(extension=".pdf"),
        )
        return response.markdown
