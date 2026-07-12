# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Optional, List

from sqlmodel import Session, select

from infrastructure.adapter.outbound.db import (
    CurriculumHierarchyRepository,
    CurriculumHierarchyRepositoryHelper,
)
from infrastructure.models.grade_level import GradeLevel


class SqlGradeLevelRepositoryAdapter(CurriculumHierarchyRepository[GradeLevel]):
    def __init__(self, session: Session):
        self.session = session

    async def save(self, grade_level: GradeLevel) -> GradeLevel:
        statement = select(GradeLevel).where(
            (GradeLevel.url == grade_level.url) | (GradeLevel.id == grade_level.id)
        )
        return CurriculumHierarchyRepositoryHelper.save_hierarchy_model(
            self.session,
            grade_level,
            statement,
            ("url", "parent_id", "title", "content", "extracted_at"),
        )

    async def find_by_url(self, url: str) -> Optional[GradeLevel]:
        statement = select(GradeLevel).where(GradeLevel.url == url)
        return self.session.exec(statement).first()

    async def find_by_id(self, id: int) -> Optional[GradeLevel]:
        statement = select(GradeLevel).where(GradeLevel.id == id)
        return self.session.exec(statement).first()

    async def find_grade_level_by_title_and_subject(
        self, title: str, subject_id: int
    ) -> Optional[GradeLevel]:
        statement = select(GradeLevel).where(
            GradeLevel.title == title, GradeLevel.parent_id == subject_id
        )
        return self.session.exec(statement).first()

    async def list(self, parent_id: Optional[int] = None) -> List[GradeLevel]:
        statement = select(GradeLevel).order_by(GradeLevel.title)
        if parent_id is not None:
            statement = statement.where(GradeLevel.parent_id == parent_id)
        results = self.session.exec(statement).all()
        return [row for row in results]
