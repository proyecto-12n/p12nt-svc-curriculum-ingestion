# -*- coding: utf-8 -*-
import pytest
from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from infrastructure.adapter.outbound.http.parser.scrap_resource_parser_provider_adapter import (
    ScrapResourceParserProviderAdapter,
)
from infrastructure.adapter.outbound.http.parser.impl.curriculum_node_parser import (
    CurriculumScrapResourceParser,
)
from infrastructure.adapter.outbound.http.parser.impl.modality_node_parser import (
    ModalityScrapResourceParser,
)
from infrastructure.adapter.outbound.http.parser.impl.subject_node_parser import (
    SubjectScrapResourceParser,
)
from infrastructure.adapter.outbound.http.parser.impl.grade_level_node_parser import (
    GradeLevelScrapResourceParser,
)
from infrastructure.adapter.outbound.http.parser.impl.study_program_ref_node_parser import (
    StudyProgramRefScrapResourceParser,
)
from infrastructure.adapter.outbound.http.parser.impl.study_program_node_parser import (
    StudyProgramScrapResourceParser,
)


def test_http_node_parser_provider_adapter_returns_correct_parsers():
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
        provider.get_parser(CurriculumHierarchyType.SUBJECT), SubjectScrapResourceParser
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


def test_http_node_parser_provider_adapter_invalid_discriminator():
    provider = ScrapResourceParserProviderAdapter()

    with pytest.raises(ValueError) as excinfo:
        provider.get_parser("invalid_type")  # type: ignore

    assert "No parser configured for discriminator: invalid_type" in str(excinfo.value)
