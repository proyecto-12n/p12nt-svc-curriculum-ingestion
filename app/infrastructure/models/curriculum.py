# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from sqlmodel import Field, SQLModel


class Curriculum(SQLModel, table=True):
    __tablename__ = "curriculums"
    __table_args__ = {"schema": "curriculum-ingestion"}

    id: int = Field(primary_key=True)
    url: str
    title: str
    content: str = Field(default="")
