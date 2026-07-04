# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from infrastructure.adapter.outbound.http.parser.impl.curriculum_node_parser import (
    CurriculumScrapResourceParser,
)
from infrastructure.adapter.outbound.http.parser.impl.grade_level_node_parser import (
    GradeLevelScrapResourceParser,
)
from infrastructure.adapter.outbound.http.parser.impl.modality_node_parser import (
    ModalityScrapResourceParser,
)
from infrastructure.adapter.outbound.http.parser.impl.study_program_node_parser import (
    StudyProgramScrapResourceParser,
)
from infrastructure.adapter.outbound.http.parser.impl.study_program_ref_node_parser import (
    StudyProgramRefScrapResourceParser,
)
from infrastructure.adapter.outbound.http.parser.impl.subject_node_parser import (
    SubjectScrapResourceParser,
)

__all__ = [
    "CurriculumScrapResourceParser",
    "GradeLevelScrapResourceParser",
    "ModalityScrapResourceParser",
    "StudyProgramScrapResourceParser",
    "StudyProgramRefScrapResourceParser",
    "SubjectScrapResourceParser",
]
