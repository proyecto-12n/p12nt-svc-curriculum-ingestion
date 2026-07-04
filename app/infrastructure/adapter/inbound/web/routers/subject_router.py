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
from application.usecase.list_subjects_usecase import ListSubjectsUseCaseImpl
from domain.model import Subject
from domain.port.inbound.get_curriculum_hierarchy_item_use_case import (
    GetCurriculumHierarchyItemUseCase,
)
from domain.port.inbound.list_subjects_use_case import ListSubjectsUseCase
from infrastructure.adapter.inbound.web.dto.subject_response import (
    SubjectResponse,
)
from infrastructure.adapter.outbound.db.sql_subject_repository_adapter import (
    SqlSubjectRepositoryAdapter,
)
from infrastructure.database import get_db

router = APIRouter(prefix="/subjects", tags=["Subjects"])


def get_list_subjects_use_case(
    session: Session = Depends(get_db),
) -> ListSubjectsUseCase:
    repo = SqlSubjectRepositoryAdapter(session)
    return ListSubjectsUseCaseImpl(repo)


def get_get_subject_use_case(
    session: Session = Depends(get_db),
) -> GetCurriculumHierarchyItemUseCase[Subject]:
    repo = SqlSubjectRepositoryAdapter(session)
    return GetCurriculumHierarchyItemUseCaseImpl(repo)


@router.get("", response_model=List[SubjectResponse])
async def list_subjects(
    modality_id: Optional[int] = Query(None, description="Filter by modality ID"),
    use_case: ListSubjectsUseCase = Depends(get_list_subjects_use_case),
):
    results = await use_case.execute(modality_id)
    return [SubjectResponse.from_domain(s) for s in results]


@router.get("/{id}", response_model=SubjectResponse)
async def get_subject(
    id: int,
    use_case: GetCurriculumHierarchyItemUseCase[Subject] = Depends(
        get_get_subject_use_case
    ),
):
    result = await use_case.execute(id)
    if result is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    return SubjectResponse.from_domain(result)
