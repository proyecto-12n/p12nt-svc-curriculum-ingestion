# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from datetime import datetime
from pydantic import BaseModel
from domain.model.grade_level import GradeLevel


class GradeLevelResponse(BaseModel):
    id: int
    subject_id: int
    url: str
    title: str
    content: str
    extracted_at: datetime

    @classmethod
    def from_domain(cls, grade_level: GradeLevel) -> "GradeLevelResponse":
        return cls(
            id=grade_level.id,
            subject_id=grade_level.subject_id,
            url=grade_level.url,
            title=grade_level.title,
            content=grade_level.content,
            extracted_at=grade_level.extracted_at,
        )
