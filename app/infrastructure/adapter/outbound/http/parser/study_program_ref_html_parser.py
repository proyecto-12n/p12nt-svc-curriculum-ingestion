# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Tuple, List, Any, Optional
from app.domain.model.study_program_ref import StudyProgramRef
from app.domain.model.node import Node
from app.domain.model.resource_type import ResourceType
from app.infrastructure.adapter.outbound.http.parser.node_parser import NodeParser


class StudyProgramRefHTMLParser(NodeParser):
    def parse(
        self,
        node: Node[Any],
        parent_id: Optional[int] = None,
        metadata: Optional[dict] = None,
    ) -> Tuple[StudyProgramRef, List[Node]]:
        res_type = ResourceType.PDF if ".pdf" in node.url.lower() else ResourceType.HTML
        nodes = [Node(url=node.url, resource_type=res_type, content=None)]

        return StudyProgramRef(grade_level_id=parent_id or 0, url=node.url), nodes
