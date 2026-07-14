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
from infrastructure.models.curriculum import Curriculum


class SqlCurriculumRepositoryAdapter(CurriculumHierarchyRepository[Curriculum]):
    def __init__(self, session: Session):
        self.session = session

    async def find_by_id(self, id: int) -> Optional[Curriculum]:
        statement = select(Curriculum).where(Curriculum.id == id)
        return await execute_first(self.session, statement)

    async def find_by_url(self, url: str) -> Optional[Curriculum]:
        statement = select(Curriculum).where(Curriculum.url == url)
        return await execute_first(self.session, statement)

    async def list(self, parent_id: Optional[int] = None) -> List[Curriculum]:
        statement = select(Curriculum).order_by(Curriculum.title)
        results = await execute_all(self.session, statement)
        return [row for row in results]

    async def save(self, curriculum: Curriculum) -> Curriculum:
        statement = select(Curriculum).where(Curriculum.url == curriculum.url)
        return await CurriculumHierarchyRepositoryHelper.save_hierarchy_model(
            self.session,
            curriculum,
            statement,
            ("title", "url", "content", "extracted_at"),
        )
