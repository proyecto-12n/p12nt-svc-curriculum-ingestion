# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Optional, AsyncGenerator, Any

from bs4 import BeautifulSoup

from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from domain.model.node import Node
from domain.model.resource_type import ResourceType
from domain.model.scrap_resource import ScrapResource
from infrastructure.adapter.outbound.http.parser.scrap_resource_parser import (
    ScrapResourceParser,
)
from infrastructure.util import BeautifulSoupBuilder


class StudyProgramRefScrapResourceParser(ScrapResourceParser[str]):
    async def get_node(self, resource: ScrapResource[str]) -> Node[str]:

        soup = BeautifulSoupBuilder.build(resource)
        title = await self.__extract_title(soup)

        return Node(
            url=resource.url,
            type=ResourceType.HTML,
            hierarchy=CurriculumHierarchyType.STUDY_PROGRAM_REF,
            title=title,
            content=resource.content,
        )

    async def get_children(
        self, resource: ScrapResource[str]
    ) -> AsyncGenerator[Node[Any], Any]:
        soup = BeautifulSoupBuilder.build(resource)
        async for x in self.__extract_nodes(soup):
            yield x

    @staticmethod
    async def __extract_title(soup: BeautifulSoup) -> Optional[str]:
        h1_tag = soup.find("h1")
        title = h1_tag.get_text(strip=True) if h1_tag else None
        return title

    @staticmethod
    async def __extract_nodes(soup: BeautifulSoup) -> AsyncGenerator[Node[Any], Any]:
        for a in soup.find_all("a", href=True):
            if not a.get("href").lower().endswith(".pdf"):
                continue

            yield Node(
                url=a.get("href"),
                type=ResourceType.PDF,
                hierarchy=CurriculumHierarchyType.STUDY_PROGRAM,
            )
