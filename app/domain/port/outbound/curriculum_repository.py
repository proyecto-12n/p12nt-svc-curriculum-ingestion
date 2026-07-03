# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Protocol, Optional
from app.domain.model.curriculum import Curriculum


class CurriculumRepository(Protocol):
    def find_curriculum_by_url(self, url: str) -> Optional[Curriculum]:
        pass

    def save_curriculum(self, curriculum: Curriculum) -> Curriculum:
        pass

    def find_curriculum_by_id(self, id: int) -> Optional[Curriculum]:
        pass

    def list_curriculums(self) -> list[Curriculum]:
        pass
