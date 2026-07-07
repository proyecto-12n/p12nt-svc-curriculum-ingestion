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
    from infrastructure.models.study_program_ref import StudyProgramRef
    from infrastructure.models.subject import Subject


class GradeLevel(SQLModel, table=True):
    __tablename__ = "grade_levels"
    __table_args__ = {"schema": "curriculum_ingestion"}

    id: int = Field(primary_key=True)
    url: str = Field(unique=True)
    parent_id: int = Field(foreign_key="curriculum_ingestion.subjects.id")

    title: str
    content: str
    extracted_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    subject: Mapped["Subject"] = Relationship(back_populates="grade_levels")

    study_program_refs: Mapped[list["StudyProgramRef"]] = Relationship(
        back_populates="grade_levels",
        link_model=GradeLevelStudyProgramRef,
    )
