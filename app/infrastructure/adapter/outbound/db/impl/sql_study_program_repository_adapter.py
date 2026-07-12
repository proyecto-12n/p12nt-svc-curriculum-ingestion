# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Any, List, Optional

from sqlmodel import Session, select

from infrastructure.adapter.outbound.db import CurriculumHierarchyRepository
from infrastructure.models.study_program import StudyProgram
from infrastructure.models.study_program_json import StudyProgramJson
from infrastructure.models.study_program_markdown import StudyProgramMarkdown
from infrastructure.util import generate_id


class SqlStudyProgramRepositoryAdapter(CurriculumHierarchyRepository[StudyProgram]):
    def __init__(self, session: Session):
        self.session = session

    async def find_by_url(self, url: str) -> Optional[StudyProgram]:
        statement = select(StudyProgram).where(StudyProgram.url == url)
        return self.session.exec(statement).first()

    async def save(self, study_program: StudyProgram) -> StudyProgram:
        parent_id = study_program.parent_id
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
        statement = select(StudyProgram).order_by(StudyProgram.title)
        if study_program_ref_id is not None:
            statement = statement.where(StudyProgram.parent_id == study_program_ref_id)
        results = self.session.exec(statement).all()
        return [row for row in results]

    async def find_markdown_by_study_program_id_and_tool_name(
        self, study_program_id: int, tool_name: str
    ) -> Optional[StudyProgramMarkdown]:
        statement = select(StudyProgramMarkdown).where(
            StudyProgramMarkdown.study_program_id == study_program_id,
            StudyProgramMarkdown.tool_name == tool_name,
        )
        return self.session.exec(statement).first()

    async def list_markdowns(
        self,
        tool_name: Optional[str] = None,
        study_program_id: Optional[int] = None,
    ) -> List[StudyProgramMarkdown]:
        statement = select(StudyProgramMarkdown)
        if tool_name is not None:
            statement = statement.where(StudyProgramMarkdown.tool_name == tool_name)
        if study_program_id is not None:
            statement = statement.where(
                StudyProgramMarkdown.study_program_id == study_program_id
            )
        results = self.session.exec(statement).all()
        return [row for row in results]

    async def save_markdown(
        self, study_program: StudyProgram, content: str, tool_name: str
    ) -> StudyProgramMarkdown:
        markdown = await self.find_markdown_by_study_program_id_and_tool_name(
            study_program.id, tool_name
        )
        if markdown:
            markdown.content = content
            markdown.tool_name = tool_name
        else:
            markdown = StudyProgramMarkdown(
                id=generate_id(tool_name, study_program.title),
                study_program_id=study_program.id,
                content=content,
                tool_name=tool_name,
            )
            self.session.add(markdown)
        self.session.commit()
        self.session.refresh(markdown)
        return markdown

    async def find_json_by_study_program_id_and_tool_name(
        self, study_program_id: int, tool_name: str
    ) -> Optional[StudyProgramJson]:
        statement = select(StudyProgramJson).where(
            StudyProgramJson.study_program_id == study_program_id,
            StudyProgramJson.tool_name == tool_name,
        )
        return self.session.exec(statement).first()

    async def save_json(
        self, study_program_id: int, content: dict[str, Any], tool_name: str
    ) -> StudyProgramJson:
        study_program_json = await self.find_json_by_study_program_id_and_tool_name(
            study_program_id, tool_name
        )
        if study_program_json:
            study_program_json.content = content
            study_program_json.tool_name = tool_name
        else:
            study_program_json = StudyProgramJson(
                id=generate_id(tool_name, str(study_program_id)),
                study_program_id=study_program_id,
                content=content,
                tool_name=tool_name,
            )
            self.session.add(study_program_json)
        self.session.commit()
        self.session.refresh(study_program_json)
        return study_program_json
