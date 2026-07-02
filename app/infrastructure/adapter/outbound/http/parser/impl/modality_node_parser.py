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

from app.domain.model.modality import Modality
from app.domain.model.node import Node
from app.domain.model.resource_type import ResourceType
from app.infrastructure.adapter.outbound.http.parser.node_parser import NodeParser
from infrastructure.util.id_generator import generate_id


class ModalityNodeParser(NodeParser[str]):
    CURRICULUM_FIELD = "curriculum"

    def parse(
        self,
        node: Node[str],
        parent_id: Optional[int] = None,
        metadata: Optional[dict] = None,
    ) -> Tuple[Modality, List[Node]]:

        soup = BeautifulSoup(node.content, "html.parser")
        title = ModalityNodeParser._extract_title(soup)
        children = ModalityNodeParser._extract_nodes(node.url, soup)

        curriculum_val = (
            metadata.get(ModalityNodeParser.CURRICULUM_FIELD) if metadata else ""
        )
        return Modality(
            id=generate_id(curriculum_val, title),
            curriculum_id=parent_id,
            title=title,
            url=node.url,
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
            nodes.append(Node(url=u, type=ResourceType.HTML))

        return nodes
