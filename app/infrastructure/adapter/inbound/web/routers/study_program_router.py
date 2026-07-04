# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from domain.port.inbound.get_study_program_use_case import GetStudyProgramUseCase
from domain.port.inbound.list_study_programs_use_case import (
    ListStudyProgramsUseCase,
)
from application.usecase.get_study_program_usecase import (
    GetStudyProgramUseCaseImpl,
)
from application.usecase.list_study_programs_usecase import (
    ListStudyProgramsUseCaseImpl,
)
from infrastructure.adapter.outbound.db.sql_study_program_repository_adapter import (
    SqlStudyProgramRepositoryAdapter,
)
from infrastructure.database import get_db
from infrastructure.adapter.inbound.web.dto.study_program_response import (
    StudyProgramResponse,
)

router = APIRouter(prefix="/study-programs", tags=["Study Programs"])


def get_list_study_programs_use_case(
    session: Session = Depends(get_db),
) -> ListStudyProgramsUseCase:
    repo = SqlStudyProgramRepositoryAdapter(session)
    return ListStudyProgramsUseCaseImpl(repo)


def get_get_study_program_use_case(
    session: Session = Depends(get_db),
) -> GetStudyProgramUseCase:
    repo = SqlStudyProgramRepositoryAdapter(session)
    return GetStudyProgramUseCaseImpl(repo)


@router.get("", response_model=List[StudyProgramResponse])
async def list_study_programs(
    study_program_ref_id: Optional[int] = Query(
        None, description="Filter by study program ref ID"
    ),
    use_case: ListStudyProgramsUseCase = Depends(get_list_study_programs_use_case),
):
    results = await use_case.execute(study_program_ref_id)
    return [StudyProgramResponse.from_domain(p) for p in results]


@router.get("/{id}", response_model=StudyProgramResponse)
async def get_study_program(
    id: int,
    use_case: GetStudyProgramUseCase = Depends(get_get_study_program_use_case),
):
    result = await use_case.execute(id)
    if result is None:
        raise HTTPException(status_code=404, detail="Study program not found")
    return StudyProgramResponse.from_domain(result)
