# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Tuple, List, Optional
from domain.model import StudyProgramRef
from domain.model.node import Node
from domain.model.resource_type import ResourceType
from infrastructure.adapter.outbound.http.parser.node_parser import NodeParser
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from infrastructure.util.id_generator import generate_id
from domain.model.curriculum_node_type import CurriculumNodeType


class StudyProgramRefNodeParser(NodeParser[str]):
    def parse(
        self,
        node: Node[str],
        parent_id: int,
    ) -> Tuple[StudyProgramRef, List[Node]]:

        soup = BeautifulSoup(node.content, "html.parser")
        title = StudyProgramRefNodeParser._extract_title(soup)
        children = StudyProgramRefNodeParser._extract_nodes(node.url, soup)
        return StudyProgramRef(
            id=generate_id(node.url),
            grade_level_id=parent_id,
            url=node.url,
            title=title,
            content=node.content,
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
                    url=u, type=ResourceType.PDF, level=CurriculumNodeType.STUDY_PROGRAM
                )
            )

        return nodes
