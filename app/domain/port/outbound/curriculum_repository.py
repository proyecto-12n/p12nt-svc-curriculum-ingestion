# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Protocol, Optional
from app.domain.model.modality import Modality
from app.domain.model.subject import Subject
from app.domain.model.grade_level import GradeLevel
from app.domain.model.study_program_ref import StudyProgramRef
from app.domain.model.study_program import StudyProgram


class CurriculumRepository(Protocol):
    def find_modality_by_url(self, url: str) -> Optional[Modality]:
        pass

    def save_modality(self, modality: Modality) -> Modality:
        pass

    def find_subject_by_title_and_modality(
        self, title: str, modality_id: int
    ) -> Optional[Subject]:
        pass

    def save_subject(self, subject: Subject) -> Subject:
        pass

    def find_grade_level_by_title_and_subject(
        self, title: str, subject_id: int
    ) -> Optional[GradeLevel]:
        pass

    def save_grade_level(self, grade_level: GradeLevel) -> GradeLevel:
        pass

    def find_study_program_ref_by_url(self, url: str) -> Optional[StudyProgramRef]:
        pass

    def save_study_program_ref(
        self, study_program_ref: StudyProgramRef
    ) -> StudyProgramRef:
        pass

    def find_study_program_by_url(self, url: str) -> Optional[StudyProgram]:
        pass

    def save_study_program(self, study_program: StudyProgram) -> StudyProgram:
        pass
