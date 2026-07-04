"""
NextProject 2026

This file is part of the NP Collector Curriculum project.
Unauthorized copying of this file, via any medium is strictly prohibited.
"""

from infrastructure.adapter.external.downloader import HTMLDownloader, PDFDownloader
from infrastructure.adapter.external.downloader_provider import DownloaderProvider
from infrastructure.adapter.external.pdf_converter_provider import (
    PDFConverterProvider,
)
from infrastructure.adapter.external.study_program_agent_parser_provider import (
    StudyProgramAgentParserProvider,
)

# Safe optional imports
try:
    from infrastructure.adapter.external.pdf_converter.markitdown_pdf_converter import (
        MarkItDownPDFConverter,
    )
except ImportError:
    MarkItDownPDFConverter = None

try:
    from infrastructure.adapter.external.pdf_converter.pymupdf_pdf_converter import (
        PyMuPDFPDFConverter,
    )
except ImportError:
    PyMuPDFPDFConverter = None

try:
    from infrastructure.adapter.external.study_program_agent_parser.pydantic_ai_study_program_agent_parser import (
        PydanticAiStudyProgramAgentParser,
    )
except ImportError:
    PydanticAiStudyProgramAgentParser = None

__all__ = [
    "DownloaderProvider",
    "HTMLDownloader",
    "MarkItDownPDFConverter",
    "PDFConverterProvider",
    "PDFDownloader",
    "PyMuPDFPDFConverter",
    "PydanticAiStudyProgramAgentParser",
    "StudyProgramAgentParserProvider",
]
