# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import asyncio
from typing import List, Optional
from app.domain.model.modality import Modality
from app.domain.port.inbound.list_modalities_use_case import ListModalitiesUseCase
from app.domain.port.outbound.modality_repository import ModalityRepository


class ListModalitiesUseCaseImpl(ListModalitiesUseCase):
    def __init__(self, modality_repository: ModalityRepository):
        self.modality_repository = modality_repository

    async def execute(self, curriculum_id: Optional[int] = None) -> List[Modality]:
        return await asyncio.to_thread(
            self.modality_repository.list_modalities, curriculum_id
        )
