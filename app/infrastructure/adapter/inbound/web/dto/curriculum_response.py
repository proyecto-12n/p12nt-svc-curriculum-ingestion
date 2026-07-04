# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from datetime import datetime
from pydantic import BaseModel
from domain.model.curriculum import Curriculum


class CurriculumResponse(BaseModel):
    id: int
    url: str
    title: str
    content: str
    extracted_at: datetime

    @classmethod
    def from_domain(cls, curriculum: Curriculum) -> "CurriculumResponse":
        return cls(
            id=curriculum.id,
            url=curriculum.url,
            title=curriculum.title,
            content=curriculum.content,
            extracted_at=curriculum.extracted_at,
        )
