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
from infrastructure.adapter.outbound.http.parser.scrap_resource_title_strategy_provider import (
    ScrapResourceTitleStrategyProvider,
)
from infrastructure.util import BeautifulSoupBuilder


class SubjectScrapResourceParser(ScrapResourceParser[str]):
    TITLE_SUFFIXES = ("3° medio", "4° medio", "3º medio", "4º medio")

    async def get_children(
        self, resource: ScrapResource[str]
    ) -> AsyncGenerator[Edge[str], Any]:
        soup = BeautifulSoupBuilder.build(resource)
        async for x in self.__extract_nodes(soup):
            yield x

    async def get_title(self, resource: ScrapResource[str]) -> str:
        soup = BeautifulSoupBuilder.build(resource)
        title = ScrapResourceTitleStrategyProvider.get_strategy(
            ResourceType.HTML
        ).extract(soup)
        return self.__remove_title_suffix(title)

    @classmethod
    def __remove_title_suffix(cls, title: str) -> str:
        for suffix in cls.TITLE_SUFFIXES:
            if title.casefold().endswith(suffix.casefold()):
                return title[: -len(suffix)].strip()

        return title

    @staticmethod
    async def __extract_nodes(soup: BeautifulSoup) -> AsyncGenerator[Edge[str], Any]:
        for subject_soup in soup.find_all("div", class_="cursos-wrapper"):
            for grade_soup in subject_soup.find_all("div", class_="grade-wrapper"):
                for a in grade_soup.find_all("a", href=True):
                    yield Edge(
                        url=a.get("href"),
                        type=ResourceType.HTML,
                        hierarchy=CurriculumHierarchyType.GRADE_LEVEL,
                        title=a.get_text(strip=True),
                    )
