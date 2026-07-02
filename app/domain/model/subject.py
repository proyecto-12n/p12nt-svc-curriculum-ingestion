# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from dataclasses import dataclass


@dataclass
class Subject:
    id: int
    modality_id: int
    title: str
    url: str
