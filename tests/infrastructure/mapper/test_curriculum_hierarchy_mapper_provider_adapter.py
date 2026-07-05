import pytest

from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from infrastructure.mapper import (
    CurriculumHierarchyMapperProviderAdapter,
    CurriculumMapper,
    GradeLevelMapper,
    ModalityMapper,
    StudyProgramMapper,
    StudyProgramRefMapper,
    SubjectMapper,
)


class TestCurriculumHierarchyMapperProviderAdapter:
    def test_given_known_type_when_get_mapper_then_returns_matching_mapper(self):
        provider = CurriculumHierarchyMapperProviderAdapter()

        assert isinstance(
            provider.get_mapper(CurriculumHierarchyType.CURRICULUM), CurriculumMapper
        )
        assert isinstance(
            provider.get_mapper(CurriculumHierarchyType.MODALITY), ModalityMapper
        )
        assert isinstance(
            provider.get_mapper(CurriculumHierarchyType.SUBJECT), SubjectMapper
        )
        assert isinstance(
            provider.get_mapper(CurriculumHierarchyType.GRADE_LEVEL), GradeLevelMapper
        )
        assert isinstance(
            provider.get_mapper(CurriculumHierarchyType.STUDY_PROGRAM_REF),
            StudyProgramRefMapper,
        )
        assert isinstance(
            provider.get_mapper(CurriculumHierarchyType.STUDY_PROGRAM),
            StudyProgramMapper,
        )

    def test_given_unknown_type_when_get_mapper_then_raises_value_error(self):
        provider = CurriculumHierarchyMapperProviderAdapter()

        with pytest.raises(ValueError, match="No mapper configured"):
            provider.get_mapper("invalid")
