# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Optional, List
from warnings import deprecated

from sqlmodel import Session, select

from domain.model.grade_level import GradeLevel as DomainGradeLevel
from domain.port.outbound import KnowledgeRepository
from infrastructure.models.grade_level import GradeLevel as SqlGradeLevel


class SqlGradeLevelRepositoryAdapter(KnowledgeRepository[DomainGradeLevel]):
    def __init__(self, session: Session):
        self.session = session

    @deprecated("Use find_by_url instead of find_grade_level_by_title_and_subject")
    async def find_grade_level_by_title_and_subject(
            self, title: str, subject_id: int
    ) -> Optional[DomainGradeLevel]:
        statement = select(SqlGradeLevel).where(
            SqlGradeLevel.title == title, SqlGradeLevel.subject_id == subject_id
        )
        sql_grade = self.session.exec(statement).first()
        if sql_grade:
            return DomainGradeLevel(
                id=sql_grade.id,
                title=sql_grade.title,
                subject_id=sql_grade.subject_id,
                url=sql_grade.url,
                content=sql_grade.content,
                extracted_at=sql_grade.extracted_at,
            )
        return None

    async def save(self, grade_level: DomainGradeLevel) -> DomainGradeLevel:
        statement = select(SqlGradeLevel).where(
            SqlGradeLevel.title == grade_level.title,
            SqlGradeLevel.subject_id == grade_level.subject_id,
        )
        sql_grade = self.session.exec(statement).first()
        if sql_grade:
            sql_grade.url = grade_level.url
            sql_grade.content = grade_level.content
            sql_grade.extracted_at = grade_level.extracted_at
        else:
            sql_grade = SqlGradeLevel(
                title=grade_level.title,
                subject_id=grade_level.subject_id,
                url=grade_level.url,
                content=grade_level.content,
                extracted_at=grade_level.extracted_at,
            )
            self.session.add(sql_grade)
        self.session.commit()
        self.session.refresh(sql_grade)
        grade_level.id = sql_grade.id
        return grade_level

    async def find_by_url(self, url: str) -> Optional[DomainGradeLevel]:
        statement = select(SqlGradeLevel).where(SqlGradeLevel.url == url)
        sql_grade = self.session.exec(statement).first()
        if sql_grade:
            return DomainGradeLevel(
                id=sql_grade.id,
                title=sql_grade.title,
                subject_id=sql_grade.subject_id,
                url=sql_grade.url,
                content=sql_grade.content,
                extracted_at=sql_grade.extracted_at,
            )
        return None

    async def find_by_id(self, id: int) -> Optional[DomainGradeLevel]:
        statement = select(SqlGradeLevel).where(SqlGradeLevel.id == id)
        sql_grade = self.session.exec(statement).first()
        if sql_grade:
            return DomainGradeLevel(
                id=sql_grade.id,
                title=sql_grade.title,
                subject_id=sql_grade.subject_id,
                url=sql_grade.url,
                content=sql_grade.content,
                extracted_at=sql_grade.extracted_at,
            )
        return None

    async def list(
            self, parent_id: Optional[int] = None
    ) -> List[DomainGradeLevel]:
        statement = select(SqlGradeLevel)
        if parent_id is not None:
            statement = statement.where(SqlGradeLevel.subject_id == parent_id)
        results = self.session.exec(statement).all()
        return [
            DomainGradeLevel(
                id=row.id,
                title=row.title,
                subject_id=row.subject_id,
                url=row.url,
                content=row.content,
                extracted_at=row.extracted_at,
            )
            for row in results
        ]
