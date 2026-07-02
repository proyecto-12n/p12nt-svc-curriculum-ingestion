# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Tuple, List, Optional
from app.domain.model.study_program_ref import StudyProgramRef
from app.domain.model.node import Node
from app.domain.model.resource_type import ResourceType
from app.infrastructure.adapter.outbound.http.parser.node_parser import NodeParser
from urllib.parse import urljoin

from bs4 import BeautifulSoup


class StudyProgramRefNodeParser(NodeParser[str]):
    CURRICULUM_FIELD = "curriculum"
    MODALITY_FIELD = "modality"
    SUBJECT_FIELD = "subject"
    GRADE_LEVEL_FIELD = "grade-level"

    def parse(
        self,
        node: Node[str],
        parent_id: Optional[int] = None,
        metadata: Optional[dict] = None,
    ) -> Tuple[StudyProgramRef, List[Node]]:

        soup = BeautifulSoup(node.content, "html.parser")
        children = StudyProgramRefNodeParser._extract_nodes(node.url, soup)

        return StudyProgramRef(grade_level_id=parent_id, url=node.url), children

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

            title = a.get_text(strip=True)
            u = urljoin(base_url, a.get("href"))
            nodes.append(
                Node(
                    url=u,
                    type=ResourceType.PDF,
                    title=title,
                )
            )

        return nodes
