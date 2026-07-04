"""
NextProject 2026

This file is part of the NP Collector Curriculum project.
Unauthorized copying of this file, via any medium is strictly prohibited.
"""

from typing import Dict

from domain.port.outbound.content_downloader import ContentDownloader
from domain.port.outbound.downloader_provider import (
    DownloaderProvider as DownloaderProviderPort,
)
from domain.model.resource_type import ResourceType
from infrastructure.adapter.external.downloader.impl import (
    HTMLDownloader,
    PDFDownloader,
)


class DownloaderProvider(DownloaderProviderPort):
    def __init__(self):
        self._downloaders: Dict[ResourceType, ContentDownloader] = {
            ResourceType.HTML: HTMLDownloader(),
            ResourceType.PDF: PDFDownloader(),
        }

    def get_downloader(self, resource_type: ResourceType) -> ContentDownloader:
        downloader = self._downloaders.get(resource_type)
        if not downloader:
            raise ValueError(
                f"No downloader configured for resource type: {resource_type}"
            )
        return downloader
