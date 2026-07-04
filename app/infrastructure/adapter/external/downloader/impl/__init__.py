"""
NextProject 2026

This file is part of the NP Collector Curriculum project.
Unauthorized copying of this file, via any medium is strictly prohibited.
"""

from infrastructure.adapter.external.downloader.impl.html_downloader import (
    HTMLDownloader,
)
from infrastructure.adapter.external.downloader.impl.pdf_downloader import PDFDownloader

__all__ = [
    "HTMLDownloader",
    "PDFDownloader",
]
