# -*- coding: utf-8 -*-
"""
NextProject © 2026

This file is part of *P12nt*.
Unauthorized copying of this file, via any medium is strictly prohibited.
All rights reserved.
"""

from typing import Dict, Any

from sqlmodel import Session

from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from infrastructure.adapter.outbound.db.curriculum_hierarchy_repository import (
    CurriculumHierarchyRepository,
)
from domain.port.outbound.curriculum_hierarchy_repository_provider import (
    CurriculumHierarchyRepositoryProvider,
)
from infrastructure.adapter.outbound.db.impl.sql_curriculum_repository_adapter import (
    SqlCurriculumRepositoryAdapter,
)
from infrastructure.adapter.outbound.db.impl.sql_grade_level_repository_adapter import (
    SqlGradeLevelRepositoryAdapter,
)
from infrastructure.adapter.outbound.db.impl.sql_curriculum_framework_repository_adapter import (
    SqlCurriculumFrameworkRepositoryAdapter,
)
from infrastructure.adapter.outbound.db.impl.sql_study_program_ref_repository_adapter import (
    SqlStudyProgramRefRepositoryAdapter,
)
from infrastructure.adapter.outbound.db.impl.sql_study_program_repository_adapter import (
    SqlStudyProgramRepositoryAdapter,
)
from infrastructure.adapter.outbound.db.impl.sql_subject_repository_adapter import (
    SqlSubjectRepositoryAdapter,
)


class SqlCurriculumHierarchyRepositoryProviderAdapter(
    CurriculumHierarchyRepositoryProvider
):
    def __init__(self, session: Session):
        self._repositories: Dict[
            CurriculumHierarchyType, CurriculumHierarchyRepository[Any]
        ] = {
            CurriculumHierarchyType.CURRICULUM: SqlCurriculumRepositoryAdapter(session),
            CurriculumHierarchyType.CURRICULUM_FRAMEWORK: SqlCurriculumFrameworkRepositoryAdapter(
                session
            ),
            CurriculumHierarchyType.SUBJECT: SqlSubjectRepositoryAdapter(session),
            CurriculumHierarchyType.GRADE_LEVEL: SqlGradeLevelRepositoryAdapter(
                session
            ),
            CurriculumHierarchyType.STUDY_PROGRAM_REF: SqlStudyProgramRefRepositoryAdapter(
                session
            ),
            CurriculumHierarchyType.STUDY_PROGRAM: SqlStudyProgramRepositoryAdapter(
                session
            ),
        }

    def get_repository(
        self, node_type: CurriculumHierarchyType
    ) -> CurriculumHierarchyRepository[Any]:
        repo = self._repositories.get(node_type)
        if not repo:
            raise ValueError(f"No repository configured for edge type: {node_type}")
        return repo
