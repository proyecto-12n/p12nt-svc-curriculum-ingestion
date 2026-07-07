# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Protocol, Optional, TypeVar, List

K = TypeVar("K")


class CurriculumHierarchyRepository(Protocol[K]):
    async def find_by_id(self, id: int) -> Optional[K]:
        pass

    async def find_by_url(self, url: str) -> Optional[K]:
        pass

    async def list(self, parent_id: Optional[int] = None) -> List[K]:
        pass

    async def save(self, knowledge: K) -> K:
        pass
