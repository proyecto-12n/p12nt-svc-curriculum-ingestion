# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from infrastructure.models.modality import Modality


class Curriculum(SQLModel, table=True):
    __tablename__ = "curriculums"
    __table_args__ = {"schema": "curriculum_ingestion"}

    id: int = Field(primary_key=True)
    url: str = Field(unique=True)
    title: str
    content: str
    extracted_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    modalities: Mapped[list["Modality"]] = Relationship(back_populates="curriculum")
