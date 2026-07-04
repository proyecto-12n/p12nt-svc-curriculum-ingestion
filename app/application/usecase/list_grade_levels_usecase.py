# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import List, Optional

from domain.model.grade_level import GradeLevel
from domain.port.inbound.list_grade_levels_use_case import ListGradeLevelsUseCase
from domain.port.outbound import KnowledgeRepository


class ListGradeLevelsUseCaseImpl(ListGradeLevelsUseCase):
    def __init__(self, grade_level_repository: KnowledgeRepository[GradeLevel]):
        self.grade_level_repository = grade_level_repository

    async def execute(self, parent_id: Optional[int] = None) -> List[GradeLevel]:
        return await self.grade_level_repository.list(parent_id)
