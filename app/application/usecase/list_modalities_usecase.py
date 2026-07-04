# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import List, Optional

from domain.model.modality import Modality
from domain.port.inbound.list_modalities_use_case import ListModalitiesUseCase
from domain.port.outbound import CurriculumHierarchyRepository


class ListModalitiesUseCaseImpl(ListModalitiesUseCase):
    def __init__(self, modality_repository: CurriculumHierarchyRepository[Modality]):
        self.modality_repository = modality_repository

    async def execute(self, curriculum_id: Optional[int] = None) -> List[Modality]:
        return await self.modality_repository.list(curriculum_id)
