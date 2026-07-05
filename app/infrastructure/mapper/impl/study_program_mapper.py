# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from hashlib import sha256

from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from domain.model.edge import Edge
from domain.model.resource_type import ResourceType
from domain.port.outbound.curriculum_hierarchy_mapper import CurriculumHierarchyMapper
from infrastructure.models import StudyProgram
from infrastructure.util import generate_id


class StudyProgramMapper(CurriculumHierarchyMapper[StudyProgram, bytes]):
    def to_edge(self, model: StudyProgram) -> Edge[bytes]:
        return Edge(
            url=model.url,
            type=ResourceType.PDF,
            hierarchy=CurriculumHierarchyType.STUDY_PROGRAM,
            title=model.title,
            content=model.content,
        )

    def to_model(self, edge: Edge[bytes]) -> StudyProgram:
        assert edge.hierarchy == CurriculumHierarchyType.STUDY_PROGRAM
        assert edge.parent_url
        assert edge.content is not None
        assert isinstance(edge.content, bytes), (
            "Content of edge should be bytes {0}".format(type(edge.content))
        )

        return StudyProgram(
            id=generate_id(edge.url),
            url=edge.url,
            parent_id=generate_id(edge.parent_url),
            title=edge.title,
            content=edge.content,
            checksum=sha256(edge.content).hexdigest(),
        )
