# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Optional
from sqlmodel import Session, select
from app.domain.port.outbound.curriculum_repository import CurriculumRepository

# Domain models
from app.domain.model.curriculum import Curriculum as DomainCurriculum
from app.domain.model.modality import Modality as DomainModality
from app.domain.model.subject import Subject as DomainSubject
from app.domain.model.grade_level import GradeLevel as DomainGradeLevel
from app.domain.model.study_program_ref import StudyProgramRef as DomainStudyProgramRef
from app.domain.model.study_program import StudyProgram as DomainStudyProgram

# SQLModel models
from app.infrastructure.models.curriculum import Curriculum as SqlCurriculum
from app.infrastructure.models.modality import Modality as SqlModality
from app.infrastructure.models.subject import Subject as SqlSubject
from app.infrastructure.models.grade_level import GradeLevel as SqlGradeLevel
from app.infrastructure.models.study_program_ref import (
    StudyProgramRef as SqlStudyProgramRef,
)
from app.infrastructure.models.study_program import StudyProgram as SqlStudyProgram


class SqlCurriculumRepositoryAdapter(CurriculumRepository):
    def __init__(self, session: Session):
        self.session = session

    def find_curriculum_by_url(self, url: str) -> Optional[DomainCurriculum]:
        statement = select(SqlCurriculum).where(SqlCurriculum.url == url)
        sql_cur = self.session.exec(statement).first()
        if sql_cur:
            return DomainCurriculum(id=sql_cur.id, title=sql_cur.title, url=sql_cur.url)
        return None

    def save_curriculum(self, curriculum: DomainCurriculum) -> DomainCurriculum:
        sql_cur = SqlCurriculum(
            id=curriculum.id,
            title=curriculum.title,
            url=curriculum.url,
        )
        self.session.add(sql_cur)
        self.session.commit()
        self.session.refresh(sql_cur)
        curriculum.id = sql_cur.id
        return curriculum

    def find_modality_by_url(self, url: str) -> Optional[DomainModality]:
        statement = select(SqlModality).where(SqlModality.url == url)
        sql_mod = self.session.exec(statement).first()
        if sql_mod:
            return DomainModality(
                id=sql_mod.id,
                curriculum_id=sql_mod.curriculum_id,
                title=sql_mod.title,
                url=sql_mod.url,
            )
        return None

    def save_modality(self, modality: DomainModality) -> DomainModality:
        sql_mod = SqlModality(
            curriculum_id=modality.curriculum_id,
            title=modality.title,
            url=modality.url,
        )
        self.session.add(sql_mod)
        self.session.commit()
        self.session.refresh(sql_mod)
        modality.id = sql_mod.id
        return modality

    def find_subject_by_title_and_modality(
        self, title: str, modality_id: int
    ) -> Optional[DomainSubject]:
        statement = select(SqlSubject).where(
            SqlSubject.title == title, SqlSubject.modality_id == modality_id
        )
        sql_sub = self.session.exec(statement).first()
        if sql_sub:
            return DomainSubject(
                id=sql_sub.id,
                title=sql_sub.title,
                modality_id=sql_sub.modality_id,
                url=sql_sub.url,
            )
        return None

    def save_subject(self, subject: DomainSubject) -> DomainSubject:
        sql_sub = SqlSubject(
            title=subject.title, modality_id=subject.modality_id, url=subject.url
        )
        self.session.add(sql_sub)
        self.session.commit()
        self.session.refresh(sql_sub)
        subject.id = sql_sub.id
        return subject

    def find_grade_level_by_title_and_subject(
        self, title: str, subject_id: int
    ) -> Optional[DomainGradeLevel]:
        statement = select(SqlGradeLevel).where(
            SqlGradeLevel.title == title, SqlGradeLevel.subject_id == subject_id
        )
        sql_grade = self.session.exec(statement).first()
        if sql_grade:
            return DomainGradeLevel(
                id=sql_grade.id,
                title=sql_grade.title,
                subject_id=sql_grade.subject_id,
                url=sql_grade.url,
            )
        return None

    def save_grade_level(self, grade_level: DomainGradeLevel) -> DomainGradeLevel:
        sql_grade = SqlGradeLevel(
            title=grade_level.title,
            subject_id=grade_level.subject_id,
            url=grade_level.url,
        )
        self.session.add(sql_grade)
        self.session.commit()
        self.session.refresh(sql_grade)
        grade_level.id = sql_grade.id
        return grade_level

    def find_study_program_ref_by_url(
        self, url: str
    ) -> Optional[DomainStudyProgramRef]:
        statement = select(SqlStudyProgramRef).where(SqlStudyProgramRef.url == url)
        sql_ref = self.session.exec(statement).first()
        if sql_ref:
            return DomainStudyProgramRef(
                id=sql_ref.id,
                grade_level_id=sql_ref.grade_level_id,
                title=sql_ref.title,
                url=sql_ref.url,
            )
        return None

    def save_study_program_ref(
        self, study_program_ref: DomainStudyProgramRef
    ) -> DomainStudyProgramRef:
        sql_ref = SqlStudyProgramRef(
            grade_level_id=study_program_ref.grade_level_id,
            title=study_program_ref.title,
            url=study_program_ref.url,
        )
        self.session.add(sql_ref)
        self.session.commit()
        self.session.refresh(sql_ref)
        study_program_ref.id = sql_ref.id
        return study_program_ref

    def find_study_program_by_url(self, url: str) -> Optional[DomainStudyProgram]:
        statement = select(SqlStudyProgram).where(SqlStudyProgram.url == url)
        sql_prog = self.session.exec(statement).first()
        if sql_prog:
            return DomainStudyProgram(
                id=sql_prog.id,
                url=sql_prog.url,
                study_program_ref_id=sql_prog.study_program_ref_id,
                title=sql_prog.title,
                checksum=sql_prog.checksum,
                content=sql_prog.content,
                extracted_at=sql_prog.extracted_at,
            )
        return None

    def save_study_program(
        self, study_program: DomainStudyProgram
    ) -> DomainStudyProgram:
        sql_prog = SqlStudyProgram(
            url=study_program.url,
            study_program_ref_id=study_program.study_program_ref_id,
            title=study_program.title,
            checksum=study_program.checksum,
            content=study_program.content,
            extracted_at=study_program.extracted_at,
        )
        self.session.add(sql_prog)
        self.session.commit()
        self.session.refresh(sql_prog)
        study_program.id = sql_prog.id
        return study_program
