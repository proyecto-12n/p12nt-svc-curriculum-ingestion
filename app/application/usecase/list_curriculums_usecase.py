# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import asyncio
from typing import List
from app.domain.model.curriculum import Curriculum
from app.domain.port.inbound.list_curriculums_use_case import ListCurriculumsUseCase
from app.domain.port.outbound.curriculum_repository import CurriculumRepository


class ListCurriculumsUseCaseImpl(ListCurriculumsUseCase):
    def __init__(self, curriculum_repository: CurriculumRepository):
        self.curriculum_repository = curriculum_repository

    async def execute(self) -> List[Curriculum]:
        return await asyncio.to_thread(self.curriculum_repository.list_curriculums)
