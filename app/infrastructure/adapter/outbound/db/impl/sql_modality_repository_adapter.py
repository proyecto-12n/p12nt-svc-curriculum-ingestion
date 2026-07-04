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
from infrastructure.models.modality import Modality


class SqlModalityRepositoryAdapter(CurriculumHierarchyRepository[Modality]):
    def __init__(self, session: Session):
        self.session = session

    async def find_by_id(self, id: int) -> Optional[Modality]:
        statement = select(Modality).where(Modality.id == id)
        return self.session.exec(statement).first()

    async def find_by_url(self, url: str) -> Optional[Modality]:
        statement = select(Modality).where(Modality.url == url)
        return self.session.exec(statement).first()

    async def save(self, modality: Modality) -> Modality:
        statement = select(Modality).where(Modality.url == modality.url)
        sql_mod = self.session.exec(statement).first()
        if sql_mod:
            sql_mod.curriculum_id = modality.parent_id
            sql_mod.title = modality.title
            sql_mod.content = modality.content
            sql_mod.extracted_at = modality.extracted_at
        else:
            sql_mod = Modality(
                curriculum_id=modality.parent_id,
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

    async def list(self, parent_id: Optional[int] = None) -> List[Modality]:
        statement = select(Modality)
        if parent_id is not None:
            statement = statement.where(Modality.parent_id == parent_id)
        results = self.session.exec(statement).all()
        return [row for row in results]
