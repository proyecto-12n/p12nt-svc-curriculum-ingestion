# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from dataclasses import replace
from typing import Any, Optional

from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from domain.model.resource_type import ResourceType
from domain.model.scrap_resource import ScrapResource
from domain.model.scrap_resource_parser_result import ScrapResourceParserResult
from domain.port.inbound.parse_scrap_resource_use_case import ParseScrapResourceUseCase
from domain.port.outbound.scrap_resource_parser_provider import (
    ScrapResourceParserProvider,
)
from infrastructure.adapter.outbound.db.curriculum_hierarchy_repository import (
    CurriculumHierarchyRepository,
)


class ParseScrapResourceUseCaseImpl(ParseScrapResourceUseCase):
    def __init__(
        self,
        repository: CurriculumHierarchyRepository[Any],
        parser_provider: ScrapResourceParserProvider,
        hierarchy_type: CurriculumHierarchyType,
    ):
        self.repository = repository
        self.parser_provider = parser_provider
        self.hierarchy_type = hierarchy_type

    async def execute(self, id: int) -> Optional[ScrapResourceParserResult]:
        item = await self.repository.find_by_id(id)
        if item is None:
            return None

        parser = self.parser_provider.get_parser(self.hierarchy_type)
        resource = ScrapResource(
            url=item.url,
            type=ResourceType.PDF
            if self.hierarchy_type == CurriculumHierarchyType.STUDY_PROGRAM
            else ResourceType.HTML,
            content=item.content,
        )

        return ScrapResourceParserResult(
            title=await parser.get_title(resource),
            children=[
                replace(child, parent_id=id)
                async for child in parser.get_children(resource)
            ],
        )
