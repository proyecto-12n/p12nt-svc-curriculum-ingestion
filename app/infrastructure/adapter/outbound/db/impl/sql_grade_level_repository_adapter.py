# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Optional, List

from sqlmodel import Session, select

from infrastructure.adapter.outbound.db import CurriculumHierarchyRepository
from infrastructure.models.grade_level import GradeLevel


class SqlGradeLevelRepositoryAdapter(CurriculumHierarchyRepository[GradeLevel]):
    def __init__(self, session: Session):
        self.session = session

    async def save(self, grade_level: GradeLevel) -> GradeLevel:
        statement = select(GradeLevel).where(GradeLevel.url == grade_level.url)
        sql_grade = self.session.exec(statement).first()
        if sql_grade:
            sql_grade.parent_id = grade_level.parent_id
            sql_grade.title = grade_level.title
            sql_grade.content = grade_level.content
            sql_grade.extracted_at = grade_level.extracted_at
        else:
            sql_grade = GradeLevel(
                id=grade_level.id,
                url=grade_level.url,
                parent_id=grade_level.parent_id,
                title=grade_level.title,
                content=grade_level.content,
                extracted_at=grade_level.extracted_at,
            )
            self.session.add(sql_grade)
        self.session.commit()
        self.session.refresh(sql_grade)
        grade_level.id = sql_grade.id
        return grade_level

    async def find_by_url(self, url: str) -> Optional[GradeLevel]:
        statement = select(GradeLevel).where(GradeLevel.url == url)
        return self.session.exec(statement).first()

    async def find_by_id(self, id: int) -> Optional[GradeLevel]:
        statement = select(GradeLevel).where(GradeLevel.id == id)
        return self.session.exec(statement).first()

    async def list(self, parent_id: Optional[int] = None) -> List[GradeLevel]:
        statement = select(GradeLevel)
        if parent_id is not None:
            statement = statement.where(GradeLevel.parent_id == parent_id)
        results = self.session.exec(statement).all()
        return [row for row in results]
