"""
NextProject 2026

This file is part of the NP Collector Curriculum project.
Unauthorized copying of this file, via any medium is strictly prohibited.
"""

import aiohttp

from domain.model.scrap_resource import ScrapResource
from domain.port.outbound.content_downloader import ContentDownloader
from domain.model.resource_type import ResourceType


class HTMLDownloader(ContentDownloader[str]):
    def __init__(self) -> None:
        self.timeout = aiohttp.ClientTimeout(60)

    async def download(self, url: str) -> ScrapResource[str]:
        async with aiohttp.ClientSession(timeout=self.timeout) as client:
            response = await client.get(url, allow_redirects=True)
            response.raise_for_status()

            content = await response.text()
            return ScrapResource(url=url, type=ResourceType.HTML, content=content)
