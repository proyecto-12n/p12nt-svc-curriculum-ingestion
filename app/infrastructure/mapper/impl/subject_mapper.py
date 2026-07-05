# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from domain.model.edge import Edge
from domain.model.resource_type import ResourceType
from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from domain.port.outbound.curriculum_hierarchy_mapper import CurriculumHierarchyMapper
from infrastructure.models import Subject
from infrastructure.util import generate_id


class SubjectMapper(CurriculumHierarchyMapper[Subject, str]):
    def to_edge(self, model: Subject) -> Edge[str]:
        return Edge(
            url=model.url,
            type=ResourceType.HTML,
            hierarchy=CurriculumHierarchyType.SUBJECT,
            title=model.title,
            content=model.content,
        )

    def to_model(self, edge: Edge[str]) -> Subject:
        assert edge.hierarchy == CurriculumHierarchyType.SUBJECT
        assert edge.parent_url
        assert edge.content

        return Subject(
            id=generate_id(edge.url),
            url=edge.url,
            parent_id=generate_id(edge.parent_url),
            title=edge.title,
            content=edge.content,
        )
