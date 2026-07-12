import pytest

from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from infrastructure.adapter.outbound.http.parser.impl import (
    CurriculumScrapResourceParser,
    GradeLevelScrapResourceParser,
    CurriculumFrameworkScrapResourceParser,
    StudyProgramScrapResourceParser,
    StudyProgramRefScrapResourceParser,
    SubjectScrapResourceParser,
)
from infrastructure.adapter.outbound.http.scrap_resource_parser_provider_adapter import (
    ScrapResourceParserProviderAdapter,
)


class TestScrapResourceParserProviderAdapter:
    def setup_method(self):
        self.provider = ScrapResourceParserProviderAdapter()

    def test_given_known_type_when_get_parser_then_returns_matching_parser(self):
        assert isinstance(
            self.provider.get_parser(CurriculumHierarchyType.CURRICULUM),
            CurriculumScrapResourceParser,
        )
        assert isinstance(
            self.provider.get_parser(CurriculumHierarchyType.CURRICULUM_FRAMEWORK),
            CurriculumFrameworkScrapResourceParser,
        )
        assert isinstance(
            self.provider.get_parser(CurriculumHierarchyType.SUBJECT),
            SubjectScrapResourceParser,
        )
        assert isinstance(
            self.provider.get_parser(CurriculumHierarchyType.GRADE_LEVEL),
            GradeLevelScrapResourceParser,
        )
        assert isinstance(
            self.provider.get_parser(CurriculumHierarchyType.STUDY_PROGRAM_REF),
            StudyProgramRefScrapResourceParser,
        )
        assert isinstance(
            self.provider.get_parser(CurriculumHierarchyType.STUDY_PROGRAM),
            StudyProgramScrapResourceParser,
        )

    def test_given_unknown_type_when_get_parser_then_raises_value_error(self):
        with pytest.raises(ValueError, match="No parser configured"):
            self.provider.get_parser("invalid")
