# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Optional
from sqlmodel import Session, select
from app.domain.port.outbound.study_program_repository import StudyProgramRepository

# Domain models
from app.domain.model.study_program import StudyProgram as DomainStudyProgram

# SQLModel models
from app.infrastructure.models.study_program import StudyProgram as SqlStudyProgram


class SqlStudyProgramRepositoryAdapter(StudyProgramRepository):
    def __init__(self, session: Session):
        self.session = session

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
        statement = select(SqlStudyProgram).where(
            SqlStudyProgram.url == study_program.url
        )
        sql_prog = self.session.exec(statement).first()
        if sql_prog:
            sql_prog.study_program_ref_id = study_program.study_program_ref_id
            sql_prog.title = study_program.title
            sql_prog.checksum = study_program.checksum
            sql_prog.content = study_program.content
            sql_prog.extracted_at = study_program.extracted_at
        else:
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
