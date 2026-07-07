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
    def setup_method(self):
        self.provider = CurriculumHierarchyMapperProviderAdapter()

    def test_given_known_type_when_get_mapper_then_returns_matching_mapper(self):
        assert isinstance(
            self.provider.get_mapper(CurriculumHierarchyType.CURRICULUM),
            CurriculumMapper,
        )
        assert isinstance(
            self.provider.get_mapper(CurriculumHierarchyType.MODALITY), ModalityMapper
        )
        assert isinstance(
            self.provider.get_mapper(CurriculumHierarchyType.SUBJECT), SubjectMapper
        )
        assert isinstance(
            self.provider.get_mapper(CurriculumHierarchyType.GRADE_LEVEL),
            GradeLevelMapper,
        )
        assert isinstance(
            self.provider.get_mapper(CurriculumHierarchyType.STUDY_PROGRAM_REF),
            StudyProgramRefMapper,
        )
        assert isinstance(
            self.provider.get_mapper(CurriculumHierarchyType.STUDY_PROGRAM),
            StudyProgramMapper,
        )

    def test_given_unknown_type_when_get_mapper_then_raises_value_error(self):
        with pytest.raises(ValueError, match="No mapper configured"):
            self.provider.get_mapper("invalid")
