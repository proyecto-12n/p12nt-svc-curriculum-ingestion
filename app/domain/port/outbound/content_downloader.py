"""
NextProject 2026

This file is part of the NP Collector Curriculum project.
Unauthorized copying of this file, via any medium is strictly prohibited.
"""

from typing import Protocol, TypeVar

from domain.model.scrap_resource import ScrapResource

T = TypeVar("T")


class ContentDownloader(Protocol[T]):
    async def download(self, url: str) -> ScrapResource[T]: ...
