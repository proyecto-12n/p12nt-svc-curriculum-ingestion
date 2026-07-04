# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import List, TypeVar, Optional

from domain.port.inbound.list_curriculum_hierarchy_item_use_case import (
    ListCurriculumHierarchyItemUseCase,
)
from domain.port.outbound.curriculum_hierarchy_repository import (
    CurriculumHierarchyRepository,
)

K = TypeVar("K")


class ListCurriculumHierarchyItemUseCaseImpl(ListCurriculumHierarchyItemUseCase[K]):
    def __init__(self, repository: CurriculumHierarchyRepository[K]):
        self.repository = repository

    async def execute(self, parent_id: Optional[int] = None) -> List[K]:
        return await self.repository.list(parent_id)
