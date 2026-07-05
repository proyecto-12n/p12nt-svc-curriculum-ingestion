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
from infrastructure.models.curriculum import Curriculum
from infrastructure.util import generate_id


class CurriculumMapper(CurriculumHierarchyMapper[Curriculum, str]):
    def to_edge(self, model: Curriculum) -> Edge[str]:
        return Edge(
            url=model.url,
            type=ResourceType.HTML,
            hierarchy=CurriculumHierarchyType.CURRICULUM,
            title=model.title,
            content=model.content,
        )

    def to_model(self, edge: Edge[str]) -> Curriculum:
        assert edge.hierarchy == CurriculumHierarchyType.CURRICULUM
        assert edge.parent_url is None
        assert edge.content

        return Curriculum(
            id=generate_id(edge.url),
            url=edge.url,
            title=edge.title,
            content=edge.content,
        )
