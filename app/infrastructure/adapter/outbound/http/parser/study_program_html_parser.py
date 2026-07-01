# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import hashlib
from datetime import datetime
from typing import Tuple, List, Any, Optional
from app.domain.model.study_program import StudyProgram
from app.domain.model.node import Node
from app.infrastructure.adapter.outbound.http.parser.node_parser import NodeParser


class StudyProgramHTMLParser(NodeParser):
    def parse(
        self,
        node: Node[Any],
        parent_id: Optional[int] = None,
        metadata: Optional[dict] = None,
    ) -> Tuple[StudyProgram, List[Node]]:
        if isinstance(node.content, str):
            raw_content = node.content.encode("utf-8")
        else:
            raw_content = node.content

        metadata = metadata or {}
        modality_title = metadata.get("modality", "")
        subject_title = metadata.get("subject", "")
        grade_level_title = metadata.get("grade_level", "")

        # Formatting as Canonical Markdown structure (traceability metadata header)
        metadata_header = (
            f"---\n"
            f"source_url: {node.url}\n"
            f"extracted_at: {datetime.utcnow().isoformat()}\n"
            f"version: 1.0\n"
            f"modality: {modality_title}\n"
            f"subject: {subject_title}\n"
            f"grade_level: {grade_level_title}\n"
            f"---\n\n"
        ).encode("utf-8")

        # Prepend metadata to the canonical markdown content
        content_bytes = metadata_header + raw_content
        md5 = hashlib.md5(content_bytes).hexdigest()

        program = StudyProgram(
            url=node.url,
            study_program_ref_id=parent_id or 0,
            md5sum=md5,
            content=content_bytes,
        )
        return program, []
