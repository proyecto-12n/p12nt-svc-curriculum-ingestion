# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Tuple, List, Optional
from domain.model import StudyProgramRef
from domain.model.node import Node
from domain.model.resource_type import ResourceType
from domain.model.scrap_resource import ScrapResource
from infrastructure.adapter.outbound.http.parser.scrap_resource_parser import (
    ScrapResourceParser,
)
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from infrastructure.util.id_generator import generate_id
from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType


class StudyProgramRefScrapResourceParser(ScrapResourceParser[str]):
    async def parse(
        self,
        resource: ScrapResource[str],
        parent_id: int,
    ) -> Tuple[StudyProgramRef, List[Node]]:

        soup = BeautifulSoup(resource.content, "html.parser")
        title = StudyProgramRefScrapResourceParser._extract_title(soup)
        children = StudyProgramRefScrapResourceParser._extract_nodes(resource.url, soup)
        return StudyProgramRef(
            id=generate_id(resource.url),
            grade_level_id=parent_id,
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
        for a in soup.find_all("a", href=True):
            if not a.get("href").lower().endswith(".pdf"):
                continue

            u = urljoin(base_url, a.get("href"))
            nodes.append(
                Node(
                    url=u,
                    type=ResourceType.PDF,
                    level=CurriculumHierarchyType.STUDY_PROGRAM,
                )
            )

        return nodes
