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
    save_hierarchy_model,
)
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
        return save_hierarchy_model(
            self.session,
            modality,
            statement,
            ("url", "parent_id", "title", "content", "extracted_at"),
        )

    async def list(self, parent_id: Optional[int] = None) -> List[Modality]:
        statement = select(Modality)
        if parent_id is not None:
            statement = statement.where(Modality.parent_id == parent_id)
        results = self.session.exec(statement).all()
        return [row for row in results]
