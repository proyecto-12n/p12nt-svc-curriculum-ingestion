# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from infrastructure.models.study_program_ref import StudyProgramRef


class StudyProgram(SQLModel, table=True):
    __tablename__ = "study_programs"
    __table_args__ = {"schema": "curriculum_ingestion"}

    id: int = Field(primary_key=True)
    url: str = Field(unique=True)
    parent_id: int = Field(foreign_key="curriculum_ingestion.study_program_refs.id")

    title: str
    content: bytes
    checksum: str
    extracted_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    study_program_ref: Mapped["StudyProgramRef"] = Relationship(
        back_populates="study_programs"
    )
