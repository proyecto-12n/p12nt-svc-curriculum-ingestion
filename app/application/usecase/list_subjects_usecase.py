# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import asyncio
from typing import List, Optional
from app.domain.model.subject import Subject
from app.domain.port.inbound.list_subjects_use_case import ListSubjectsUseCase
from app.domain.port.outbound.subject_repository import SubjectRepository


class ListSubjectsUseCaseImpl(ListSubjectsUseCase):
    def __init__(self, subject_repository: SubjectRepository):
        self.subject_repository = subject_repository

    async def execute(self, modality_id: Optional[int] = None) -> List[Subject]:
        return await asyncio.to_thread(
            self.subject_repository.list_subjects, modality_id
        )
