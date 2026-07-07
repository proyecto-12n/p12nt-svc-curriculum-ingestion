# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from datetime import datetime
from pydantic import BaseModel
from domain.model.study_program_ref import StudyProgramRef


class StudyProgramRefResponse(BaseModel):
    id: int
    grade_level_id: int
    url: str
    title: str
    content: str
    extracted_at: datetime

    @classmethod
    def from_domain(cls, ref: StudyProgramRef) -> "StudyProgramRefResponse":
        return cls(
            id=ref.id,
            grade_level_id=(
                ref.grade_level_id
                if hasattr(ref, "grade_level_id")
                else getattr(
                    ref,
                    "_grade_level_id",
                    ref.grade_levels[0].id if ref.grade_levels else None,
                )
            ),
            url=ref.url,
            title=ref.title,
            content=ref.content,
            extracted_at=ref.extracted_at,
        )
