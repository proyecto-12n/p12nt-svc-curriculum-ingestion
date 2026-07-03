# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Protocol, List
from app.domain.model.curriculum import Curriculum


class ListCurriculumsUseCase(Protocol):
    async def execute(self) -> List[Curriculum]:
        pass
