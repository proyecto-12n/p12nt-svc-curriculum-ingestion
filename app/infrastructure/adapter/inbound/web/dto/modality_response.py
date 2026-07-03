# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from datetime import datetime
from pydantic import BaseModel
from app.domain.model.modality import Modality


class ModalityResponse(BaseModel):
    id: int
    curriculum_id: int
    url: str
    title: str
    content: str
    extracted_at: datetime

    @classmethod
    def from_domain(cls, modality: Modality) -> "ModalityResponse":
        return cls(
            id=modality.id,
            curriculum_id=modality.curriculum_id,
            url=modality.url,
            title=modality.title,
            content=modality.content,
            extracted_at=modality.extracted_at,
        )
