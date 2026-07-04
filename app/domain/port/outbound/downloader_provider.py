# -*- coding: utf-8 -*-
"""
NextProject © 2026
"""

from typing import Protocol
from domain.model.resource_type import ResourceType
from domain.port.outbound.content_downloader import ContentDownloader


class DownloaderProvider(Protocol):
    def get_downloader(self, resource_type: ResourceType) -> ContentDownloader:
        """
        Retrieves a ContentDownloader implementation by resource type.
        """
        ...
