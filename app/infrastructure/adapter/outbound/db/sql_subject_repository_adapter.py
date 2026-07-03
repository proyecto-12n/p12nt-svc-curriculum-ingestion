# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Optional
from sqlmodel import Session, select
from app.domain.port.outbound.subject_repository import SubjectRepository

# Domain models
from app.domain.model.subject import Subject as DomainSubject

# SQLModel models
from app.infrastructure.models.subject import Subject as SqlSubject


class SqlSubjectRepositoryAdapter(SubjectRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_subject_by_title_and_modality(
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

    def save_subject(self, subject: DomainSubject) -> DomainSubject:
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
