# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Optional
from sqlmodel import Session, select
from app.domain.port.outbound.study_program_ref_repository import (
    StudyProgramRefRepository,
)

# Domain models
from app.domain.model.study_program_ref import StudyProgramRef as DomainStudyProgramRef

# SQLModel models
from app.infrastructure.models.study_program_ref import (
    StudyProgramRef as SqlStudyProgramRef,
)


class SqlStudyProgramRefRepositoryAdapter(StudyProgramRefRepository):
    def __init__(self, session: Session):
        self.session = session

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
                content=sql_ref.content,
                extracted_at=sql_ref.extracted_at,
            )
        return None

    def save_study_program_ref(
        self, study_program_ref: DomainStudyProgramRef
    ) -> DomainStudyProgramRef:
        statement = select(SqlStudyProgramRef).where(
            SqlStudyProgramRef.url == study_program_ref.url
        )
        sql_ref = self.session.exec(statement).first()
        if sql_ref:
            sql_ref.grade_level_id = study_program_ref.grade_level_id
            sql_ref.title = study_program_ref.title
            sql_ref.content = study_program_ref.content
            sql_ref.extracted_at = study_program_ref.extracted_at
        else:
            sql_ref = SqlStudyProgramRef(
                grade_level_id=study_program_ref.grade_level_id,
                title=study_program_ref.title,
                url=study_program_ref.url,
                content=study_program_ref.content,
                extracted_at=study_program_ref.extracted_at,
            )
            self.session.add(sql_ref)
        self.session.commit()
        self.session.refresh(sql_ref)
        study_program_ref.id = sql_ref.id
        return study_program_ref
