# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Optional, List

from sqlmodel import Session, select

from domain.port.outbound.curriculum_hierarchy_repository import (
    CurriculumHierarchyRepository,
)
from infrastructure.adapter.outbound.db.curriculum_hierarchy_repository_helper import (
    CurriculumHierarchyRepositoryHelper,
    execute_all,
    execute_first,
)
from infrastructure.models.modality import Modality


class SqlModalityRepositoryAdapter(CurriculumHierarchyRepository[Modality]):
    def __init__(self, session: Session):
        self.session = session

    async def find_by_id(self, id: int) -> Optional[Modality]:
        statement = select(Modality).where(Modality.id == id)
        return await execute_first(self.session, statement)

    async def find_by_url(self, url: str) -> Optional[Modality]:
        statement = select(Modality).where(Modality.url == url)
        return await execute_first(self.session, statement)

    async def save(self, modality: Modality) -> Modality:
        statement = select(Modality).where(Modality.url == modality.url)
        return await CurriculumHierarchyRepositoryHelper.save_hierarchy_model(
            self.session,
            modality,
            statement,
            ("url", "parent_id", "title", "content", "extracted_at"),
        )

    async def list(self, parent_id: Optional[int] = None) -> List[Modality]:
        statement = select(Modality)
        if parent_id is not None:
            statement = statement.where(Modality.parent_id == parent_id).order_by(
                Modality.title
            )
        results = await execute_all(self.session, statement)
        return [row for row in results]
