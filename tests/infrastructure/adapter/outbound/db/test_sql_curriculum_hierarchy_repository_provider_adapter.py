import pytest

from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from infrastructure.adapter.outbound.db import (
    SqlCurriculumHierarchyRepositoryProviderAdapter,
    SqlCurriculumRepositoryAdapter,
    SqlGradeLevelRepositoryAdapter,
    SqlModalityRepositoryAdapter,
    SqlStudyProgramRefRepositoryAdapter,
    SqlStudyProgramRepositoryAdapter,
    SqlSubjectRepositoryAdapter,
)


class TestSqlCurriculumHierarchyRepositoryProviderAdapter:
    def test_given_known_type_when_get_repository_then_returns_matching_repository(
        self, session
    ):
        provider = SqlCurriculumHierarchyRepositoryProviderAdapter(session)

        assert isinstance(
            provider.get_repository(CurriculumHierarchyType.CURRICULUM),
            SqlCurriculumRepositoryAdapter,
        )
        assert isinstance(
            provider.get_repository(CurriculumHierarchyType.MODALITY),
            SqlModalityRepositoryAdapter,
        )
        assert isinstance(
            provider.get_repository(CurriculumHierarchyType.SUBJECT),
            SqlSubjectRepositoryAdapter,
        )
        assert isinstance(
            provider.get_repository(CurriculumHierarchyType.GRADE_LEVEL),
            SqlGradeLevelRepositoryAdapter,
        )
        assert isinstance(
            provider.get_repository(CurriculumHierarchyType.STUDY_PROGRAM_REF),
            SqlStudyProgramRefRepositoryAdapter,
        )
        assert isinstance(
            provider.get_repository(CurriculumHierarchyType.STUDY_PROGRAM),
            SqlStudyProgramRepositoryAdapter,
        )

    def test_given_unknown_type_when_get_repository_then_raises_value_error(
        self, session
    ):
        provider = SqlCurriculumHierarchyRepositoryProviderAdapter(session)

        with pytest.raises(ValueError, match="No repository configured"):
            provider.get_repository("invalid")
