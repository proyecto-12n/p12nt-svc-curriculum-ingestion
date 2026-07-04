# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Protocol, Optional
from domain.model.study_program_ref import StudyProgramRef


class GetStudyProgramRefUseCase(Protocol):
    async def execute(self, id: int) -> Optional[StudyProgramRef]:
        pass
