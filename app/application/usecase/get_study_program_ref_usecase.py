# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Optional

from domain.model.study_program_ref import StudyProgramRef
from domain.port.inbound.get_study_program_ref_use_case import (
    GetStudyProgramRefUseCase,
)
from domain.port.outbound import KnowledgeRepository


class GetStudyProgramRefUseCaseImpl(GetStudyProgramRefUseCase):
    def __init__(self, study_program_ref_repository: KnowledgeRepository[StudyProgramRef]):
        self.study_program_ref_repository = study_program_ref_repository

    async def execute(self, id: int) -> Optional[StudyProgramRef]:
        return await self.study_program_ref_repository.find_by_id(id)
