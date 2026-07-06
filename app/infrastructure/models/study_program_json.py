# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from datetime import UTC, datetime
from typing import Any

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


class StudyProgramJson(SQLModel, table=True):
    __tablename__ = "study_program_jsons"
    __table_args__ = {"schema": "curriculum_ingestion"}

    id: int | None = Field(default=None, primary_key=True)
    study_program_id: int = Field(
        foreign_key="curriculum_ingestion.study_programs.id",
    )
    content: dict[str, Any] = Field(sa_column=Column(JSONB))
    tool_name: str
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
