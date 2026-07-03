# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import asyncio
from typing import Optional
from app.domain.model.study_program import StudyProgram
from app.domain.port.inbound.get_study_program_use_case import GetStudyProgramUseCase
from app.domain.port.outbound.study_program_repository import StudyProgramRepository


class GetStudyProgramUseCaseImpl(GetStudyProgramUseCase):
    def __init__(self, study_program_repository: StudyProgramRepository):
        self.study_program_repository = study_program_repository

    async def execute(self, id: int) -> Optional[StudyProgram]:
        return await asyncio.to_thread(
            self.study_program_repository.find_study_program_by_id, id
        )
