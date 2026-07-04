# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Protocol, List, TypeVar, Optional

K = TypeVar("K")


class ListCurriculumHierarchyItemUseCase(Protocol[K]):
    async def execute(self, parent_id: Optional[int] = None) -> List[K]: ...
