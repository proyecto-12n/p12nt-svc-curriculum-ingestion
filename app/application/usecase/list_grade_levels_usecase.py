# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import asyncio
from typing import List, Optional
from domain.model.grade_level import GradeLevel
from domain.port.inbound.list_grade_levels_use_case import ListGradeLevelsUseCase
from domain.port.outbound.grade_level_repository import GradeLevelRepository


class ListGradeLevelsUseCaseImpl(ListGradeLevelsUseCase):
    def __init__(self, grade_level_repository: GradeLevelRepository):
        self.grade_level_repository = grade_level_repository

    async def execute(self, subject_id: Optional[int] = None) -> List[GradeLevel]:
        return await asyncio.to_thread(
            self.grade_level_repository.list_grade_levels, subject_id
        )
