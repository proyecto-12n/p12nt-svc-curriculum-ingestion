# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Protocol, List, Optional
from domain.model.modality import Modality


class ListModalitiesUseCase(Protocol):
    async def execute(self, curriculum_id: Optional[int] = None) -> List[Modality]:
        pass
