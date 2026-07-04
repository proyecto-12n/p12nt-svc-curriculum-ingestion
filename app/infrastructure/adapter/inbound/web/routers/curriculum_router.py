# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from application.usecase.get_curriculum_hierarchy_item_usecase import (
    GetCurriculumHierarchyItemUseCaseImpl,
)
from application.usecase.list_curriculums_usecase import ListCurriculumsUseCaseImpl
from domain.model import Curriculum
from domain.port.inbound.get_curriculum_hierarchy_item_use_case import (
    GetCurriculumHierarchyItemUseCase,
)
from domain.port.inbound.list_curriculums_use_case import ListCurriculumsUseCase
from infrastructure.adapter.inbound.web.dto.curriculum_response import (
    CurriculumResponse,
)
from infrastructure.adapter.outbound.db.sql_curriculum_repository_adapter import (
    SqlCurriculumRepositoryAdapter,
)
from infrastructure.database import get_db

router = APIRouter(prefix="/curriculums", tags=["Curriculums"])


def get_list_curriculums_use_case(
    session: Session = Depends(get_db),
) -> ListCurriculumsUseCase:
    repo = SqlCurriculumRepositoryAdapter(session)
    return ListCurriculumsUseCaseImpl(repo)


def get_get_curriculum_use_case(
    session: Session = Depends(get_db),
) -> GetCurriculumHierarchyItemUseCase[Curriculum]:
    repo = SqlCurriculumRepositoryAdapter(session)
    return GetCurriculumHierarchyItemUseCaseImpl(repo)


@router.get("", response_model=List[CurriculumResponse])
async def list_curriculums(
    use_case: ListCurriculumsUseCase = Depends(get_list_curriculums_use_case),
):
    results = await use_case.execute()
    return [CurriculumResponse.from_domain(c) for c in results]


@router.get("/{id}", response_model=CurriculumResponse)
async def get_curriculum(
    id: int,
    use_case: GetCurriculumHierarchyItemUseCase[Curriculum] = Depends(
        get_get_curriculum_use_case
    ),
):
    result = await use_case.execute(id)
    if result is None:
        raise HTTPException(status_code=404, detail="Curriculum not found")
    return CurriculumResponse.from_domain(result)
