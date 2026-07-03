# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import asyncio
from typing import Optional
from app.domain.model.modality import Modality
from app.domain.port.inbound.get_modality_use_case import GetModalityUseCase
from app.domain.port.outbound.modality_repository import ModalityRepository


class GetModalityUseCaseImpl(GetModalityUseCase):
    def __init__(self, modality_repository: ModalityRepository):
        self.modality_repository = modality_repository

    async def execute(self, id: int) -> Optional[Modality]:
        return await asyncio.to_thread(self.modality_repository.find_modality_by_id, id)
