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

from domain.model.subject import Subject as DomainSubject
from domain.port.outbound import KnowledgeRepository

from infrastructure.models.subject import Subject as SqlSubject


class SqlSubjectRepositoryAdapter(KnowledgeRepository[DomainSubject]):
    def __init__(self, session: Session):
        self.session = session

    @deprecated("Use find_by_url instead of find_subject_by_title_and_modality")
    async def find_subject_by_title_and_modality(
            self, title: str, modality_id: int
    ) -> Optional[DomainSubject]:
        statement = select(SqlSubject).where(
            SqlSubject.title == title, SqlSubject.modality_id == modality_id
        )
        sql_sub = self.session.exec(statement).first()
        if sql_sub:
            return DomainSubject(
                id=sql_sub.id,
                title=sql_sub.title,
                modality_id=sql_sub.modality_id,
                url=sql_sub.url,
                content=sql_sub.content,
                extracted_at=sql_sub.extracted_at,
            )
        return None

    async def find_by_id(self, id: int) -> Optional[DomainSubject]:
        statement = select(SqlSubject).where(SqlSubject.id == id)
        sql_sub = self.session.exec(statement).first()
        if sql_sub:
            return DomainSubject(
                id=sql_sub.id,
                title=sql_sub.title,
                modality_id=sql_sub.modality_id,
                url=sql_sub.url,
                content=sql_sub.content,
                extracted_at=sql_sub.extracted_at,
            )
        return None

    async def find_by_url(self, url: str) -> Optional[DomainSubject]:
        statement = select(SqlSubject).where(SqlSubject.url == url)
        sql_sub = self.session.exec(statement).first()
        if sql_sub:
            return DomainSubject(
                id=sql_sub.id,
                title=sql_sub.title,
                modality_id=sql_sub.modality_id,
                url=sql_sub.url,
                content=sql_sub.content,
                extracted_at=sql_sub.extracted_at,
            )
        return None

    async def list(self, modality_id: Optional[int] = None) -> List[DomainSubject]:
        statement = select(SqlSubject)
        if modality_id is not None:
            statement = statement.where(SqlSubject.modality_id == modality_id)
        results = self.session.exec(statement).all()
        return [
            DomainSubject(
                id=row.id,
                title=row.title,
                modality_id=row.modality_id,
                url=row.url,
                content=row.content,
                extracted_at=row.extracted_at,
            )
            for row in results
        ]

    async def save(self, subject: DomainSubject) -> DomainSubject:
        statement = select(SqlSubject).where(
            SqlSubject.title == subject.title,
            SqlSubject.modality_id == subject.modality_id,
        )
        sql_sub = self.session.exec(statement).first()
        if sql_sub:
            sql_sub.url = subject.url
            sql_sub.content = subject.content
            sql_sub.extracted_at = subject.extracted_at
        else:
            sql_sub = SqlSubject(
                title=subject.title,
                modality_id=subject.modality_id,
                url=subject.url,
                content=subject.content,
                extracted_at=subject.extracted_at,
            )
            self.session.add(sql_sub)
        self.session.commit()
        self.session.refresh(sql_sub)
        subject.id = sql_sub.id
        return subject
