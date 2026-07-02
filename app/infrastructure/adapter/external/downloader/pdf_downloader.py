"""
NextProject 2026

This file is part of the NP Collector Curriculum project.
Unauthorized copying of this file, via any medium is strictly prohibited.
"""

import httpx

from app.domain.port.outbound.content_downloader import ContentDownloader
from app.domain.model.node import Node
from app.domain.model.resource_type import ResourceType


class PDFDownloader(ContentDownloader[bytes]):
    async def download(self, url: str, timeout: float = 120.0) -> Node[bytes]:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            return Node(url=url, type=ResourceType.PDF, content=response.content)
