"""
NextProject 2026

This file is part of the NP Collector Curriculum project.
Unauthorized copying of this file, via any medium is strictly prohibited.
"""

import aiohttp

from app.domain.port.outbound.content_downloader import ContentDownloader


class PDFDownloader(ContentDownloader[bytes]):
    async def download(self, url: str, timeout: float = 120.0) -> bytes:
        async with aiohttp.AsyncClient(timeout=timeout) as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            return response.content
