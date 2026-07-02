# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Curriculum:
    id: int
    url: str

    title: str
    content: str

    extracted_at: datetime = field(default_factory=datetime.now)
