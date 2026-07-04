# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

import asyncio
from typing import Optional

from domain.model.modality import Modality
from domain.port.inbound.get_modality_use_case import GetModalityUseCase
from domain.port.outbound import KnowledgeRepository


class GetModalityUseCaseImpl(GetModalityUseCase):
    def __init__(self, modality_repository: KnowledgeRepository[Modality]):
        self.modality_repository = modality_repository

    async def execute(self, id: int) -> Optional[Modality]:
        return await asyncio.to_thread(self.modality_repository.find_by_id, id)
