# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Optional, List

from sqlalchemy import case, func
from sqlmodel import Session, select

from domain.model.grade_level_detail_report import GradeLevelDetailReport
from infrastructure.adapter.outbound.db import (
    CurriculumHierarchyRepository,
    CurriculumHierarchyRepositoryHelper,
)
from infrastructure.models.grade_level import GradeLevel
from infrastructure.models.grade_level_study_program_ref import (
    GradeLevelStudyProgramRef,
)
from infrastructure.models.study_program import StudyProgram
from infrastructure.models.study_program_markdown import StudyProgramMarkdown
from infrastructure.models.study_program_ref import StudyProgramRef


class SqlGradeLevelRepositoryAdapter(CurriculumHierarchyRepository[GradeLevel]):
    def __init__(self, session: Session):
        self.session = session

    async def save(self, grade_level: GradeLevel) -> GradeLevel:
        statement = select(GradeLevel).where(
            (GradeLevel.url == grade_level.url) | (GradeLevel.id == grade_level.id)
        )
        return CurriculumHierarchyRepositoryHelper.save_hierarchy_model(
            self.session,
            grade_level,
            statement,
            ("url", "parent_id", "title", "content", "extracted_at"),
        )

    async def find_by_url(self, url: str) -> Optional[GradeLevel]:
        statement = select(GradeLevel).where(GradeLevel.url == url)
        return self.session.exec(statement).first()

    async def find_by_id(self, id: int) -> Optional[GradeLevel]:
        statement = select(GradeLevel).where(GradeLevel.id == id)
        return self.session.exec(statement).first()

    async def find_grade_level_by_title_and_subject(
        self, title: str, subject_id: int
    ) -> Optional[GradeLevel]:
        statement = select(GradeLevel).where(
            GradeLevel.title == title, GradeLevel.parent_id == subject_id
        )
        return self.session.exec(statement).first()

    async def list(self, parent_id: Optional[int] = None) -> List[GradeLevel]:
        statement = select(GradeLevel)
        if parent_id is not None:
            statement = statement.where(GradeLevel.parent_id == parent_id)
        results = self.session.exec(statement).all()
        return [row for row in results]

    async def list_detail_report(self) -> List[GradeLevelDetailReport]:
        markdowns = (
            select(
                StudyProgramMarkdown.study_program_id,
                func.max(
                    case(
                        (
                            StudyProgramMarkdown.tool_name == "markitdown",
                            StudyProgramMarkdown.id,
                        )
                    )
                ).label("study_program_markitdown_id"),
                func.max(
                    case(
                        (
                            StudyProgramMarkdown.tool_name == "pymupdf4llm",
                            StudyProgramMarkdown.id,
                        )
                    )
                ).label("study_program_pymupdf4llm_id"),
            )
            .group_by(StudyProgramMarkdown.study_program_id)
            .subquery()
        )
        rows = self.session.exec(
            select(
                GradeLevel.id.label("id"),
                GradeLevel.title.label("title"),
                GradeLevel.url.label("url"),
                StudyProgramRef.id.label("study_program_ref_id"),
                StudyProgram.id.label("study_program_id"),
                markdowns.c.study_program_markitdown_id,
                markdowns.c.study_program_pymupdf4llm_id,
            )
            .outerjoin(
                GradeLevelStudyProgramRef,
                GradeLevelStudyProgramRef.grade_level_id == GradeLevel.id,
            )
            .outerjoin(
                StudyProgramRef,
                StudyProgramRef.id == GradeLevelStudyProgramRef.study_program_ref_id,
            )
            .outerjoin(
                StudyProgram,
                StudyProgram.parent_id == StudyProgramRef.id,
            )
            .outerjoin(markdowns, markdowns.c.study_program_id == StudyProgram.id)
        ).all()

        return [GradeLevelDetailReport(**row._mapping) for row in rows]
