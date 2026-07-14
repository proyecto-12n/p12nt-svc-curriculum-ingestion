# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Modality:
    id: int
    curriculum_id: int
    url: str

    title: str
    content: str

    extracted_at: datetime = field(default_factory=datetime.now)
