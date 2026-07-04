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

from domain.port.inbound.get_study_program_ref_use_case import (
    GetStudyProgramRefUseCase,
)
from domain.port.inbound.list_study_program_refs_use_case import (
    ListStudyProgramRefsUseCase,
)
from application.usecase.get_study_program_ref_usecase import (
    GetStudyProgramRefUseCaseImpl,
)
from application.usecase.list_study_program_refs_usecase import (
    ListStudyProgramRefsUseCaseImpl,
)
from infrastructure.adapter.outbound.db.sql_study_program_ref_repository_adapter import (
    SqlStudyProgramRefRepositoryAdapter,
)
from infrastructure.database import get_db
from infrastructure.adapter.inbound.web.dto.study_program_ref_response import (
    StudyProgramRefResponse,
)

router = APIRouter(prefix="/study-program-refs", tags=["Study Program Refs"])


def get_list_study_program_refs_use_case(
    session: Session = Depends(get_db),
) -> ListStudyProgramRefsUseCase:
    repo = SqlStudyProgramRefRepositoryAdapter(session)
    return ListStudyProgramRefsUseCaseImpl(repo)


def get_get_study_program_ref_use_case(
    session: Session = Depends(get_db),
) -> GetStudyProgramRefUseCase:
    repo = SqlStudyProgramRefRepositoryAdapter(session)
    return GetStudyProgramRefUseCaseImpl(repo)


@router.get("", response_model=List[StudyProgramRefResponse])
async def list_study_program_refs(
    grade_level_id: Optional[int] = Query(None, description="Filter by grade level ID"),
    use_case: ListStudyProgramRefsUseCase = Depends(
        get_list_study_program_refs_use_case
    ),
):
    results = await use_case.execute(grade_level_id)
    return [StudyProgramRefResponse.from_domain(r) for r in results]


@router.get("/{id}", response_model=StudyProgramRefResponse)
async def get_study_program_ref(
    id: int,
    use_case: GetStudyProgramRefUseCase = Depends(get_get_study_program_ref_use_case),
):
    result = await use_case.execute(id)
    if result is None:
        raise HTTPException(status_code=404, detail="Study program ref not found")
    return StudyProgramRefResponse.from_domain(result)
