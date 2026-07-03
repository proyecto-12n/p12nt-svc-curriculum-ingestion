# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Protocol, Optional
from app.domain.model.subject import Subject


class SubjectRepository(Protocol):
    def find_subject_by_title_and_modality(
        self, title: str, modality_id: int
    ) -> Optional[Subject]:
        pass

    def save_subject(self, subject: Subject) -> Subject:
        pass
