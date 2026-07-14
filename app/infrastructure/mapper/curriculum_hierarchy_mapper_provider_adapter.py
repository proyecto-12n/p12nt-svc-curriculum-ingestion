# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of Project-12nt.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Dict, Any

from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from domain.port.outbound.curriculum_hierarchy_mapper import (
    CurriculumHierarchyMapper,
)
from domain.port.outbound.curriculum_hierarchy_mapper_provider import (
    CurriculumHierarchyMapperProvider,
)
from infrastructure.mapper.impl.curriculum_mapper import CurriculumMapper
from infrastructure.mapper.impl.grade_level_mapper import GradeLevelMapper
from infrastructure.mapper.impl.curriculum_framework_mapper import (
    CurriculumFrameworkMapper,
)
from infrastructure.mapper.impl.study_program_mapper import StudyProgramMapper
from infrastructure.mapper.impl.study_program_ref_mapper import (
    StudyProgramRefMapper,
)
from infrastructure.mapper.impl.subject_mapper import SubjectMapper


class CurriculumHierarchyMapperProviderAdapter(CurriculumHierarchyMapperProvider):
    def __init__(self):
        self._mappers: Dict[
            CurriculumHierarchyType, CurriculumHierarchyMapper[Any, Any]
        ] = {
            CurriculumHierarchyType.CURRICULUM: CurriculumMapper(),
            CurriculumHierarchyType.CURRICULUM_FRAMEWORK: CurriculumFrameworkMapper(),
            CurriculumHierarchyType.SUBJECT: SubjectMapper(),
            CurriculumHierarchyType.GRADE_LEVEL: GradeLevelMapper(),
            CurriculumHierarchyType.STUDY_PROGRAM_REF: StudyProgramRefMapper(),
            CurriculumHierarchyType.STUDY_PROGRAM: StudyProgramMapper(),
        }

    def get_mapper(
        self, node_type: CurriculumHierarchyType
    ) -> CurriculumHierarchyMapper[Any, Any]:
        mapper = self._mappers.get(node_type)
        if not mapper:
            raise ValueError(f"No mapper configured for edge type: {node_type}")
        return mapper
