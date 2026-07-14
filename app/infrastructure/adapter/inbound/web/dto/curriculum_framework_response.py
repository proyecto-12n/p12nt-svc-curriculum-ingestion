# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from datetime import datetime

from domain.model.curriculum_framework import CurriculumFramework
from pydantic import BaseModel


class CurriculumFrameworkResponse(BaseModel):
    id: int
    curriculum_id: int
    url: str
    title: str
    content: str
    extracted_at: datetime

    @classmethod
    def from_domain(
        cls, curriculum_framework: CurriculumFramework
    ) -> "CurriculumFrameworkResponse":
        return cls(
            id=curriculum_framework.id,
            curriculum_id=(
                curriculum_framework.curriculum_id
                if hasattr(curriculum_framework, "curriculum_id")
                else curriculum_framework.parent_id
            ),
            url=curriculum_framework.url,
            title=curriculum_framework.title,
            content=curriculum_framework.content,
            extracted_at=curriculum_framework.extracted_at,
        )
