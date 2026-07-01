"""
NextProject 2026

This file is part of the NP Collector Curriculum project.
Unauthorized copying of this file, via any medium is strictly prohibited.
"""

import httpx
from bs4 import BeautifulSoup

from app.domain.port.outbound.content_downloader import ContentDownloader
from app.domain.model.node import Node
from app.domain.model.resource_type import ResourceType


class HTMLDownloader(ContentDownloader[str]):
    async def download(self, url: str, timeout: float = 60.0) -> Node[str]:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            return Node(
                url=url, resource_type=ResourceType.HTML, content=soup.prettify()
            )
