# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from bs4 import BeautifulSoup

from domain.model.resource_type import ResourceType
from domain.model.scrap_resource import ScrapResource


class BeautifulSoupBuilder:
    @staticmethod
    def build(resource: ScrapResource[str]) -> BeautifulSoup:
        """Builds a BeautifulSoup instance from a ScrapResource with HTML content."""
        if resource.type != ResourceType.HTML:
            raise ValueError(
                f"Cannot build BeautifulSoup from resource type: {resource.type}"
            )
        return BeautifulSoup(resource.content, "html.parser")
