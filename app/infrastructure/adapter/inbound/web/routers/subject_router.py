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
from domain.model import Subject
from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from domain.port.inbound.get_curriculum_hierarchy_item_use_case import (
    GetCurriculumHierarchyItemUseCase,
)
from domain.port.inbound.list_curriculum_hierarchy_item_use_case import (
    ListCurriculumHierarchyItemUseCase,
)
from domain.port.inbound.parse_scrap_resource_use_case import ParseScrapResourceUseCase
from infrastructure.adapter.inbound.web.dto.subject_response import (
    SubjectResponse,
)
from infrastructure.adapter.inbound.web.dto.scrap_resource_parser_result_response import (
    ScrapResourceParserResultResponse,
)
from infrastructure.adapter.outbound.db.impl.sql_subject_repository_adapter import (
    SqlSubjectRepositoryAdapter,
)
from infrastructure.adapter.outbound.http.scrap_resource_parser_provider_adapter import (
    ScrapResourceParserProviderAdapter,
)
from infrastructure.database import get_db

router = APIRouter(prefix="/subjects", tags=["Subjects"])


def get_list_subjects_use_case(
    session: Session = Depends(get_db),
) -> ListCurriculumHierarchyItemUseCase[Subject]:
    repo = SqlSubjectRepositoryAdapter(session)
    return ListCurriculumHierarchyItemUseCaseImpl(repo)


def get_get_subject_use_case(
    session: Session = Depends(get_db),
) -> GetCurriculumHierarchyItemUseCase[Subject]:
    repo = SqlSubjectRepositoryAdapter(session)
    return GetCurriculumHierarchyItemUseCaseImpl(repo)


def get_parse_subject_use_case(
    session: Session = Depends(get_db),
) -> ParseScrapResourceUseCase:
    repo = SqlSubjectRepositoryAdapter(session)
    return ParseScrapResourceUseCaseImpl(
        repo, ScrapResourceParserProviderAdapter(), CurriculumHierarchyType.SUBJECT
    )


@router.get(
    "",
    response_model=List[SubjectResponse],
    response_model_exclude={"__all__": {"content"}},
)
async def list_subjects(
    parent_id: int = Query(..., description="Filter by parent ID"),
    use_case: ListCurriculumHierarchyItemUseCase[Subject] = Depends(
        get_list_subjects_use_case
    ),
):
    results = await use_case.execute(parent_id)
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


@router.get("/{id}/parser-result", response_model=ScrapResourceParserResultResponse)
async def parse_subject_resource(
    id: int,
    use_case: ParseScrapResourceUseCase = Depends(get_parse_subject_use_case),
):
    result = await use_case.execute(id)
    if result is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    return ScrapResourceParserResultResponse.from_domain(result)
