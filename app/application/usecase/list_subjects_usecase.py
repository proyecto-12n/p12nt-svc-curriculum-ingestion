# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import List, Optional

from domain.model.subject import Subject
from domain.port.inbound.list_subjects_use_case import ListSubjectsUseCase
from domain.port.outbound import CurriculumHierarchyRepository


class ListSubjectsUseCaseImpl(ListSubjectsUseCase):
    def __init__(self, subject_repository: CurriculumHierarchyRepository[Subject]):
        self.subject_repository = subject_repository

    async def execute(self, parent_id: Optional[int] = None) -> List[Subject]:
        return await self.subject_repository.list(parent_id)
