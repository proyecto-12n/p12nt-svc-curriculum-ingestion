# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Tuple, List, Any, Optional
from bs4 import BeautifulSoup
from app.domain.model.grade_level import GradeLevel
from app.domain.model.node import Node
from app.domain.model.resource_type import ResourceType
from app.infrastructure.adapter.outbound.http.parser.node_parser import NodeParser


class GradeLevelHTMLParser(NodeParser):
    def parse(
        self,
        node: Node[Any],
        parent_id: Optional[int] = None,
        metadata: Optional[dict] = None,
    ) -> Tuple[GradeLevel, List[Node]]:
        soup = BeautifulSoup(node.content, "html.parser")
        title = "GradeLevel"
        h1 = soup.find("h1")
        if h1:
            title = h1.get_text().strip()
        elif soup.title and soup.title.string:
            title = soup.title.string.strip()

        nodes = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if ".pdf" in href or "descargar" in href:
                res_type = (
                    ResourceType.PDF if ".pdf" in href.lower() else ResourceType.HTML
                )
                nodes.append(Node(url=href, resource_type=res_type, content=None))

        return GradeLevel(title=title, subject_id=parent_id or 0), nodes
