# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import base64
from typing import Any, Optional

from pydantic import BaseModel

from domain.model.edge import Edge
from domain.model.scrap_resource_parser_result import ScrapResourceParserResult


class ScrapResourceParserResultResponse(BaseModel):
    title: Optional[str] = None
    children: list[dict[str, Any]]

    @classmethod
    def from_domain(
        cls, result: ScrapResourceParserResult
    ) -> "ScrapResourceParserResultResponse":
        return cls(
            title=result.title,
            children=[cls._child_to_dict(child) for child in result.children],
        )

    @staticmethod
    def _child_to_dict(child: Edge[Any]) -> dict[str, Any]:
        content = child.content
        if isinstance(content, bytes):
            content = base64.b64encode(content).decode("utf-8")
        return {
            "url": child.url,
            "type": child.type.value,
            "hierarchy": child.hierarchy.value if child.hierarchy else None,
            "parent_url": child.parent_url,
            "title": child.title,
            "content": content,
        }
