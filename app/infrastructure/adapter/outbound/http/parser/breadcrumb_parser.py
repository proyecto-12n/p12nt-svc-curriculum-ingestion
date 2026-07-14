# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from bs4 import BeautifulSoup

from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from domain.model.edge import Edge
from domain.model.resource_type import ResourceType


class BreadcrumbParser:
    def __init__(self):
        self.hierarchy_by_position = {
            1: CurriculumHierarchyType.CURRICULUM,
            2: CurriculumHierarchyType.MODALITY,
            3: CurriculumHierarchyType.SUBJECT,
            4: CurriculumHierarchyType.GRADE_LEVEL,
        }

    def parse(self, soup: BeautifulSoup) -> dict[CurriculumHierarchyType, Edge[str]]:
        """Returns breadcrumb components mapped to their curriculum hierarchy."""
        components = soup.select(".breadcrumb li")
        assert (
            len(components) > 0 and components[0].get_text(" ", strip=True) == "Inicio"
        ), "First breadcrumb must be Inicio"
        assert (
            len(components) > 1
            and components[1].get_text(" ", strip=True) == "Currículum"
        ), "Second breadcrumb must be Currículum"

        return {
            hierarchy: Edge(
                url=(
                    link.get("href") if (link := component.find("a", href=True)) else ""
                ),
                type=ResourceType.HTML,
                hierarchy=hierarchy,
                title=component.get_text(" ", strip=True),
            )
            for position, component in enumerate(components)
            if (hierarchy := self.hierarchy_by_position.get(position)) is not None
        }
