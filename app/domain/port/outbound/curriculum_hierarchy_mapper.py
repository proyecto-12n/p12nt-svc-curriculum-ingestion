# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Protocol, TypeVar

from domain.model.node import Node

M = TypeVar("M")
T = TypeVar("T")


class CurriculumHierarchyMapper(Protocol[M, T]):
    def to_domain_node(self, model: M) -> Node[T]:
        """Maps a SQLModel instance to a domain Node dataclass."""
        ...
