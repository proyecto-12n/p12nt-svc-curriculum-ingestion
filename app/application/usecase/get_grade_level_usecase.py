# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Optional

from domain.model.grade_level import GradeLevel
from domain.port.inbound.get_grade_level_use_case import GetGradeLevelUseCase
from domain.port.outbound import KnowledgeRepository


class GetGradeLevelUseCaseImpl(GetGradeLevelUseCase):
    def __init__(self, grade_level_repository: KnowledgeRepository[GradeLevel]):
        self.grade_level_repository = grade_level_repository

    async def execute(self, id: int) -> Optional[GradeLevel]:
        return await self.grade_level_repository.find_by_id(id)
