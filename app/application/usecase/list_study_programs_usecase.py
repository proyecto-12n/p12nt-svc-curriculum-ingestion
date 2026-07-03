# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import asyncio
from typing import List, Optional
from app.domain.model.study_program import StudyProgram
from app.domain.port.inbound.list_study_programs_use_case import (
    ListStudyProgramsUseCase,
)
from app.domain.port.outbound.study_program_repository import StudyProgramRepository


class ListStudyProgramsUseCaseImpl(ListStudyProgramsUseCase):
    def __init__(self, study_program_repository: StudyProgramRepository):
        self.study_program_repository = study_program_repository

    async def execute(
        self, study_program_ref_id: Optional[int] = None
    ) -> List[StudyProgram]:
        return await asyncio.to_thread(
            self.study_program_repository.list_study_programs, study_program_ref_id
        )
