"""
NextProject 2026

This file is part of the NP Collector Curriculum project.
Unauthorized copying of this file, via any medium is strictly prohibited.
"""

from io import BytesIO

from markitdown import MarkItDown, StreamInfo

from app.domain.port.outbound.pdf_converter import PDFConverter
from app.domain.model.pdf_resource import PDFResource
from app.utils import log_execution_time


class MarkItDownPDFConverter(PDFConverter):
    """
    Concrete implementation of PDFConverter using the MarkItDown library.
    """

    def __init__(self):

        self.converter = MarkItDown()

    @log_execution_time
    def convert(self, resource: PDFResource) -> str:
        stream_info = StreamInfo(extension=".pdf")

        stream = BytesIO(resource.content)
        response = self.converter.convert_stream(stream, stream_info=stream_info)
        return response.markdown
