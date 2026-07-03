# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Protocol, Optional
from app.domain.model.study_program import StudyProgram


class StudyProgramRepository(Protocol):
    def find_study_program_by_url(self, url: str) -> Optional[StudyProgram]:
        pass

    def save_study_program(self, study_program: StudyProgram) -> StudyProgram:
        pass

    def find_study_program_by_id(self, id: int) -> Optional[StudyProgram]:
        pass

    def list_study_programs(
        self, study_program_ref_id: Optional[int] = None
    ) -> list[StudyProgram]:
        pass
