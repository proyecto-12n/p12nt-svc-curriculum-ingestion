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

from app.domain.port.inbound.get_grade_level_use_case import GetGradeLevelUseCase
from app.domain.port.inbound.list_grade_levels_use_case import ListGradeLevelsUseCase
from app.application.usecase.get_grade_level_usecase import GetGradeLevelUseCaseImpl
from app.application.usecase.list_grade_levels_usecase import ListGradeLevelsUseCaseImpl
from app.infrastructure.adapter.outbound.db.sql_grade_level_repository_adapter import (
    SqlGradeLevelRepositoryAdapter,
)
from app.infrastructure.database import get_db
from app.infrastructure.adapter.inbound.web.dto.grade_level_response import (
    GradeLevelResponse,
)

router = APIRouter(prefix="/grade-levels", tags=["Grade Levels"])


def get_list_grade_levels_use_case(
    session: Session = Depends(get_db),
) -> ListGradeLevelsUseCase:
    repo = SqlGradeLevelRepositoryAdapter(session)
    return ListGradeLevelsUseCaseImpl(repo)


def get_get_grade_level_use_case(
    session: Session = Depends(get_db),
) -> GetGradeLevelUseCase:
    repo = SqlGradeLevelRepositoryAdapter(session)
    return GetGradeLevelUseCaseImpl(repo)


@router.get("", response_model=List[GradeLevelResponse])
async def list_grade_levels(
    subject_id: Optional[int] = Query(None, description="Filter by subject ID"),
    use_case: ListGradeLevelsUseCase = Depends(get_list_grade_levels_use_case),
):
    results = await use_case.execute(subject_id)
    return [GradeLevelResponse.from_domain(g) for g in results]


@router.get("/{id}", response_model=GradeLevelResponse)
async def get_grade_level(
    id: int,
    use_case: GetGradeLevelUseCase = Depends(get_get_grade_level_use_case),
):
    result = await use_case.execute(id)
    if result is None:
        raise HTTPException(status_code=404, detail="Grade level not found")
    return GradeLevelResponse.from_domain(result)
