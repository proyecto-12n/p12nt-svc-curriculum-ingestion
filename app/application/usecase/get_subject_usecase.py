# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Optional

from domain.model.subject import Subject
from domain.port.inbound.get_subject_use_case import GetSubjectUseCase
from domain.port.outbound import KnowledgeRepository


class GetSubjectUseCaseImpl(GetSubjectUseCase):
    def __init__(self, subject_repository: KnowledgeRepository[Subject]):
        self.subject_repository = subject_repository

    async def execute(self, id: int) -> Optional[Subject]:
        return await self.subject_repository.find_by_id(id)
