# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from dataclasses import dataclass, field
from typing import Any, Optional

from domain.model.edge import Edge


@dataclass(frozen=True)
class ScrapResourceParserResult:
    title: Optional[str] = None
    children: list[Edge[Any]] = field(default_factory=list)
