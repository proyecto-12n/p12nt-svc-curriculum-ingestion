# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Protocol, Any

from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from domain.port.outbound.curriculum_hierarchy_mapper import CurriculumHierarchyMapper


class CurriculumHierarchyMapperProvider(Protocol):
    def get_mapper(
        self, node_type: CurriculumHierarchyType
    ) -> CurriculumHierarchyMapper[Any, Any]:
        """Retrieves a CurriculumHierarchyMapper implementation by CurriculumNodeType."""
        ...
