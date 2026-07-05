import pytest

from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from infrastructure.adapter.outbound.http.parser.impl import (
    CurriculumScrapResourceParser,
    GradeLevelScrapResourceParser,
    ModalityScrapResourceParser,
    StudyProgramScrapResourceParser,
    StudyProgramRefScrapResourceParser,
    SubjectScrapResourceParser,
)
from infrastructure.adapter.outbound.http.scrap_resource_parser_provider_adapter import (
    ScrapResourceParserProviderAdapter,
)


class TestScrapResourceParserProviderAdapter:
    def test_given_known_type_when_get_parser_then_returns_matching_parser(self):
        provider = ScrapResourceParserProviderAdapter()

        assert isinstance(
            provider.get_parser(CurriculumHierarchyType.CURRICULUM),
            CurriculumScrapResourceParser,
        )
        assert isinstance(
            provider.get_parser(CurriculumHierarchyType.MODALITY),
            ModalityScrapResourceParser,
        )
        assert isinstance(
            provider.get_parser(CurriculumHierarchyType.SUBJECT),
            SubjectScrapResourceParser,
        )
        assert isinstance(
            provider.get_parser(CurriculumHierarchyType.GRADE_LEVEL),
            GradeLevelScrapResourceParser,
        )
        assert isinstance(
            provider.get_parser(CurriculumHierarchyType.STUDY_PROGRAM_REF),
            StudyProgramRefScrapResourceParser,
        )
        assert isinstance(
            provider.get_parser(CurriculumHierarchyType.STUDY_PROGRAM),
            StudyProgramScrapResourceParser,
        )

    def test_given_unknown_type_when_get_parser_then_raises_value_error(self):
        provider = ScrapResourceParserProviderAdapter()

        with pytest.raises(ValueError, match="No parser configured"):
            provider.get_parser("invalid")
