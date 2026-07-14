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
from infrastructure.models import Modality
from infrastructure.util import generate_id


class ModalityMapper(CurriculumHierarchyMapper[Modality, str]):
    def to_edge(self, model: Modality) -> Edge[str]:
        return Edge(
            url=model.url,
            type=ResourceType.HTML,
            hierarchy=CurriculumHierarchyType.MODALITY,
            title=model.title,
            content=model.content,
        )

    def to_model(self, edge: Edge[str]) -> Modality:
        assert edge.hierarchy == CurriculumHierarchyType.MODALITY
        assert edge.parent_url
        assert edge.content

        return Modality(
            id=generate_id(edge.url),
            url=edge.url,
            curriculum_id=generate_id(edge.parent_url),
            title=edge.title,
            content=edge.content,
        )
