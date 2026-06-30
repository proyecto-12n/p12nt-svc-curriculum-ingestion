"""
NextProject 2026

This file is part of the NP Collector Curriculum project.
Unauthorized copying of this file, via any medium is strictly prohibited.
"""

from app.infrastructure.adapter.external.downloader import HTMLDownloader, PDFDownloader
from app.infrastructure.adapter.external.downloader_provider import DownloaderProvider
from app.infrastructure.adapter.external.pdf_converter.docling_pdf_converter import (
    DoclingPDFConverter,
)
from app.infrastructure.adapter.external.pdf_converter.markitdown_pdf_converter import (
    MarkItDownPDFConverter,
)
from app.infrastructure.adapter.external.pdf_converter.pymupdf_pdf_converter import (
    PyMuPDFPDFConverter,
)
from app.infrastructure.adapter.external.pdf_converter_provider import (
    PDFConverterProvider,
)
from app.infrastructure.adapter.external.study_program_agent_parser.pydantic_ai_study_program_agent_parser import (
    PydanticAiStudyProgramAgentParser,
)
from app.infrastructure.adapter.external.study_program_agent_parser_provider import (
    StudyProgramAgentParserProvider,
)

__all__ = [
    "DoclingPDFConverter",
    "DownloaderProvider",
    "HTMLDownloader",
    "MarkItDownPDFConverter",
    "PDFConverterProvider",
    "PDFDownloader",
    "PyMuPDFPDFConverter",
    "PydanticAiStudyProgramAgentParser",
    "StudyProgramAgentParserProvider",
]
