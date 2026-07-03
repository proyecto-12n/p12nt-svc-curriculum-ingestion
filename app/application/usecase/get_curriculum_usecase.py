# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import asyncio
from typing import Optional
from app.domain.model.curriculum import Curriculum
from app.domain.port.inbound.get_curriculum_use_case import GetCurriculumUseCase
from app.domain.port.outbound.curriculum_repository import CurriculumRepository


class GetCurriculumUseCaseImpl(GetCurriculumUseCase):
    def __init__(self, curriculum_repository: CurriculumRepository):
        self.curriculum_repository = curriculum_repository

    async def execute(self, id: int) -> Optional[Curriculum]:
        return await asyncio.to_thread(
            self.curriculum_repository.find_curriculum_by_id, id
        )
