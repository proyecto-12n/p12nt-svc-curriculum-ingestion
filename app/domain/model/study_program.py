# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class StudyProgram:
    url: str
    study_program_ref_id: int
    content: bytes
    checksum: str = ""
    status: str = "PENDING"
    error_log: Optional[str] = None
    extracted_at: datetime = field(default_factory=datetime.utcnow)
    version: str = "1.0"
    id: Optional[int] = None

    @property
    def md5sum(self) -> str:
        return self.checksum
