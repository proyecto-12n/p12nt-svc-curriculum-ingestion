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
from domain.model.edge import Edge
from domain.model.resource_type import ResourceType
from domain.model.scrap_resource import ScrapResource
from infrastructure.adapter.outbound.http.parser.scrap_resource_parser import (
    ScrapResourceParser,
)
from infrastructure.util import BeautifulSoupBuilder


class StudyProgramRefScrapResourceParser(ScrapResourceParser[str]):
    async def get_children(
        self, resource: ScrapResource[str]
    ) -> AsyncGenerator[Edge[Any], Any]:
        soup = BeautifulSoupBuilder.build(resource)
        async for x in self.__extract_nodes(soup):
            yield x

    async def get_edge(self, resource: ScrapResource[str]) -> Edge[str]:

        soup = BeautifulSoupBuilder.build(resource)
        title = await self.__extract_title(soup)

        return Edge(
            url=resource.url,
            type=ResourceType.HTML,
            hierarchy=CurriculumHierarchyType.STUDY_PROGRAM_REF,
            title=title,
            content=resource.content,
        )

    async def get_title(self, resource: ScrapResource[str]) -> Optional[str]:
        soup = BeautifulSoupBuilder.build(resource)
        return await self.__extract_title(soup)

    @staticmethod
    async def __extract_title(soup: BeautifulSoup) -> Optional[str]:
        h1_tag = soup.find("h1")
        title = h1_tag.get_text(strip=True) if h1_tag else None
        return title

    @staticmethod
    async def __extract_nodes(soup: BeautifulSoup) -> AsyncGenerator[Edge[Any], Any]:
        for a in soup.find_all("a", href=True):
            if not a.get("href").lower().endswith(".pdf"):
                continue

            yield Edge(
                url=a.get("href"),
                type=ResourceType.PDF,
                hierarchy=CurriculumHierarchyType.STUDY_PROGRAM,
            )
