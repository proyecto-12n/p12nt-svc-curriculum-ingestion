# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from sqlmodel import Field, SQLModel


class GradeLevelStudyProgramRef(SQLModel, table=True):
    __tablename__ = "grade_level_study_program_refs"
    __table_args__ = {"schema": "curriculum_ingestion"}

    grade_level_id: int = Field(
        foreign_key="curriculum_ingestion.grade_levels.id",
        primary_key=True,
    )
    study_program_ref_id: int = Field(
        foreign_key="curriculum_ingestion.study_program_refs.id",
        primary_key=True,
    )
