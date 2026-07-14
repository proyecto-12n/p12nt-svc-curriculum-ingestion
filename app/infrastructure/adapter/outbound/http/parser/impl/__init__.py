# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from infrastructure.adapter.outbound.http.parser.impl.curriculum_edge_parser import (
    CurriculumScrapResourceParser,
)
from infrastructure.adapter.outbound.http.parser.impl.grade_level_edge_parser import (
    GradeLevelScrapResourceParser,
)
from infrastructure.adapter.outbound.http.parser.impl.curriculum_framework_edge_parser import (
    CurriculumFrameworkScrapResourceParser,
)
from infrastructure.adapter.outbound.http.parser.impl.study_program_edge_parser import (
    StudyProgramScrapResourceParser,
)
from infrastructure.adapter.outbound.http.parser.impl.study_program_ref_edge_parser import (
    StudyProgramRefScrapResourceParser,
)
from infrastructure.adapter.outbound.http.parser.impl.subject_edge_parser import (
    SubjectScrapResourceParser,
)

__all__ = [
    "CurriculumScrapResourceParser",
    "GradeLevelScrapResourceParser",
    "CurriculumFrameworkScrapResourceParser",
    "StudyProgramScrapResourceParser",
    "StudyProgramRefScrapResourceParser",
    "SubjectScrapResourceParser",
]
