# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class StudyProgram(SQLModel, table=True):
    __tablename__ = "study_programs"
    __table_args__ = {"schema": "curriculum-ingestion"}

    id: Optional[int] = Field(default=None, primary_key=True)
    url: str
    study_program_ref_id: int = Field(
        foreign_key="curriculum-ingestion.study_program_refs.id"
    )
    md5sum: str
    content: bytes
    status: str = Field(default="PENDING")
    error_log: Optional[str] = None
    extracted_at: datetime = Field(default_factory=datetime.utcnow)
    version: str = Field(default="1.0")
