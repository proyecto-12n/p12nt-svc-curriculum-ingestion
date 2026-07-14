# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from datetime import datetime
from pydantic import BaseModel
from domain.model.subject import Subject


class SubjectResponse(BaseModel):
    id: int
    curriculum_framework_id: int
    url: str
    title: str
    content: str
    extracted_at: datetime

    @classmethod
    def from_domain(cls, subject: Subject) -> "SubjectResponse":
        return cls(
            id=subject.id,
            curriculum_framework_id=(
                subject.curriculum_framework_id
                if hasattr(subject, "curriculum_framework_id")
                else subject.parent_id
            ),
            url=subject.url,
            title=subject.title,
            content=subject.content,
            extracted_at=subject.extracted_at,
        )
