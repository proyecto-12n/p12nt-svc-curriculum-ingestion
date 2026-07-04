# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Protocol, Optional, List
from domain.model.modality import Modality


class ModalityRepository(Protocol):
    def find_by_url(self, url: str) -> Optional[Modality]:
        pass

    def save(self, modality: Modality) -> Modality:
        pass

    def find_by_id(self, id: int) -> Optional[Modality]:
        pass

    def list(self, curriculum_id: Optional[int] = None) -> List[Modality]:
        pass
