# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from datetime import UTC, datetime

from sqlalchemy import Column, Text
from sqlmodel import Field, SQLModel


class StudyProgramMarkdown(SQLModel, table=True):
    __tablename__ = "study_program_markdowns"
    __table_args__ = {"schema": "curriculum_ingestion"}

    id: int | None = Field(default=None, primary_key=True)
    study_program_id: int = Field(
        foreign_key="curriculum_ingestion.study_programs.id",
    )
    content: str = Field(sa_column=Column(Text))
    tool_name: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
