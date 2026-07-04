# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import List

from domain.model.curriculum import Curriculum
from domain.port.inbound.list_curriculums_use_case import ListCurriculumsUseCase
from domain.port.outbound.curriculum_hierarchy_repository import (
    CurriculumHierarchyRepository,
)


class ListCurriculumsUseCaseImpl(ListCurriculumsUseCase):
    def __init__(
        self, curriculum_repository: CurriculumHierarchyRepository[Curriculum]
    ):
        self.curriculum_repository = curriculum_repository

    async def execute(self) -> List[Curriculum]:
        return await self.curriculum_repository.list()
