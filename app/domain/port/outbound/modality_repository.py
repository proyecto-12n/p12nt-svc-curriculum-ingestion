# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Protocol, Optional
from app.domain.model.modality import Modality


class ModalityRepository(Protocol):
    def find_modality_by_url(self, url: str) -> Optional[Modality]:
        pass

    def save_modality(self, modality: Modality) -> Modality:
        pass
