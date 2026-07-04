# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Dict

from domain.port.outbound.node_parser_provider import NodeParserProvider
from domain.model.curriculum_node_type import CurriculumNodeType
from infrastructure.adapter.outbound.http.parser.node_parser import NodeParser
from infrastructure.adapter.outbound.http.parser.impl import (
    CurriculumNodeParser,
    GradeLevelNodeParser,
    ModalityNodeParser,
    StudyProgramNodeParser,
    StudyProgramRefNodeParser,
    SubjectNodeParser,
)


class HttpNodeParserProviderAdapter(NodeParserProvider):
    def __init__(self):
        self._parsers: Dict[CurriculumNodeType, NodeParser] = {
            CurriculumNodeType.CURRICULUM: CurriculumNodeParser(),
            CurriculumNodeType.MODALITY: ModalityNodeParser(),
            CurriculumNodeType.SUBJECT: SubjectNodeParser(),
            CurriculumNodeType.GRADE_LEVEL: GradeLevelNodeParser(),
            CurriculumNodeType.STUDY_PROGRAM_REF: StudyProgramRefNodeParser(),
            CurriculumNodeType.STUDY_PROGRAM: StudyProgramNodeParser(),
        }

    def get_parser(self, discriminator: CurriculumNodeType) -> NodeParser:
        parser = self._parsers.get(discriminator)
        if not parser:
            raise ValueError(f"No parser configured for discriminator: {discriminator}")
        return parser
