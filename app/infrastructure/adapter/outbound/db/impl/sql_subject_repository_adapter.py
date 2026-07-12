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

    async def find_subject_by_title_and_curriculum_framework(
        self, title: str, curriculum_framework_id: int
    ) -> Optional[Subject]:
        statement = select(Subject).where(
            Subject.title == title, Subject.parent_id == curriculum_framework_id
        )
        return self.session.exec(statement).first()

    async def list(
        self, curriculum_framework_id: Optional[int] = None
    ) -> List[Subject]:
        statement = select(Subject).order_by(Subject.title)
        if curriculum_framework_id is not None:
            statement = statement.where(Subject.parent_id == curriculum_framework_id)
        results = self.session.exec(statement).all()
        return [row for row in results]

    async def save(self, subject: Subject) -> Subject:
        statement = select(Subject).where(
            (Subject.url == subject.url) | (Subject.id == subject.id)
        )
        return CurriculumHierarchyRepositoryHelper.save_hierarchy_model(
            self.session,
            subject,
            statement,
            ("url", "parent_id", "title", "content", "extracted_at"),
        )
