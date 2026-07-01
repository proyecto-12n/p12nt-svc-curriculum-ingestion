# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from dataclasses import dataclass
from typing import Generic, TypeVar
from app.domain.model.resource_type import ResourceType

T = TypeVar("T")


@dataclass
class Node(Generic[T]):
    url: str
    resource_type: ResourceType
    content: T
