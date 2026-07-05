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
from infrastructure.models.subject import Subject


class SqlSubjectRepositoryAdapter(CurriculumHierarchyRepository[Subject]):
    def __init__(self, session: Session):
        self.session = session

    async def find_by_id(self, id: int) -> Optional[Subject]:
        statement = select(Subject).where(Subject.id == id)
        return self.session.exec(statement).first()

    async def find_by_url(self, url: str) -> Optional[Subject]:
        statement = select(Subject).where(Subject.url == url)
        return self.session.exec(statement).first()

    async def list(self, modality_id: Optional[int] = None) -> List[Subject]:
        statement = select(Subject)
        if modality_id is not None:
            statement = statement.where(Subject.parent_id == modality_id)
        results = self.session.exec(statement).all()
        return [row for row in results]

    async def save(self, subject: Subject) -> Subject:
        statement = select(Subject).where(Subject.url == subject.url)
        sql_sub = self.session.exec(statement).first()
        if sql_sub:
            sql_sub.parent_id = subject.parent_id
            sql_sub.title = subject.title
            sql_sub.content = subject.content
            sql_sub.extracted_at = subject.extracted_at
        else:
            sql_sub = Subject(
                id=subject.id,
                url=subject.url,
                parent_id=subject.parent_id,
                title=subject.title,
                content=subject.content,
                extracted_at=subject.extracted_at,
            )
            self.session.add(sql_sub)
        self.session.commit()
        self.session.refresh(sql_sub)
        subject.id = sql_sub.id
        return subject
