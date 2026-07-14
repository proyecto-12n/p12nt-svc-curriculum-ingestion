# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from domain.model.modality import Modality
from domain.model.subject import Subject
from domain.model.grade_level import GradeLevel
from domain.model.grade_level_detail_report import GradeLevelDetailReport
from domain.model.grade_level_summary_report import GradeLevelSummaryReport
from domain.model.study_program import StudyProgram
from domain.model.study_program_ref import StudyProgramRef
from domain.model.resource_type import ResourceType
from domain.model.pdf_resource import PDFResource
from domain.model.edge import Edge
from domain.model.curriculum import Curriculum
from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from domain.model.scrap_resource_parser_result import ScrapResourceParserResult

__all__ = [
    "Modality",
    "Subject",
    "GradeLevel",
    "GradeLevelDetailReport",
    "GradeLevelSummaryReport",
    "StudyProgram",
    "StudyProgramRef",
    "ResourceType",
    "PDFResource",
    "Edge",
    "Curriculum",
    "CurriculumHierarchyType",
    "ScrapResourceParserResult",
]
