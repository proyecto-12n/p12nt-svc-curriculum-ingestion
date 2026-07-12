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
from infrastructure.models import CurriculumFramework
from infrastructure.util import generate_id


class CurriculumFrameworkMapper(CurriculumHierarchyMapper[CurriculumFramework, str]):
    def to_edge(self, model: CurriculumFramework) -> Edge[str]:
        return Edge(
            url=model.url,
            type=ResourceType.HTML,
            hierarchy=CurriculumHierarchyType.CURRICULUM_FRAMEWORK,
            title=model.title,
            content=model.content,
        )

    def to_model(self, edge: Edge[str]) -> CurriculumFramework:
        assert edge.hierarchy == CurriculumHierarchyType.CURRICULUM_FRAMEWORK
        assert edge.parent_url
        assert edge.content

        return CurriculumFramework(
            id=generate_id(edge.url),
            url=edge.url,
            parent_id=generate_id(edge.parent_url),
            title=edge.title,
            content=edge.content,
        )
