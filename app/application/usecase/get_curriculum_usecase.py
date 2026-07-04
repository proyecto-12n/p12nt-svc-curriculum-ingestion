# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Optional
from domain.model.curriculum import Curriculum
from domain.port.inbound.get_curriculum_use_case import GetCurriculumUseCase
from domain.port.outbound.curriculum_hierarchy_repository import (
    CurriculumHierarchyRepository,
)


class GetCurriculumUseCaseImpl(GetCurriculumUseCase):
    def __init__(
        self, curriculum_repository: CurriculumHierarchyRepository[Curriculum]
    ):
        self.curriculum_repository = curriculum_repository

    async def execute(self, id: int) -> Optional[Curriculum]:
        return await self.curriculum_repository.find_by_id(id)
