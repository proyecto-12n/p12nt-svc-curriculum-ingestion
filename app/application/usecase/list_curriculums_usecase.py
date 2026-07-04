# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import asyncio
from typing import List

from domain.model.curriculum import Curriculum
from domain.port.inbound.list_curriculums_use_case import ListCurriculumsUseCase
from domain.port.outbound.knowledge_repository import KnowledgeRepository


class ListCurriculumsUseCaseImpl(ListCurriculumsUseCase):
    def __init__(self, curriculum_repository: KnowledgeRepository[Curriculum]):
        self.curriculum_repository = curriculum_repository

    async def execute(self) -> List[Curriculum]:
        return await asyncio.to_thread(self.curriculum_repository.list)
