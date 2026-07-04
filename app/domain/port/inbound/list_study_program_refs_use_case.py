# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Protocol, List, Optional
from domain.model.study_program_ref import StudyProgramRef


class ListStudyProgramRefsUseCase(Protocol):
    async def execute(
        self, grade_level_id: Optional[int] = None
    ) -> List[StudyProgramRef]:
        pass
