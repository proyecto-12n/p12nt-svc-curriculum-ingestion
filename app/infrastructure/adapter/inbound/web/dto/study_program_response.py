# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import base64
from datetime import datetime
from pydantic import BaseModel
from domain.model.study_program import StudyProgram


class StudyProgramResponse(BaseModel):
    id: int
    study_program_ref_id: int
    url: str
    title: str
    content: str  # base64 encoded string
    checksum: str
    extracted_at: datetime

    @classmethod
    def from_domain(cls, program: StudyProgram) -> "StudyProgramResponse":
        content_b64 = base64.b64encode(program.content).decode("utf-8")
        return cls(
            id=program.id,
            study_program_ref_id=program.study_program_ref_id,
            url=program.url,
            title=program.title,
            content=content_b64,
            checksum=program.checksum,
            extracted_at=program.extracted_at,
        )
