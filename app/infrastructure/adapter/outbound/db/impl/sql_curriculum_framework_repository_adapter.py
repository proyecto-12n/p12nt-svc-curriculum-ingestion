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
    CurriculumHierarchyRepositoryHelper,
)
from infrastructure.models.curriculum_framework import CurriculumFramework


class SqlCurriculumFrameworkRepositoryAdapter(
    CurriculumHierarchyRepository[CurriculumFramework]
):
    def __init__(self, session: Session):
        self.session = session

    async def find_by_id(self, id: int) -> Optional[CurriculumFramework]:
        statement = select(CurriculumFramework).where(CurriculumFramework.id == id)
        return self.session.exec(statement).first()

    async def find_by_url(self, url: str) -> Optional[CurriculumFramework]:
        statement = select(CurriculumFramework).where(CurriculumFramework.url == url)
        return self.session.exec(statement).first()

    async def save(
        self, curriculum_framework: CurriculumFramework
    ) -> CurriculumFramework:
        statement = select(CurriculumFramework).where(
            CurriculumFramework.url == curriculum_framework.url
        )
        return CurriculumHierarchyRepositoryHelper.save_hierarchy_model(
            self.session,
            curriculum_framework,
            statement,
            ("url", "parent_id", "title", "content", "extracted_at"),
        )

    async def list(self, parent_id: Optional[int] = None) -> List[CurriculumFramework]:
        statement = select(CurriculumFramework)
        if parent_id is not None:
            statement = statement.where(CurriculumFramework.parent_id == parent_id)
        results = self.session.exec(statement).all()
        return [row for row in results]
