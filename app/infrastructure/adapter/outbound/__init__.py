# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from infrastructure.adapter.outbound.db import (
    SqlCurriculumRepositoryAdapter,
    SqlModalityRepositoryAdapter,
    SqlSubjectRepositoryAdapter,
    SqlGradeLevelRepositoryAdapter,
    SqlStudyProgramRefRepositoryAdapter,
    SqlStudyProgramRepositoryAdapter,
)
from infrastructure.adapter.outbound.http import ScrapResourceParserProviderAdapter

__all__ = [
    "SqlCurriculumRepositoryAdapter",
    "SqlModalityRepositoryAdapter",
    "SqlSubjectRepositoryAdapter",
    "SqlGradeLevelRepositoryAdapter",
    "SqlStudyProgramRefRepositoryAdapter",
    "SqlStudyProgramRepositoryAdapter",
    "ScrapResourceParserProviderAdapter",
]
