# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Protocol, TypeVar

from domain.model.edge import Edge

M = TypeVar("M")
T = TypeVar("T")


class CurriculumHierarchyMapper(Protocol[M, T]):
    def to_edge(self, model: M) -> Edge[T]: ...

    def to_model(self, edge: Edge[T]) -> M: ...
