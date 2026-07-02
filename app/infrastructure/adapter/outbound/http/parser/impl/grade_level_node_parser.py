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
from app.domain.model import GradeLevel
from app.domain.model.node import Node
from app.domain.model.resource_type import ResourceType
from app.infrastructure.adapter.outbound.http.parser.node_parser import NodeParser
from app.infrastructure.util.id_generator import generate_id


class GradeLevelNodeParser(NodeParser[str]):
    def parse(
        self,
        node: Node[str],
        parent_id: int,
    ) -> Tuple[GradeLevel, List[Node]]:
        soup = BeautifulSoup(node.content, "html.parser")
        title = GradeLevelNodeParser._extract_title(soup)
        children = GradeLevelNodeParser._extract_nodes(node.url, soup)

        return GradeLevel(
            id=generate_id(node.url),
            subject_id=parent_id,
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
        for div in soup.find_all("div", class_="three-grid-content"):
            for card in div.find_all("div", class_="card--content"):
                badge = card.find("span", class_="badge")
                if not badge or "Programa de estudio" not in badge.get_text(strip=True):
                    continue

                a = card.find("a", href=True)
                if not a:
                    continue

                u = urljoin(base_url, a.get("href"))
                nodes.append(Node(url=u, type=ResourceType.HTML))

        return nodes
