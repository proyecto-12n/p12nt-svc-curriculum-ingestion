# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Optional
from sqlmodel import Field, SQLModel


class Modality(SQLModel, table=True):
    __tablename__ = "modalities"
    __table_args__ = {"schema": "curriculum-ingestion"}

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    url: str
