"""
NextProject 2026

This file is part of the NP Collector Curriculum project.
Unauthorized copying of this file, via any medium is strictly prohibited.
"""

from app.infrastructure.adapter.external.downloader.html_downloader import (
    HTMLDownloader,
)
from app.infrastructure.adapter.external.downloader.pdf_downloader import PDFDownloader

__all__ = [
    "HTMLDownloader",
    "PDFDownloader",
]
