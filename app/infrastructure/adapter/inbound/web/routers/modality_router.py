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
from application.usecase.list_modalities_usecase import ListModalitiesUseCaseImpl
from domain.model import Modality
from domain.port.inbound.get_curriculum_hierarchy_item_use_case import (
    GetCurriculumHierarchyItemUseCase,
)
from domain.port.inbound.list_modalities_use_case import ListModalitiesUseCase
from infrastructure.adapter.inbound.web.dto.modality_response import (
    ModalityResponse,
)
from infrastructure.adapter.outbound.db.sql_modality_repository_adapter import (
    SqlModalityRepositoryAdapter,
)
from infrastructure.database import get_db

router = APIRouter(prefix="/modalities", tags=["Modalities"])


def get_list_modalities_use_case(
    session: Session = Depends(get_db),
) -> ListModalitiesUseCase:
    repo = SqlModalityRepositoryAdapter(session)
    return ListModalitiesUseCaseImpl(repo)


def get_get_modality_use_case(
    session: Session = Depends(get_db),
) -> GetCurriculumHierarchyItemUseCase[Modality]:
    repo = SqlModalityRepositoryAdapter(session)
    return GetCurriculumHierarchyItemUseCaseImpl(repo)


@router.get("", response_model=List[ModalityResponse])
async def list_modalities(
    curriculum_id: Optional[int] = Query(None, description="Filter by curriculum ID"),
    use_case: ListModalitiesUseCase = Depends(get_list_modalities_use_case),
):
    results = await use_case.execute(curriculum_id)
    return [ModalityResponse.from_domain(m) for m in results]


@router.get("/{id}", response_model=ModalityResponse)
async def get_modality(
    id: int,
    use_case: GetCurriculumHierarchyItemUseCase[Modality] = Depends(
        get_get_modality_use_case
    ),
):
    result = await use_case.execute(id)
    if result is None:
        raise HTTPException(status_code=404, detail="Modality not found")
    return ModalityResponse.from_domain(result)
