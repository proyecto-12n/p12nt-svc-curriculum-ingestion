# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import asyncio
from typing import List, Optional
from domain.model.study_program_ref import StudyProgramRef
from domain.port.inbound.list_study_program_refs_use_case import (
    ListStudyProgramRefsUseCase,
)
from domain.port.outbound.study_program_ref_repository import (
    StudyProgramRefRepository,
)


class ListStudyProgramRefsUseCaseImpl(ListStudyProgramRefsUseCase):
    def __init__(self, study_program_ref_repository: StudyProgramRefRepository):
        self.study_program_ref_repository = study_program_ref_repository

    async def execute(
        self, grade_level_id: Optional[int] = None
    ) -> List[StudyProgramRef]:
        return await asyncio.to_thread(
            self.study_program_ref_repository.list_study_program_refs, grade_level_id
        )
