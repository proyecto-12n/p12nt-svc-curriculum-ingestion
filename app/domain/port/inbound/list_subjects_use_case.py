# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Protocol, List, Optional
from app.domain.model.subject import Subject


class ListSubjectsUseCase(Protocol):
    async def execute(self, modality_id: Optional[int] = None) -> List[Subject]:
        pass
