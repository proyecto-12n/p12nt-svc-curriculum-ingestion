# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from sqlmodel import Field, SQLModel


class Subject(SQLModel, table=True):
    __tablename__ = "subjects"
    __table_args__ = {"schema": "curriculum-ingestion"}

    id: int = Field(primary_key=True)
    title: str
    modality_id: int = Field(foreign_key="curriculum-ingestion.modalities.id")
    url: str
    content: str = Field(default="")
