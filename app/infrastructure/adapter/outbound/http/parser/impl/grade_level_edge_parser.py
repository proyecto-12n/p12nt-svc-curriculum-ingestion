# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import AsyncGenerator, Any

from bs4 import BeautifulSoup
from domain.model.edge import Edge
from domain.model.resource_type import ResourceType
from domain.model.scrap_resource import ScrapResource
from infrastructure.adapter.outbound.http.parser.scrap_resource_parser import (
    ScrapResourceParser,
)
from infrastructure.adapter.outbound.http.parser.scrap_resource_title_strategy_provider import (
    ScrapResourceTitleStrategyProvider,
)
from infrastructure.adapter.outbound.http.parser.breadcrumb_parser import (
    BreadcrumbParser,
)
from infrastructure.util import BeautifulSoupBuilder
from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType


class GradeLevelScrapResourceParser(ScrapResourceParser[str]):
    TITLE_REPLACEMENTS = {
        "SC (Sala Cuna)": "Sala Cuna (SC)",
        "NM (Nivel Medio)": "Nivel Medio (NM)",
        "NT (Nivel Transición)": "Nivel Transición (NT)",
    }

    def __init__(self):
        self.breadcrumb_parser = BreadcrumbParser()

    async def get_children(
        self, resource: ScrapResource[str]
    ) -> AsyncGenerator[Edge[str], Any]:
        soup = BeautifulSoupBuilder.build(resource)
        async for x in self.__extract_nodes(soup):
            yield x

    async def get_edge(self, resource: ScrapResource[str]) -> Edge[str]:

        soup = BeautifulSoupBuilder.build(resource)
        breadcrumbs = self.breadcrumb_parser.parse(soup)

        return Edge(
            url=resource.url,
            type=ResourceType.HTML,
            hierarchy=CurriculumHierarchyType.GRADE_LEVEL,
            parent_url=breadcrumbs[CurriculumHierarchyType.SUBJECT].url,
            title=await self.get_title(resource),
            content=resource.content,
        )

    async def get_title(self, resource: ScrapResource[str]) -> str:
        soup = BeautifulSoupBuilder.build(resource)
        title = ScrapResourceTitleStrategyProvider.get_strategy(
            ResourceType.HTML
        ).extract(soup)

        breadcrumbs = self.breadcrumb_parser.parse(soup)
        subject = breadcrumbs.get(CurriculumHierarchyType.SUBJECT)
        if subject and title.casefold().startswith(subject.title.casefold()):
            title = title[len(subject.title) :].strip()

        return self.TITLE_REPLACEMENTS.get(title, title)

    @staticmethod
    async def __extract_nodes(soup: BeautifulSoup) -> AsyncGenerator[Edge, Any]:
        for div in soup.find_all("div", class_="three-grid-content"):
            for card in div.find_all("div", class_="card--content"):
                badge = card.find("span", class_="badge")
                if not badge or badge.get_text(strip=True) not in (
                    "Programa de estudio"
                ):
                    continue

                a = card.find("a", href=True)
                if not a:
                    continue

                yield Edge(
                    url=a.get("href"),
                    type=ResourceType.HTML,
                    hierarchy=CurriculumHierarchyType.STUDY_PROGRAM_REF,
                    title=a.get_text(strip=True),
                )
