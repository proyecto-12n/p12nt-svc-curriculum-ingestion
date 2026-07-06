# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Optional, Protocol

from domain.model.scrap_resource_parser_result import ScrapResourceParserResult


class ParseScrapResourceUseCase(Protocol):
    async def execute(self, id: int) -> Optional[ScrapResourceParserResult]: ...
