# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from datetime import datetime
from sqlmodel import Field, SQLModel


class GradeLevel(SQLModel, table=True):
    __tablename__ = "grade_levels"
    __table_args__ = {"schema": "curriculum_ingestion"}

    id: int = Field(primary_key=True)
    url: str = Field(unique=True)
    parent_id: int = Field(foreign_key="curriculum_ingestion.subjects.id")

    title: str
    content: str
    extracted_at: datetime = Field(default_factory=datetime.utcnow)

    def __init__(self, **data):
        if "subject_id" in data and "parent_id" not in data:
            data["parent_id"] = data.pop("subject_id")
        super().__init__(**data)

    @property
    def subject_id(self) -> int:
        return self.parent_id

    @subject_id.setter
    def subject_id(self, value: int) -> None:
        self.parent_id = value
