# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Protocol, Optional, TypeVar

K = TypeVar("K")


class GetCurriculumHierarchyItemUseCase(Protocol[K]):
    async def execute(self, id: int) -> Optional[K]: ...
