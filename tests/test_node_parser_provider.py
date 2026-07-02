# -*- coding: utf-8 -*-
import pytest
from app.domain.model.curriculum_node_type import CurriculumNodeType
from app.infrastructure.adapter.outbound.http.parser.http_node_parser_provider_adapter import (
    HttpNodeParserProviderAdapter,
)
from app.infrastructure.adapter.outbound.http.parser.impl.curriculum_node_parser import (
    CurriculumNodeParser,
)
from app.infrastructure.adapter.outbound.http.parser.impl.modality_node_parser import (
    ModalityNodeParser,
)
from app.infrastructure.adapter.outbound.http.parser.impl.subject_node_parser import (
    SubjectNodeParser,
)
from app.infrastructure.adapter.outbound.http.parser.impl.grade_level_node_parser import (
    GradeLevelNodeParser,
)
from app.infrastructure.adapter.outbound.http.parser.impl.study_program_ref_node_parser import (
    StudyProgramRefNodeParser,
)
from app.infrastructure.adapter.outbound.http.parser.impl.study_program_node_parser import (
    StudyProgramNodeParser,
)


def test_http_node_parser_provider_adapter_returns_correct_parsers():
    provider = HttpNodeParserProviderAdapter()

    assert isinstance(
        provider.get_parser(CurriculumNodeType.CURRICULUM), CurriculumNodeParser
    )
    assert isinstance(
        provider.get_parser(CurriculumNodeType.MODALITY), ModalityNodeParser
    )
    assert isinstance(
        provider.get_parser(CurriculumNodeType.SUBJECT), SubjectNodeParser
    )
    assert isinstance(
        provider.get_parser(CurriculumNodeType.GRADE_LEVEL), GradeLevelNodeParser
    )
    assert isinstance(
        provider.get_parser(CurriculumNodeType.STUDY_PROGRAM_REF),
        StudyProgramRefNodeParser,
    )
    assert isinstance(
        provider.get_parser(CurriculumNodeType.STUDY_PROGRAM), StudyProgramNodeParser
    )


def test_http_node_parser_provider_adapter_invalid_discriminator():
    provider = HttpNodeParserProviderAdapter()

    with pytest.raises(ValueError) as excinfo:
        provider.get_parser("invalid_type")  # type: ignore

    assert "No parser configured for discriminator: invalid_type" in str(
        excinfo.value
    )
