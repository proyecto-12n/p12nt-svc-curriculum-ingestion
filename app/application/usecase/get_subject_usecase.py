# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import asyncio
from typing import Optional
from app.domain.model.subject import Subject
from app.domain.port.inbound.get_subject_use_case import GetSubjectUseCase
from app.domain.port.outbound.subject_repository import SubjectRepository


class GetSubjectUseCaseImpl(GetSubjectUseCase):
    def __init__(self, subject_repository: SubjectRepository):
        self.subject_repository = subject_repository

    async def execute(self, id: int) -> Optional[Subject]:
        return await asyncio.to_thread(self.subject_repository.find_subject_by_id, id)
