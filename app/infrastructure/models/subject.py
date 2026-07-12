# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from datetime import UTC, datetime
from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from infrastructure.models.grade_level import GradeLevel
    from infrastructure.models.curriculum_framework import CurriculumFramework


class Subject(SQLModel, table=True):
    __tablename__ = "subjects"
    __table_args__ = {"schema": "curriculum_ingestion"}

    id: int = Field(primary_key=True)
    url: str = Field(unique=True)
    parent_id: int = Field(foreign_key="curriculum_ingestion.curriculum_frameworks.id")

    title: str
    content: str
    extracted_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    curriculum_framework: Mapped["CurriculumFramework"] = Relationship(
        back_populates="subjects"
    )

    grade_levels: Mapped[List["GradeLevel"]] = Relationship(back_populates="subject")
