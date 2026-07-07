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
from infrastructure.models.grade_level_study_program_ref import (
    GradeLevelStudyProgramRef,
)
from infrastructure.models.study_program_ref import StudyProgramRef


class SqlStudyProgramRefRepositoryAdapter(
    CurriculumHierarchyRepository[StudyProgramRef]
):
    def __init__(self, session: Session):
        self.session = session

    async def find_by_url(self, url: str) -> Optional[StudyProgramRef]:
        statement = select(StudyProgramRef).where(StudyProgramRef.url == url)
        return self.session.exec(statement).first()

    async def save(self, study_program_ref: StudyProgramRef) -> StudyProgramRef:
        grade_level_id = self._get_grade_level_id(study_program_ref)
        statement = select(StudyProgramRef).where(
            StudyProgramRef.url == study_program_ref.url
        )
        study_program_ref = save_hierarchy_model(
            self.session,
            study_program_ref,
            statement,
            ("url", "title", "content", "extracted_at"),
            self._merge_grade_level_ref(grade_level_id),
        )
        if grade_level_id is not None:
            object.__setattr__(study_program_ref, "_grade_level_id", grade_level_id)
        return study_program_ref

    async def find_by_id(self, id: int) -> Optional[StudyProgramRef]:
        statement = select(StudyProgramRef).where(StudyProgramRef.id == id)
        return self.session.exec(statement).first()

    async def list(self, grade_level_id: Optional[int] = None) -> List[StudyProgramRef]:
        statement = select(StudyProgramRef)
        if grade_level_id is not None:
            statement = statement.join(GradeLevelStudyProgramRef).where(
                GradeLevelStudyProgramRef.grade_level_id == grade_level_id
            )
        results = self.session.exec(statement).all()
        if grade_level_id is not None:
            for row in results:
                object.__setattr__(row, "_grade_level_id", grade_level_id)
        return [row for row in results]

    @staticmethod
    def _get_grade_level_id(study_program_ref: StudyProgramRef) -> Optional[int]:
        if not study_program_ref.grade_levels:
            return None
        return study_program_ref.grade_levels[0].id

    def _merge_grade_level_ref(self, grade_level_id: Optional[int]):
        if grade_level_id is None:
            return None

        def merge(study_program_ref: StudyProgramRef) -> None:
            self.session.merge(
                GradeLevelStudyProgramRef(
                    grade_level_id=grade_level_id,
                    study_program_ref_id=study_program_ref.id,
                )
            )

        return merge
