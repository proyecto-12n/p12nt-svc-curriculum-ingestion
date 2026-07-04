# -*- coding: utf-8 -*-
from datetime import datetime, timezone
import pytest

from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from domain.model.resource_type import ResourceType
from infrastructure.mapper import (
    CurriculumMapper,
    ModalityMapper,
    SubjectMapper,
    GradeLevelMapper,
    StudyProgramRefMapper,
    StudyProgramMapper,
    CurriculumHierarchyMapperProviderAdapter,
)
from infrastructure.models.modality import Modality
from infrastructure.models.study_program import StudyProgram


def test_provider_resolves_all_mappers():
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


def test_provider_raises_error_for_invalid_type():
    provider = CurriculumHierarchyMapperProviderAdapter()

    with pytest.raises(ValueError) as excinfo:
        provider.get_mapper("invalid_type")
    assert "No mapper configured for node type" in str(excinfo.value)


def test_modality_mapping():
    mapper = ModalityMapper()
    now = datetime.now(timezone.utc)
    model = Modality(
        id=1,
        curriculum_id=10,
        url="http://test.url/modality",
        title="Modality Title",
        content="Modality Content",
        extracted_at=now,
    )

    node = mapper.to_domain_node(model)
    assert node.url == "http://test.url/modality"
    assert node.type == ResourceType.HTML
    assert node.level == CurriculumHierarchyType.MODALITY
    assert node.title == "Modality Title"
    assert node.content == "Modality Content"


def test_study_program_mapping():
    mapper = StudyProgramMapper()
    now = datetime.now(timezone.utc)
    model = StudyProgram(
        id=2,
        study_program_ref_id=20,
        url="http://test.url/program.pdf",
        title="Program Title",
        content=b"PDF BINARY CONTENT",
        checksum="123456",
        extracted_at=now,
    )

    node = mapper.to_domain_node(model)
    assert node.url == "http://test.url/program.pdf"
    assert node.type == ResourceType.PDF
    assert node.level == CurriculumHierarchyType.STUDY_PROGRAM
    assert node.title == "Program Title"
    assert node.content == b"PDF BINARY CONTENT"
