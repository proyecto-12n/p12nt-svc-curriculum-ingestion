# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from datetime import datetime
from sqlmodel import Field, SQLModel


class Curriculum(SQLModel, table=True):
    __tablename__ = "curriculums"
    __table_args__ = {"schema": "curriculum_ingestion"}

    id: int = Field(primary_key=True)
    url: str = Field(unique=True)
    title: str
    content: str
    extracted_at: datetime = Field(default_factory=datetime.utcnow)
