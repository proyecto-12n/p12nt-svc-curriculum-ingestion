# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from domain.model.resource_type import ResourceType
from infrastructure.adapter.outbound.http.parser.html_scrap_resource_title_strategy import (
    HtmlScrapResourceTitleStrategy,
)
from infrastructure.adapter.outbound.http.parser.pdf_scrap_resource_title_strategy import (
    PdfScrapResourceTitleStrategy,
)


class ScrapResourceTitleStrategyProvider:
    STRATEGIES = {
        ResourceType.HTML: HtmlScrapResourceTitleStrategy,
        ResourceType.PDF: PdfScrapResourceTitleStrategy,
    }

    @classmethod
    def get_strategy(cls, resource_type: ResourceType) -> type:
        if resource_type not in cls.STRATEGIES:
            raise ValueError(
                f"No title strategy found for resource type: {resource_type}"
            )

        return cls.STRATEGIES[resource_type]
