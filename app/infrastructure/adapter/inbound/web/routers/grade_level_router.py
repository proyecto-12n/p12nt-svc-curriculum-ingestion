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
from domain.model import GradeLevel
from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from domain.port.inbound.get_curriculum_hierarchy_item_use_case import (
    GetCurriculumHierarchyItemUseCase,
)
from domain.port.inbound.get_grade_level_summary_report_use_case import (
    GetGradeLevelSummaryReportUseCase,
)
from domain.port.inbound.list_curriculum_hierarchy_item_use_case import (
    ListCurriculumHierarchyItemUseCase,
)
from domain.port.inbound.list_grade_level_detail_report_use_case import (
    ListGradeLevelDetailReportUseCase,
)
from domain.port.inbound.parse_scrap_resource_use_case import ParseScrapResourceUseCase
from infrastructure.adapter.inbound.web.dto.grade_level_detail_report_response import (
    GradeLevelDetailReportResponse,
)
from infrastructure.adapter.inbound.web.dto.grade_level_response import (
    GradeLevelResponse,
)
from infrastructure.adapter.inbound.web.dto.grade_level_summary_report_response import (
    GradeLevelSummaryReportResponse,
)
from infrastructure.adapter.inbound.web.dto.scrap_resource_parser_result_response import (
    ScrapResourceParserResultResponse,
)
from infrastructure.adapter.inbound.web.routers import subject_router
from infrastructure.adapter.outbound.db.impl.sql_grade_level_repository_adapter import (
    SqlGradeLevelRepositoryAdapter,
)
from infrastructure.adapter.outbound.http.scrap_resource_parser_provider_adapter import (
    ScrapResourceParserProviderAdapter,
)
from infrastructure.database import get_db

router = APIRouter(prefix="/grade-levels", tags=["Grade Levels"])


def get_list_grade_levels_use_case(
    session: Session = Depends(get_db),
) -> ListCurriculumHierarchyItemUseCase[GradeLevel]:
    repo = SqlGradeLevelRepositoryAdapter(session)
    return ListCurriculumHierarchyItemUseCaseImpl(repo)


def get_get_grade_level_use_case(
    session: Session = Depends(get_db),
) -> GetCurriculumHierarchyItemUseCase[GradeLevel]:
    repo = SqlGradeLevelRepositoryAdapter(session)
    return GetCurriculumHierarchyItemUseCaseImpl(repo)


def get_parse_grade_level_use_case(
    session: Session = Depends(get_db),
) -> ParseScrapResourceUseCase:
    repo = SqlGradeLevelRepositoryAdapter(session)
    return ParseScrapResourceUseCaseImpl(
        repo, ScrapResourceParserProviderAdapter(), CurriculumHierarchyType.GRADE_LEVEL
    )


@router.get(
    "",
    response_model=List[GradeLevelResponse],
    response_model_exclude={"__all__": {"content"}},
)
async def list_grade_levels(
    parent_id: int = Query(..., description="Filter by parent ID"),
    use_case: ListCurriculumHierarchyItemUseCase[GradeLevel] = Depends(
        get_list_grade_levels_use_case
    ),
):
    results = await use_case.execute(parent_id)
    return [GradeLevelResponse.from_domain(g) for g in results]


@router.get(
    "/report/detail",
    response_model=list[GradeLevelDetailReportResponse],
)
async def list_grade_level_detail_report(
    use_case: ListGradeLevelDetailReportUseCase = Depends(
        subject_router.get_list_grade_level_detail_report_use_case
    ),
) -> list[GradeLevelDetailReportResponse]:
    results = await use_case.execute()
    return [GradeLevelDetailReportResponse.from_domain(result) for result in results]


@router.get(
    "/report/summary",
    response_model=GradeLevelSummaryReportResponse,
)
async def get_grade_level_summary_report(
    use_case: GetGradeLevelSummaryReportUseCase = Depends(
        subject_router.get_grade_level_summary_report_use_case
    ),
) -> GradeLevelSummaryReportResponse:
    result = await use_case.execute()
    return GradeLevelSummaryReportResponse.from_domain(result)


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


@router.get("/{id}/parser-result", response_model=ScrapResourceParserResultResponse)
async def parse_grade_level_resource(
    id: int,
    use_case: ParseScrapResourceUseCase = Depends(get_parse_grade_level_use_case),
):
    result = await use_case.execute(id)
    if result is None:
        raise HTTPException(status_code=404, detail="Grade level not found")
    return ScrapResourceParserResultResponse.from_domain(result)
