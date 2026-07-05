# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from datetime import datetime
from sqlmodel import Field, SQLModel


class StudyProgramRef(SQLModel, table=True):
    __tablename__ = "study_program_refs"
    __table_args__ = {"schema": "curriculum_ingestion"}

    id: int = Field(primary_key=True)
    url: str = Field(unique=True)
    parent_id: int = Field(foreign_key="curriculum_ingestion.grade_levels.id")

    title: str
    content: str
    extracted_at: datetime = Field(default_factory=datetime.utcnow)

    def __init__(self, **data):
        if "grade_level_id" in data and "parent_id" not in data:
            data["parent_id"] = data.pop("grade_level_id")
        super().__init__(**data)

    @property
    def grade_level_id(self) -> int:
        return self.parent_id

    @grade_level_id.setter
    def grade_level_id(self, value: int) -> None:
        self.parent_id = value
