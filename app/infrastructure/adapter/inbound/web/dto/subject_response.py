# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from datetime import datetime
from pydantic import BaseModel
from domain.model.subject import Subject


class SubjectResponse(BaseModel):
    id: int
    modality_id: int
    url: str
    title: str
    content: str
    extracted_at: datetime

    @classmethod
    def from_domain(cls, subject: Subject) -> "SubjectResponse":
        return cls(
            id=subject.id,
            modality_id=subject.modality_id,
            url=subject.url,
            title=subject.title,
            content=subject.content,
            extracted_at=subject.extracted_at,
        )
