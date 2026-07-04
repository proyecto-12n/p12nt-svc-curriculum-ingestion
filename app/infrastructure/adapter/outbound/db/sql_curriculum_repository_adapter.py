# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Optional, List

from sqlmodel import Session, select

from domain.model.curriculum import Curriculum as DomainCurriculum
from infrastructure.models.curriculum import Curriculum as SqlCurriculum
from domain.port.outbound.knowledge_repository import KnowledgeRepository


class SqlCurriculumRepositoryAdapter(KnowledgeRepository[DomainCurriculum]):
    def __init__(self, session: Session):
        self.session = session

    def find_by_id(self, id: int) -> Optional[DomainCurriculum]:
        statement = select(SqlCurriculum).where(SqlCurriculum.id == id)
        sql_cur = self.session.exec(statement).first()
        if sql_cur:
            return DomainCurriculum(
                id=sql_cur.id,
                url=sql_cur.url,
                title=sql_cur.title,
                content=sql_cur.content,
                extracted_at=sql_cur.extracted_at,
            )
        return None

    def find_by_url(self, url: str) -> Optional[DomainCurriculum]:
        statement = select(SqlCurriculum).where(SqlCurriculum.url == url)
        sql_cur = self.session.exec(statement).first()
        if sql_cur:
            return DomainCurriculum(
                id=sql_cur.id,
                url=sql_cur.url,
                title=sql_cur.title,
                content=sql_cur.content,
                extracted_at=sql_cur.extracted_at,
            )
        return None

    def list(self) -> List[DomainCurriculum]:
        statement = select(SqlCurriculum)
        results = self.session.exec(statement).all()
        return [
            DomainCurriculum(
                id=row.id,
                url=row.url,
                title=row.title,
                content=row.content,
                extracted_at=row.extracted_at,
            )
            for row in results
        ]

    def save(self, curriculum: DomainCurriculum) -> DomainCurriculum:
        statement = select(SqlCurriculum).where(SqlCurriculum.url == curriculum.url)
        sql_cur = self.session.exec(statement).first()
        if sql_cur:
            sql_cur.title = curriculum.title
            sql_cur.content = curriculum.content
            sql_cur.extracted_at = curriculum.extracted_at
        else:
            sql_cur = SqlCurriculum(
                id=curriculum.id,
                title=curriculum.title,
                url=curriculum.url,
                content=curriculum.content,
                extracted_at=curriculum.extracted_at,
            )
            self.session.add(sql_cur)
        self.session.commit()
        self.session.refresh(sql_cur)
        curriculum.id = sql_cur.id
        return curriculum
