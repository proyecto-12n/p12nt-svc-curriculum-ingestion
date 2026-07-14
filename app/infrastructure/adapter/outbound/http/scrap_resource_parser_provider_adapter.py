# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Dict

from domain.port.outbound.scrap_resource_parser_provider import (
    ScrapResourceParserProvider,
)
from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from domain.port.outbound.scrap_resource_parser import (
    ScrapResourceParser,
)
from infrastructure.adapter.outbound.http.parser.impl import (
    CurriculumScrapResourceParser,
    GradeLevelScrapResourceParser,
    ModalityScrapResourceParser,
    StudyProgramScrapResourceParser,
    StudyProgramRefScrapResourceParser,
    SubjectScrapResourceParser,
)


class ScrapResourceParserProviderAdapter(ScrapResourceParserProvider):
    def __init__(self):
        self._parsers: Dict[CurriculumHierarchyType, ScrapResourceParser] = {
            CurriculumHierarchyType.CURRICULUM: CurriculumScrapResourceParser(),
            CurriculumHierarchyType.MODALITY: ModalityScrapResourceParser(),
            CurriculumHierarchyType.SUBJECT: SubjectScrapResourceParser(),
            CurriculumHierarchyType.GRADE_LEVEL: GradeLevelScrapResourceParser(),
            CurriculumHierarchyType.STUDY_PROGRAM_REF: StudyProgramRefScrapResourceParser(),
            CurriculumHierarchyType.STUDY_PROGRAM: StudyProgramScrapResourceParser(),
        }

    def get_parser(self, discriminator: CurriculumHierarchyType) -> ScrapResourceParser:
        parser = self._parsers.get(discriminator)
        if not parser:
            raise ValueError(f"No parser configured for discriminator: {discriminator}")
        return parser
