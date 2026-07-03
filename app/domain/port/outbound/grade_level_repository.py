# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Protocol, Optional
from app.domain.model.grade_level import GradeLevel


class GradeLevelRepository(Protocol):
    def find_grade_level_by_title_and_subject(
        self, title: str, subject_id: int
    ) -> Optional[GradeLevel]:
        pass

    def save_grade_level(self, grade_level: GradeLevel) -> GradeLevel:
        pass
