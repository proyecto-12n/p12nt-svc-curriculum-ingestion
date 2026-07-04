# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Optional, List

from sqlmodel import Session, select

from domain.model.study_program import StudyProgram as DomainStudyProgram
from domain.port.outbound import KnowledgeRepository
from infrastructure.models.study_program import StudyProgram as SqlStudyProgram


class SqlStudyProgramRepositoryAdapter(KnowledgeRepository[DomainStudyProgram]):
    def __init__(self, session: Session):
        self.session = session

    async def find_by_url(self, url: str) -> Optional[DomainStudyProgram]:
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

    async def save(
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

    async def find_by_id(self, id: int) -> Optional[DomainStudyProgram]:
        statement = select(SqlStudyProgram).where(SqlStudyProgram.id == id)
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

    async def list(
            self, study_program_ref_id: Optional[int] = None
    ) -> List[DomainStudyProgram]:
        statement = select(SqlStudyProgram)
        if study_program_ref_id is not None:
            statement = statement.where(
                SqlStudyProgram.study_program_ref_id == study_program_ref_id
            )
        results = self.session.exec(statement).all()
        return [
            DomainStudyProgram(
                id=row.id,
                url=row.url,
                study_program_ref_id=row.study_program_ref_id,
                title=row.title,
                checksum=row.checksum,
                content=row.content,
                extracted_at=row.extracted_at,
            )
            for row in results
        ]
