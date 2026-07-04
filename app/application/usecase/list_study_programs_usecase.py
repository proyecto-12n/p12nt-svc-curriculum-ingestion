# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import List, Optional

from domain.model.study_program import StudyProgram
from domain.port.inbound.list_study_programs_use_case import (
    ListStudyProgramsUseCase,
)
from domain.port.outbound import KnowledgeRepository


class ListStudyProgramsUseCaseImpl(ListStudyProgramsUseCase):
    def __init__(self, study_program_repository: KnowledgeRepository[StudyProgram]):
        self.study_program_repository = study_program_repository

    async def execute(
            self, parent_id: Optional[int] = None
    ) -> List[StudyProgram]:
        return await self.study_program_repository.list(parent_id)
