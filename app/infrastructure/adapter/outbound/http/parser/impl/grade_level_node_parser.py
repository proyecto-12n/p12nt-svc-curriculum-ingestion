# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Tuple, List, Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from domain.model import GradeLevel
from domain.model.node import Node
from domain.model.resource_type import ResourceType
from domain.model.scrap_resource import ScrapResource
from infrastructure.adapter.outbound.http.parser.scrap_resource_parser import (
    ScrapResourceParser,
)
from infrastructure.util.id_generator import generate_id
from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType


class GradeLevelScrapResourceParser(ScrapResourceParser[str]):
    async def parse(
        self,
        resource: ScrapResource[str],
        parent_id: int,
    ) -> Tuple[GradeLevel, List[Node]]:
        soup = BeautifulSoup(resource.content, "html.parser")
        title = GradeLevelScrapResourceParser._extract_title(soup)
        children = GradeLevelScrapResourceParser._extract_nodes(resource.url, soup)

        return GradeLevel(
            id=generate_id(resource.url),
            subject_id=parent_id,
            url=resource.url,
            title=title,
            content=resource.content,
        ), children

    @staticmethod
    def _extract_title(soup: BeautifulSoup) -> Optional[str]:
        h1_tag = soup.find("h1")
        title = h1_tag.get_text(strip=True) if h1_tag else None
        return title

    @staticmethod
    def _extract_nodes(base_url: str, soup: BeautifulSoup) -> List[Node]:
        nodes = []
        for div in soup.find_all("div", class_="three-grid-content"):
            for card in div.find_all("div", class_="card--content"):
                badge = card.find("span", class_="badge")
                if not badge or "Programa de estudio" not in badge.get_text(strip=True):
                    continue

                a = card.find("a", href=True)
                if not a:
                    continue

                u = urljoin(base_url, a.get("href"))
                nodes.append(
                    Node(
                        url=u,
                        type=ResourceType.HTML,
                        level=CurriculumHierarchyType.STUDY_PROGRAM_REF,
                        title=a.get_text(strip=True),
                    )
                )

        return nodes
