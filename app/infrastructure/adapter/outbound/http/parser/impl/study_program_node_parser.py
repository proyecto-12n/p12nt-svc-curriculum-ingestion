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

from app.domain.model.study_program import StudyProgram
from app.domain.model.node import Node
from app.infrastructure.adapter.outbound.http.parser.node_parser import NodeParser
from infrastructure.util.id_generator import generate_id


class StudyProgramNodeParser(NodeParser[bytes]):
    CURRICULUM_FIELD = "curriculum"
    MODALITY_FIELD = "modality"
    SUBJECT_FIELD = "subject"
    GRADE_LEVEL_FIELD = "grade-level"
    STUDY_PROGRAM_REF_FIELD = "study_program_ref"

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

        curriculum_val = (
            metadata.get(StudyProgramNodeParser.CURRICULUM_FIELD) if metadata else None
        )
        modality_val = (
            metadata.get(StudyProgramNodeParser.MODALITY_FIELD) if metadata else None
        )
        subject_val = (
            metadata.get(StudyProgramNodeParser.SUBJECT_FIELD) if metadata else None
        )
        grade_level_val = (
            metadata.get(StudyProgramNodeParser.SUBJECT_FIELD) if metadata else None
        )
        study_program_ref_val = (
            metadata.get(StudyProgramNodeParser.STUDY_PROGRAM_REF_FIELD)
            if metadata
            else None
        )

        return StudyProgram(
            id=generate_id(
                curriculum_val,
                modality_val,
                subject_val,
                grade_level_val,
                study_program_ref_val,
                title,
            ),
            study_program_ref_id=parent_id,
            url=node.url,
            title=title,
            content=node.content,
            checksum=checksum.hexdigest(),
            extracted_at=datetime.now(),
        ), []
