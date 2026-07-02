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

from app.domain.model.curriculum import Curriculum
from app.domain.model.node import Node
from app.domain.model.resource_type import ResourceType
from app.infrastructure.adapter.outbound.http.parser.node_parser import NodeParser
from infrastructure.util.id_generator import generate_id


class CurriculumNodeParser(NodeParser[str]):
    def parse(
        self,
        node: Node[str],
        parent_id: Optional[int] = None,
        metadata: Optional[dict] = None,
    ) -> Tuple[Curriculum, List[Node]]:
        soup = BeautifulSoup(node.content, "html.parser")

        title = CurriculumNodeParser._extract_title(soup)
        children = CurriculumNodeParser._extract_nodes(node.url, soup)

        return Curriculum(id=generate_id(title), title=title, url=node.url), children

    @staticmethod
    def _extract_title(soup: BeautifulSoup) -> Optional[str]:
        h1_tag = soup.find("h1")
        title = h1_tag.get_text(strip=True) if h1_tag else None
        return title

    @staticmethod
    def _extract_nodes(base_url: str, soup: BeautifulSoup) -> List[Node]:
        nodes = []
        for div in soup.find_all("div", class_="menu"):
            for a in div.find_all("a", href=True):
                h3 = a.find("h3")
                if h3 is None:
                    continue

                title = h3.get_text(strip=True)
                u = urljoin(base_url, a.get("href"))
                nodes.append(Node(url=u, type=ResourceType.HTML, title=title))

        return nodes
