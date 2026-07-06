# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from infrastructure.models.curriculum import Curriculum
from infrastructure.models.modality import Modality
from infrastructure.models.subject import Subject
from infrastructure.models.grade_level import GradeLevel
from infrastructure.models.study_program import StudyProgram
from infrastructure.models.study_program_json import StudyProgramJson
from infrastructure.models.study_program_markdown import StudyProgramMarkdown
from infrastructure.models.study_program_ref import StudyProgramRef

__all__ = [
    "Curriculum",
    "Modality",
    "Subject",
    "GradeLevel",
    "StudyProgram",
    "StudyProgramJson",
    "StudyProgramMarkdown",
    "StudyProgramRef",
]
