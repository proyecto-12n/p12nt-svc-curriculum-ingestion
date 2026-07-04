"""
NextProject 2026

This file is part of the NP Collector Curriculum project.
Unauthorized copying of this file, via any medium is strictly prohibited.
"""

from aiohttp import ClientSession, ClientTimeout

from domain.model.resource_type import ResourceType
from domain.model.scrap_resource import ScrapResource
from domain.port.outbound.content_downloader import ContentDownloader


class PDFDownloader(ContentDownloader[bytes]):
    async def download(self, url: str, timeout: float = 120.0) -> ScrapResource[bytes]:
        async with ClientSession(timeout=ClientTimeout(timeout)) as client:
            response = await client.get(url, allow_redirects=True)
            response.raise_for_status()
            return ScrapResource(
                url=url, type=ResourceType.PDF, content=response.content
            )
