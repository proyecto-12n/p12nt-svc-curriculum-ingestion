# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from domain.model.edge import Edge
from domain.model.resource_type import ResourceType
from domain.port.outbound.curriculum_hierarchy_mapper import CurriculumHierarchyMapper
from infrastructure.models import GradeLevel, StudyProgramRef
from infrastructure.util import generate_id


class StudyProgramRefMapper(CurriculumHierarchyMapper[StudyProgramRef, str]):
    def to_edge(self, model: StudyProgramRef) -> Edge[str]:
        return Edge(
            url=model.url,
            type=ResourceType.HTML,
            hierarchy=CurriculumHierarchyType.STUDY_PROGRAM_REF,
            title=model.title,
            content=model.content,
        )

    def to_model(self, edge: Edge[str]) -> StudyProgramRef:
        assert edge.hierarchy == CurriculumHierarchyType.STUDY_PROGRAM_REF
        assert edge.parent_url
        assert edge.content
        grade_level_id = generate_id(edge.parent_url)

        return StudyProgramRef(
            id=generate_id(edge.url),
            url=edge.url,
            title=edge.title,
            content=edge.content,
            grade_levels=[
                GradeLevel(
                    id=grade_level_id,
                    parent_id=0,
                    url="",
                    title="",
                    content="",
                )
            ],
        )
