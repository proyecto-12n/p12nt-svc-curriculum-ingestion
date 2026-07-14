# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Any, AsyncGenerator

from bs4 import BeautifulSoup

from domain.model.edge import Edge
from domain.model.resource_type import ResourceType
from domain.model.scrap_resource import ScrapResource
from domain.port.outbound.scrap_resource_parser import (
    ScrapResourceParser,
)
from infrastructure.adapter.outbound.http.parser.scrap_resource_title_strategy_provider import (
    ScrapResourceTitleStrategyProvider,
)
from infrastructure.util import BeautifulSoupBuilder
from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType


class ModalityScrapResourceParser(ScrapResourceParser[str]):
    async def get_children(
        self, resource: ScrapResource[str]
    ) -> AsyncGenerator[Edge[str], Any]:
        soup = BeautifulSoupBuilder.build(resource)
        async for x in self.__extract_nodes(soup):
            yield x

    async def get_title(self, resource: ScrapResource[str]) -> str:
        soup = BeautifulSoupBuilder.build(resource)
        return ScrapResourceTitleStrategyProvider.get_strategy(
            ResourceType.HTML
        ).extract(soup)

    @staticmethod
    async def __extract_nodes(soup: BeautifulSoup) -> AsyncGenerator[Edge, Any]:
        for span in soup.select("div.subject a span.subject-title"):
            a = span.find_parent("a", href=True)
            if not a:
                continue

            yield Edge(
                url=a.get("href"),
                type=ResourceType.HTML,
                hierarchy=CurriculumHierarchyType.SUBJECT,
                title=span.get_text(strip=True),
            )
