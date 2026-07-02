# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from hashlib import sha256
from datetime import datetime
from typing import Tuple, List, Optional
from app.domain.model.study_program import StudyProgram
from app.domain.model.node import Node
from app.infrastructure.adapter.outbound.http.parser.node_parser import NodeParser


class StudyProgramNodeParser(NodeParser[bytes]):
    def parse(
        self,
        node: Node[bytes],
        parent_id: Optional[int] = None,
        metadata: Optional[dict] = None,
    ) -> Tuple[StudyProgram, List[Node]]:
        checksum = sha256(node.content)

        return StudyProgram(
            url=node.url,
            study_program_ref_id=parent_id,
            checksum=checksum.hexdigest(),
            content=node.content,
            extracted_at=datetime.now(),
        ), []
