# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Protocol, Any

from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from infrastructure.adapter.outbound.db.curriculum_hierarchy_repository import (
    CurriculumHierarchyRepository,
)


class CurriculumHierarchyRepositoryProvider(Protocol):
    def get_repository(
        self, node_type: CurriculumHierarchyType
    ) -> CurriculumHierarchyRepository[Any]:
        """Retrieves a CurriculumHierarchyRepository implementation by CurriculumNodeType."""
        ...
