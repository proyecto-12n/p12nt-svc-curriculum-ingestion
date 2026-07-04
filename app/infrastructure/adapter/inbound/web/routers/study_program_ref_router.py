# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from application.usecase.get_curriculum_hierarchy_item_usecase import (
    GetCurriculumHierarchyItemUseCaseImpl,
)
from application.usecase.list_curriculum_hierarchy_item_usecase import (
    ListCurriculumHierarchyItemUseCaseImpl,
)
from domain.model import StudyProgramRef
from domain.port.inbound.get_curriculum_hierarchy_item_use_case import (
    GetCurriculumHierarchyItemUseCase,
)
from domain.port.inbound.list_curriculum_hierarchy_item_use_case import (
    ListCurriculumHierarchyItemUseCase,
)
from infrastructure.adapter.inbound.web.dto.study_program_ref_response import (
    StudyProgramRefResponse,
)
from infrastructure.adapter.outbound.db.impl.sql_study_program_ref_repository_adapter import (
    SqlStudyProgramRefRepositoryAdapter,
)
from infrastructure.database import get_db

router = APIRouter(prefix="/study-program-refs", tags=["Study Program Refs"])


def get_list_study_program_refs_use_case(
    session: Session = Depends(get_db),
) -> ListCurriculumHierarchyItemUseCase[StudyProgramRef]:
    repo = SqlStudyProgramRefRepositoryAdapter(session)
    return ListCurriculumHierarchyItemUseCaseImpl(repo)


def get_get_study_program_ref_use_case(
    session: Session = Depends(get_db),
) -> GetCurriculumHierarchyItemUseCase[StudyProgramRef]:
    repo = SqlStudyProgramRefRepositoryAdapter(session)
    return GetCurriculumHierarchyItemUseCaseImpl(repo)


@router.get("", response_model=List[StudyProgramRefResponse])
async def list_study_program_refs(
    grade_level_id: Optional[int] = Query(None, description="Filter by grade level ID"),
    use_case: ListCurriculumHierarchyItemUseCase[StudyProgramRef] = Depends(
        get_list_study_program_refs_use_case
    ),
):
    results = await use_case.execute(grade_level_id)
    return [StudyProgramRefResponse.from_domain(r) for r in results]


@router.get("/{id}", response_model=StudyProgramRefResponse)
async def get_study_program_ref(
    id: int,
    use_case: GetCurriculumHierarchyItemUseCase[StudyProgramRef] = Depends(
        get_get_study_program_ref_use_case
    ),
):
    result = await use_case.execute(id)
    if result is None:
        raise HTTPException(status_code=404, detail="Study program ref not found")
    return StudyProgramRefResponse.from_domain(result)
