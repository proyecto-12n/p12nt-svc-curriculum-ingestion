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

from application.usecase.get_curriculum_hierarchy_item_usecase import (
    GetCurriculumHierarchyItemUseCaseImpl,
)
from application.usecase.list_grade_levels_usecase import ListGradeLevelsUseCaseImpl
from domain.model import GradeLevel
from domain.port.inbound.get_curriculum_hierarchy_item_use_case import (
    GetCurriculumHierarchyItemUseCase,
)
from domain.port.inbound.list_grade_levels_use_case import ListGradeLevelsUseCase
from infrastructure.adapter.inbound.web.dto.grade_level_response import (
    GradeLevelResponse,
)
from infrastructure.adapter.outbound.db.sql_grade_level_repository_adapter import (
    SqlGradeLevelRepositoryAdapter,
)
from infrastructure.database import get_db

router = APIRouter(prefix="/grade-levels", tags=["Grade Levels"])


def get_list_grade_levels_use_case(
    session: Session = Depends(get_db),
) -> ListGradeLevelsUseCase:
    repo = SqlGradeLevelRepositoryAdapter(session)
    return ListGradeLevelsUseCaseImpl(repo)


def get_get_grade_level_use_case(
    session: Session = Depends(get_db),
) -> GetCurriculumHierarchyItemUseCase[GradeLevel]:
    repo = SqlGradeLevelRepositoryAdapter(session)
    return GetCurriculumHierarchyItemUseCaseImpl(repo)


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
    use_case: GetCurriculumHierarchyItemUseCase[GradeLevel] = Depends(
        get_get_grade_level_use_case
    ),
):
    result = await use_case.execute(id)
    if result is None:
        raise HTTPException(status_code=404, detail="Grade level not found")
    return GradeLevelResponse.from_domain(result)
