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
                Subject.id.label("subject_id"),
                Subject.title.label("subject_name"),
                Subject.url.label("subject_url"),
                GradeLevel.id.label("grade_level_id"),
                GradeLevel.title.label("grade_level_title"),
                GradeLevel.url.label("grade_level_url"),
                StudyProgramRef.id.label("study_program_ref_id"),
                StudyProgram.id.label("study_program_id"),
                markdowns.c.study_program_markitdown_id,
                markdowns.c.study_program_pymupdf4llm_id,
            )
            .select_from(Subject)
            .outerjoin(
                GradeLevel,
                GradeLevel.parent_id == Subject.id,
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
            .order_by(Subject.title, GradeLevel.title)
        ).all()

        return [GradeLevelDetailReport(**row._mapping) for row in rows]

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
