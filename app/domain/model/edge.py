# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from dataclasses import dataclass
from typing import Generic, TypeVar, Optional
from domain.model.resource_type import ResourceType
from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType

T = TypeVar("T")


@dataclass(frozen=True)
class Edge(Generic[T]):
    url: str
    type: ResourceType
    hierarchy: Optional[CurriculumHierarchyType] = None

    parent_url: Optional[str] = None
    parent_id: Optional[int] = None
    title: Optional[str] = None
    content: Optional[T] = None
