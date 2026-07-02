# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from hashlib import sha256
from datetime import datetime
from os import path
from typing import Tuple, List, Optional
from urllib.parse import urlparse

from app.domain.model import StudyProgram
from app.domain.model.node import Node
from app.infrastructure.adapter.outbound.http.parser.node_parser import NodeParser
from app.infrastructure.util.id_generator import generate_id


class StudyProgramNodeParser(NodeParser[bytes]):
    def parse(
        self,
        node: Node[bytes],
        parent_id: Optional[int] = None,
        metadata: Optional[dict] = None,
    ) -> Tuple[StudyProgram, List[Node]]:
        checksum = sha256(node.content)

        parsed_url = urlparse(node.url)
        filename = path.basename(parsed_url.path)
        title = filename if filename else ""
        return StudyProgram(
            id=generate_id(node.url),
            study_program_ref_id=parent_id,
            url=node.url,
            title=title,
            content=node.content,
            checksum=checksum.hexdigest(),
            extracted_at=datetime.now(),
        ), []
