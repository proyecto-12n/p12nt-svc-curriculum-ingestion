# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from sqlmodel import Field, SQLModel


class StudyProgramRef(SQLModel, table=True):
    __tablename__ = "study_program_refs"
    __table_args__ = {"schema": "curriculum-ingestion"}

    id: int = Field(primary_key=True)
    grade_level_id: int = Field(foreign_key="curriculum-ingestion.grade_levels.id")
    url: str
    content: str
