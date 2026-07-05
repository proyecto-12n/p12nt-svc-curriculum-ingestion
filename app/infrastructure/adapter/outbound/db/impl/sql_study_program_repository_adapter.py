# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Optional, List

from sqlmodel import Session, select

from infrastructure.adapter.outbound.db import CurriculumHierarchyRepository
from infrastructure.models.study_program import StudyProgram


class SqlStudyProgramRepositoryAdapter(CurriculumHierarchyRepository[StudyProgram]):
    def __init__(self, session: Session):
        self.session = session

    async def find_by_url(self, url: str) -> Optional[StudyProgram]:
        statement = select(StudyProgram).where(StudyProgram.url == url)
        return self.session.exec(statement).first()

    async def save(self, study_program: StudyProgram) -> StudyProgram:
        parent_id = getattr(
            study_program, "parent_id", study_program.study_program_ref_id
        )
        statement = select(StudyProgram).where(StudyProgram.url == study_program.url)
        sql_prog = self.session.exec(statement).first()
        if sql_prog:
            sql_prog.parent_id = parent_id
            sql_prog.title = study_program.title
            sql_prog.content = study_program.content
            sql_prog.checksum = study_program.checksum
            sql_prog.extracted_at = study_program.extracted_at
        else:
            sql_prog = StudyProgram(
                id=study_program.id,
                url=study_program.url,
                parent_id=parent_id,
                title=study_program.title,
                content=study_program.content,
                checksum=study_program.checksum,
                extracted_at=study_program.extracted_at,
            )
            self.session.add(sql_prog)
        self.session.commit()
        self.session.refresh(sql_prog)
        study_program.id = sql_prog.id
        return study_program

    async def find_by_id(self, id: int) -> Optional[StudyProgram]:
        statement = select(StudyProgram).where(StudyProgram.id == id)
        return self.session.exec(statement).first()

    async def list(
        self, study_program_ref_id: Optional[int] = None
    ) -> List[StudyProgram]:
        statement = select(StudyProgram)
        if study_program_ref_id is not None:
            statement = statement.where(StudyProgram.parent_id == study_program_ref_id)
        results = self.session.exec(statement).all()
        return [row for row in results]
