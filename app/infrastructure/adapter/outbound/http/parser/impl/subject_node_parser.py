# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Tuple, List, Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from app.domain.model.subject import Subject
from app.domain.model.node import Node
from app.domain.model.resource_type import ResourceType
from app.infrastructure.adapter.outbound.http.parser.node_parser import NodeParser
from infrastructure.util.id_generator import generate_id


class SubjectNodeParser(NodeParser[str]):
    CURRICULUM_FIELD = "curriculum"
    MODALITY_FIELD = "modality"

    def parse(
        self,
        node: Node[str],
        parent_id: Optional[int] = None,
        metadata: Optional[dict] = None,
    ) -> Tuple[Subject, List[Node]]:

        soup = BeautifulSoup(node.content, "html.parser")
        title = SubjectNodeParser._extract_title(soup)
        children = SubjectNodeParser._extract_nodes(node.url, soup)

        curriculum_val = (
            metadata.get(SubjectNodeParser.CURRICULUM_FIELD) if metadata else None
        )
        modality_val = (
            metadata.get(SubjectNodeParser.MODALITY_FIELD) if metadata else None
        )
        return Subject(
            id=generate_id(curriculum_val, modality_val, title),
            modality_id=parent_id,
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
        for subject_soup in soup.find_all("div", class_="cursos-wrapper"):
            for grade_soup in subject_soup.find_all("div", class_="grade-wrapper"):
                for a in grade_soup.find_all("a", href=True):
                    title = a.get_text(strip=True)
                    u = urljoin(base_url, a.get("href"))
                    nodes.append(
                        Node(
                            url=u,
                            type=ResourceType.HTML,
                            title=title,
                        )
                    )
        return nodes
