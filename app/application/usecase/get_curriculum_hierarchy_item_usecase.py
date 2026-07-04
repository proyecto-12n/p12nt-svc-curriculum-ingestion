# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Optional, TypeVar

from domain.port.inbound.get_curriculum_hierarchy_item_use_case import (
    GetCurriculumHierarchyItemUseCase,
)
from domain.port.outbound.curriculum_hierarchy_repository import (
    CurriculumHierarchyRepository,
)

K = TypeVar("K")


class GetCurriculumHierarchyItemUseCaseImpl(GetCurriculumHierarchyItemUseCase[K]):
    def __init__(self, repository: CurriculumHierarchyRepository[K]):
        self.repository = repository

    async def execute(self, id: int) -> Optional[K]:
        return await self.repository.find_by_id(id)
