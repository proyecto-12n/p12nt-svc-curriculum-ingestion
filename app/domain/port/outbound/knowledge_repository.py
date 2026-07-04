# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Protocol, Optional, TypeVar, List
from domain.model.curriculum import Curriculum

K = TypeVar("K")


class KnowledgeRepository(Protocol[K]):
    def find_by_id(self, id: int) -> Optional[K]:
        pass

    def find_by_url(self, url: str) -> Optional[K]:
        pass

    def list(self) -> List[K]:
        pass

    def save(self, knowledge: K) -> K:
        pass
