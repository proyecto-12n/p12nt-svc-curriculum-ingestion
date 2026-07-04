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
from infrastructure.models import GradeLevel


class GradeLevelMapper(CurriculumHierarchyMapper[GradeLevel, str]):
    def to_domain_node(self, model: GradeLevel) -> Node[str]:
        return Node(
            url=model.url,
            type=ResourceType.HTML,
            level=CurriculumHierarchyType.GRADE_LEVEL,
            title=model.title,
            content=model.content,
        )
