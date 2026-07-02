# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from enum import Enum


class CurriculumNodeType(str, Enum):
    CURRICULUM = "curriculum"
    MODALITY = "modality"
    SUBJECT = "subject"
    GRADE_LEVEL = "grade-level"
    STUDY_PROGRAM_REF = "study_program_ref"
    STUDY_PROGRAM = "study_program"
