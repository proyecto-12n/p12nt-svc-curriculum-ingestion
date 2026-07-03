# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import List, Optional, Tuple
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from app.domain.model import Modality
from app.domain.model.node import Node
from app.domain.model.resource_type import ResourceType
from app.infrastructure.adapter.outbound.http.parser.node_parser import NodeParser
from app.infrastructure.util.id_generator import generate_id
from app.domain.model.curriculum_node_type import CurriculumNodeType


class ModalityNodeParser(NodeParser[str]):
    def parse(
        self,
        node: Node[str],
        parent_id: int,
    ) -> Tuple[Modality, List[Node]]:

        soup = BeautifulSoup(node.content, "html.parser")
        title = ModalityNodeParser._extract_title(soup)
        children = ModalityNodeParser._extract_nodes(node.url, soup)
        return Modality(
            id=generate_id(node.url),
            curriculum_id=parent_id,
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
        for span in soup.select("div.subject a span.subject-title"):
            a = span.find_parent("a", href=True)
            if not a:
                continue

            u = urljoin(base_url, a.get("href"))
            nodes.append(
                Node(
                    url=u,
                    type=ResourceType.HTML,
                    level=CurriculumNodeType.SUBJECT,
                    title=span.get_text(strip=True),
                )
            )

        return nodes
