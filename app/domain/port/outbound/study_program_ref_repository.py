# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Protocol, Optional
from app.domain.model.study_program_ref import StudyProgramRef


class StudyProgramRefRepository(Protocol):
    def find_study_program_ref_by_url(self, url: str) -> Optional[StudyProgramRef]:
        pass

    def save_study_program_ref(
        self, study_program_ref: StudyProgramRef
    ) -> StudyProgramRef:
        pass
