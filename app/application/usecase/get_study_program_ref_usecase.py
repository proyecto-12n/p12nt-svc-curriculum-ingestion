# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import asyncio
from typing import Optional
from app.domain.model.study_program_ref import StudyProgramRef
from app.domain.port.inbound.get_study_program_ref_use_case import (
    GetStudyProgramRefUseCase,
)
from app.domain.port.outbound.study_program_ref_repository import (
    StudyProgramRefRepository,
)


class GetStudyProgramRefUseCaseImpl(GetStudyProgramRefUseCase):
    def __init__(self, study_program_ref_repository: StudyProgramRefRepository):
        self.study_program_ref_repository = study_program_ref_repository

    async def execute(self, id: int) -> Optional[StudyProgramRef]:
        return await asyncio.to_thread(
            self.study_program_ref_repository.find_study_program_ref_by_id, id
        )
