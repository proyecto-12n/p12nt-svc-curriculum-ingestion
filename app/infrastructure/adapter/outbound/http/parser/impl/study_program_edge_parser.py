# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import AsyncGenerator, Any

from domain.model import ResourceType
from domain.model.edge import Edge
from domain.model.scrap_resource import ScrapResource
from infrastructure.adapter.outbound.http.parser.scrap_resource_parser import (
    ScrapResourceParser,
)
from infrastructure.adapter.outbound.http.parser.scrap_resource_title_strategy_provider import (
    ScrapResourceTitleStrategyProvider,
)


class StudyProgramScrapResourceParser(ScrapResourceParser[bytes]):
    async def get_children(
        self, resource: ScrapResource[bytes]
    ) -> AsyncGenerator[Edge[bytes], Any]:
        if False:
            yield

    async def get_title(self, resource: ScrapResource[bytes]) -> str:
        return ScrapResourceTitleStrategyProvider.get_strategy(
            ResourceType.PDF
        ).extract(resource)
