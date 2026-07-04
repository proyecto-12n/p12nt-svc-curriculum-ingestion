"""
NextProject 2026

This file is part of the NP Collector Curriculum project.
Unauthorized copying of this file, via any medium is strictly prohibited.
"""

from aiohttp import ClientSession

from domain.model.scrap_resource import ScrapResource
from domain.port.outbound.content_downloader import ContentDownloader
from domain.model.resource_type import ResourceType


class HTMLDownloader(ContentDownloader[str]):
    async def download(self, url: str, timeout: float = 60.0) -> ScrapResource[str]:
        async with ClientSession(timeout=timeout) as client:
            response = await client.get(url, allow_redirects=True)
            response.raise_for_status()

            content = await response.text()
            return ScrapResource(url=url, type=ResourceType.HTML, content=content)
