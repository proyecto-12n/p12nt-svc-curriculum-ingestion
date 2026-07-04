# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Protocol, Any

from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from infrastructure.adapter.outbound.http.parser.scrap_resource_parser import (
    ScrapResourceParser,
)


class ScrapResourceParserProvider(Protocol):
    def get_parser(
        self, discriminator: CurriculumHierarchyType
    ) -> ScrapResourceParser[Any]:
        """
        Retrieves a ScrapResourceParser implementation matching the CurriculumNodeType discriminator.
        """
        ...
