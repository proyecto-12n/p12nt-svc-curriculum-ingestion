# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Optional

from domain.model.study_program import StudyProgram
from domain.port.inbound.get_study_program_use_case import GetStudyProgramUseCase
from domain.port.outbound import CurriculumHierarchyRepository


class GetStudyProgramUseCaseImpl(GetStudyProgramUseCase):
    def __init__(
        self, study_program_repository: CurriculumHierarchyRepository[StudyProgram]
    ):
        self.study_program_repository = study_program_repository

    async def execute(self, id: int) -> Optional[StudyProgram]:
        return await self.study_program_repository.find_by_id(id)
