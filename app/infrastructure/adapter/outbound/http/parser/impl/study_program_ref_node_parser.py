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

from infrastructure.util.id_generator import generate_id


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
        title = StudyProgramRefNodeParser._extract_title(soup)
        children = StudyProgramRefNodeParser._extract_nodes(node.url, soup)

        curriculum_val = (
            metadata.get(StudyProgramRefNodeParser.CURRICULUM_FIELD)
            if metadata
            else None
        )
        modality_val = (
            metadata.get(StudyProgramRefNodeParser.MODALITY_FIELD) if metadata else None
        )
        subject_val = (
            metadata.get(StudyProgramRefNodeParser.SUBJECT_FIELD) if metadata else None
        )
        grade_level_val = (
            metadata.get(StudyProgramRefNodeParser.SUBJECT_FIELD) if metadata else None
        )

        return StudyProgramRef(
            id=generate_id(
                curriculum_val, modality_val, subject_val, grade_level_val, title
            ),
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
            nodes.append(Node(url=u, type=ResourceType.PDF))

        return nodes
