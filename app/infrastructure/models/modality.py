# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from datetime import UTC, datetime
from sqlmodel import Field, SQLModel


class Modality(SQLModel, table=True):
    __tablename__ = "modalities"
    __table_args__ = {"schema": "curriculum_ingestion"}

    id: int = Field(primary_key=True)
    url: str = Field(unique=True)
    parent_id: int = Field(foreign_key="curriculum_ingestion.curriculums.id")

    title: str
    content: str
    extracted_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
