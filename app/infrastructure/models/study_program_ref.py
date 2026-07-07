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

from infrastructure.models.grade_level_study_program_ref import (
    GradeLevelStudyProgramRef,
)

if TYPE_CHECKING:
    from infrastructure.models.grade_level import GradeLevel
    from infrastructure.models.study_program import StudyProgram


class StudyProgramRef(SQLModel, table=True):
    __tablename__ = "study_program_refs"
    __table_args__ = {"schema": "curriculum_ingestion"}

    id: int = Field(primary_key=True)
    url: str = Field(unique=True)

    title: str
    content: str
    extracted_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    grade_levels: Mapped[list["GradeLevel"]] = Relationship(
        back_populates="study_program_refs",
        link_model=GradeLevelStudyProgramRef,
    )

    study_programs: Mapped[list["StudyProgram"]] = Relationship(
        back_populates="study_program_ref"
    )
