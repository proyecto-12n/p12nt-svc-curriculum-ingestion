# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Optional
from sqlmodel import Session, select
from app.domain.port.outbound.grade_level_repository import GradeLevelRepository

# Domain models
from app.domain.model.grade_level import GradeLevel as DomainGradeLevel

# SQLModel models
from app.infrastructure.models.grade_level import GradeLevel as SqlGradeLevel


class SqlGradeLevelRepositoryAdapter(GradeLevelRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_grade_level_by_title_and_subject(
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

    def save_grade_level(self, grade_level: DomainGradeLevel) -> DomainGradeLevel:
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

    def find_grade_level_by_id(self, id: int) -> Optional[DomainGradeLevel]:
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

    def list_grade_levels(
        self, subject_id: Optional[int] = None
    ) -> list[DomainGradeLevel]:
        statement = select(SqlGradeLevel)
        if subject_id is not None:
            statement = statement.where(SqlGradeLevel.subject_id == subject_id)
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
