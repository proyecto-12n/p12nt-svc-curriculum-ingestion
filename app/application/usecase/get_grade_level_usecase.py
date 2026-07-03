# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import asyncio
from typing import Optional
from app.domain.model.grade_level import GradeLevel
from app.domain.port.inbound.get_grade_level_use_case import GetGradeLevelUseCase
from app.domain.port.outbound.grade_level_repository import GradeLevelRepository


class GetGradeLevelUseCaseImpl(GetGradeLevelUseCase):
    def __init__(self, grade_level_repository: GradeLevelRepository):
        self.grade_level_repository = grade_level_repository

    async def execute(self, id: int) -> Optional[GradeLevel]:
        return await asyncio.to_thread(
            self.grade_level_repository.find_grade_level_by_id, id
        )
