# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class StudyProgramRef:
    grade_level_id: int
    url: str
    id: Optional[int] = None
