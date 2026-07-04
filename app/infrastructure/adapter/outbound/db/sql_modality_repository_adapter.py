# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Optional, List

from sqlmodel import Session, select

from domain.model.modality import Modality as DomainModality
from domain.port.outbound import CurriculumHierarchyRepository
from infrastructure.models.modality import Modality as SqlModality


class SqlModalityRepositoryAdapter(CurriculumHierarchyRepository[DomainModality]):
    def __init__(self, session: Session):
        self.session = session

    async def find_by_id(self, id: int) -> Optional[DomainModality]:
        statement = select(SqlModality).where(SqlModality.id == id)
        sql_mod = self.session.exec(statement).first()
        if sql_mod:
            return DomainModality(
                id=sql_mod.id,
                curriculum_id=sql_mod.curriculum_id,
                title=sql_mod.title,
                url=sql_mod.url,
                content=sql_mod.content,
                extracted_at=sql_mod.extracted_at,
            )
        return None

    async def find_by_url(self, url: str) -> Optional[DomainModality]:
        statement = select(SqlModality).where(SqlModality.url == url)
        sql_mod = self.session.exec(statement).first()
        if sql_mod:
            return DomainModality(
                id=sql_mod.id,
                curriculum_id=sql_mod.curriculum_id,
                title=sql_mod.title,
                url=sql_mod.url,
                content=sql_mod.content,
                extracted_at=sql_mod.extracted_at,
            )
        return None

    async def save(self, modality: DomainModality) -> DomainModality:
        statement = select(SqlModality).where(SqlModality.url == modality.url)
        sql_mod = self.session.exec(statement).first()
        if sql_mod:
            sql_mod.curriculum_id = modality.curriculum_id
            sql_mod.title = modality.title
            sql_mod.content = modality.content
            sql_mod.extracted_at = modality.extracted_at
        else:
            sql_mod = SqlModality(
                curriculum_id=modality.curriculum_id,
                title=modality.title,
                url=modality.url,
                content=modality.content,
                extracted_at=modality.extracted_at,
            )
            self.session.add(sql_mod)
        self.session.commit()
        self.session.refresh(sql_mod)
        modality.id = sql_mod.id
        return modality

    async def list(self, curriculum_id: Optional[int] = None) -> List[DomainModality]:
        statement = select(SqlModality)
        if curriculum_id is not None:
            statement = statement.where(SqlModality.curriculum_id == curriculum_id)
        results = self.session.exec(statement).all()
        return [
            DomainModality(
                id=row.id,
                curriculum_id=row.curriculum_id,
                title=row.title,
                url=row.url,
                content=row.content,
                extracted_at=row.extracted_at,
            )
            for row in results
        ]
