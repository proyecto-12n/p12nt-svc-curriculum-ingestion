# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from sqlmodel import Field, SQLModel


class GradeLevel(SQLModel, table=True):
    __tablename__ = "grade_levels"
    __table_args__ = {"schema": "curriculum-ingestion"}

    id: int = Field(primary_key=True)
    subject_id: int = Field(foreign_key="curriculum-ingestion.subjects.id")
    title: str
    content: str = Field(default="")
