# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import AsyncGenerator, Any

from bs4 import BeautifulSoup

from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from domain.model.edge import Edge
from domain.model.resource_type import ResourceType
from domain.model.scrap_resource import ScrapResource
from infrastructure.adapter.outbound.http.parser.scrap_resource_parser import (
    ScrapResourceParser,
)
from infrastructure.adapter.outbound.http.parser.html_scrap_resource_title_strategy import (
    HtmlScrapResourceTitleStrategy,
)
from infrastructure.util import BeautifulSoupBuilder


class SubjectScrapResourceParser(ScrapResourceParser[str]):
    async def get_children(
        self, resource: ScrapResource[str]
    ) -> AsyncGenerator[Edge[str], Any]:
        soup = BeautifulSoupBuilder.build(resource)
        async for x in self.__extract_nodes(soup):
            yield x

    async def get_edge(self, resource: ScrapResource[str]) -> Edge[str]:

        soup = BeautifulSoupBuilder.build(resource)
        title = HtmlScrapResourceTitleStrategy.extract(soup)

        return Edge(
            url=resource.url,
            type=ResourceType.HTML,
            hierarchy=CurriculumHierarchyType.SUBJECT,
            title=title,
            content=resource.content,
        )

    async def get_title(self, resource: ScrapResource[str]) -> str:
        soup = BeautifulSoupBuilder.build(resource)
        return HtmlScrapResourceTitleStrategy.extract(soup)

    @staticmethod
    async def __extract_nodes(soup: BeautifulSoup) -> AsyncGenerator[Edge[str], Any]:
        for subject_soup in soup.find_all("div", class_="cursos-wrapper"):
            for grade_soup in subject_soup.find_all("div", class_="grade-wrapper"):
                for a in grade_soup.find_all("a", href=True):
                    yield Edge(
                        url=a.get("href"),
                        type=ResourceType.HTML,
                        hierarchy=CurriculumHierarchyType.GRADE_LEVEL,
                    )
