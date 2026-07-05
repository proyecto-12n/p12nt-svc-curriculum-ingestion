# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from dataclasses import dataclass
from typing import Generic, TypeVar
from domain.model.resource_type import ResourceType

T = TypeVar("T")


@dataclass(frozen=True)
class ScrapResource(Generic[T]):
    url: str
    type: ResourceType
    content: T
