# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Tuple, List, Any, Optional
from bs4 import BeautifulSoup
from app.domain.model.root import Root
from app.domain.model.node import Node
from app.domain.model.resource_type import ResourceType
from app.infrastructure.adapter.outbound.http.parser.node_parser import NodeParser


class RootHTMLParser(NodeParser):
    def parse(
        self,
        node: Node[Any],
        parent_id: Optional[int] = None,
        metadata: Optional[dict] = None,
    ) -> Tuple[Root, List[Node]]:
        soup = BeautifulSoup(node.content, "html.parser")
        title = "Curriculum Nacional"
        if soup.title and soup.title.string:
            title = soup.title.string.strip()

        nodes = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "/curriculum/" in href:
                nodes.append(
                    Node(url=href, resource_type=ResourceType.HTML, content=None)
                )

        return Root(title=title, url=node.url), nodes
