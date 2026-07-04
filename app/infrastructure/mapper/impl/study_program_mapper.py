# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from domain.model.node import Node
from domain.model.resource_type import ResourceType
from domain.port.outbound.curriculum_hierarchy_mapper import CurriculumHierarchyMapper
from infrastructure.models import StudyProgram


class StudyProgramMapper(CurriculumHierarchyMapper[StudyProgram, bytes]):
    def to_domain_node(self, model: StudyProgram) -> Node[bytes]:
        return Node(
            url=model.url,
            type=ResourceType.PDF,
            hierarchy=CurriculumHierarchyType.STUDY_PROGRAM,
            title=model.title,
            content=model.content,
        )
