# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from application.usecase.get_curriculum_hierarchy_item_usecase import (
    GetCurriculumHierarchyItemUseCaseImpl,
)
from application.usecase.list_curriculum_hierarchy_item_usecase import (
    ListCurriculumHierarchyItemUseCaseImpl,
)
from application.usecase.parse_scrap_resource_usecase import (
    ParseScrapResourceUseCaseImpl,
)
from domain.model import Modality
from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from domain.port.inbound.get_curriculum_hierarchy_item_use_case import (
    GetCurriculumHierarchyItemUseCase,
)
from domain.port.inbound.list_curriculum_hierarchy_item_use_case import (
    ListCurriculumHierarchyItemUseCase,
)
from domain.port.inbound.parse_scrap_resource_use_case import ParseScrapResourceUseCase
from infrastructure.adapter.inbound.web.dto.modality_response import (
    ModalityResponse,
)
from infrastructure.adapter.inbound.web.dto.scrap_resource_parser_result_response import (
    ScrapResourceParserResultResponse,
)
from infrastructure.adapter.outbound.db.impl.sql_modality_repository_adapter import (
    SqlModalityRepositoryAdapter,
)
from infrastructure.adapter.outbound.http.scrap_resource_parser_provider_adapter import (
    ScrapResourceParserProviderAdapter,
)
from infrastructure.database import get_db

router = APIRouter(prefix="/modalities", tags=["Modalities"])


def get_list_modalities_use_case(
    session: Session = Depends(get_db),
) -> ListCurriculumHierarchyItemUseCase[Modality]:
    repo = SqlModalityRepositoryAdapter(session)
    return ListCurriculumHierarchyItemUseCaseImpl(repo)


def get_get_modality_use_case(
    session: Session = Depends(get_db),
) -> GetCurriculumHierarchyItemUseCase[Modality]:
    repo = SqlModalityRepositoryAdapter(session)
    return GetCurriculumHierarchyItemUseCaseImpl(repo)


def get_parse_modality_use_case(
    session: Session = Depends(get_db),
) -> ParseScrapResourceUseCase:
    repo = SqlModalityRepositoryAdapter(session)
    return ParseScrapResourceUseCaseImpl(
        repo,
        ScrapResourceParserProviderAdapter(),
        CurriculumHierarchyType.MODALITY,
    )


@router.get(
    "",
    response_model=List[ModalityResponse],
    response_model_exclude={"__all__": {"content"}},
)
async def list_modalities(
    parent_id: int = Query(..., description="Filter by parent ID"),
    use_case: ListCurriculumHierarchyItemUseCase[Modality] = Depends(
        get_list_modalities_use_case
    ),
):
    results = await use_case.execute(parent_id)
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
        raise HTTPException(status_code=404, detail="Curriculum framework not found")
    return ModalityResponse.from_domain(result)


@router.get("/{id}/parser-result", response_model=ScrapResourceParserResultResponse)
async def parse_modality_resource(
    id: int,
    use_case: ParseScrapResourceUseCase = Depends(get_parse_modality_use_case),
):
    result = await use_case.execute(id)
    if result is None:
        raise HTTPException(status_code=404, detail="Curriculum framework not found")
    return ScrapResourceParserResultResponse.from_domain(result)
