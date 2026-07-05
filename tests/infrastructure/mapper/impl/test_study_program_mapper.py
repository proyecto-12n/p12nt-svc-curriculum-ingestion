from hashlib import sha256

import pytest

from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from domain.model.edge import Edge
from domain.model.resource_type import ResourceType
from infrastructure.mapper.impl.study_program_mapper import StudyProgramMapper
from infrastructure.models import StudyProgram


class TestStudyProgramMapper:
    def test_given_sql_model_when_to_edge_then_returns_pdf_edge(self):
        model = StudyProgram(
            id=1,
            parent_id=2,
            url="url.pdf",
            title="title",
            content=b"pdf",
            checksum="checksum",
        )
        mapper = StudyProgramMapper()

        edge = mapper.to_edge(model)

        assert edge.type == ResourceType.PDF
        assert edge.hierarchy == CurriculumHierarchyType.STUDY_PROGRAM
        assert edge.content == b"pdf"

    def test_given_pdf_edge_when_to_model_then_returns_sql_model_with_checksum(self):
        edge = Edge(
            url="url.pdf",
            type=ResourceType.PDF,
            hierarchy=CurriculumHierarchyType.STUDY_PROGRAM,
            parent_url="parent",
            title="title",
            content=b"pdf",
        )
        mapper = StudyProgramMapper()

        model = mapper.to_model(edge)

        assert model.url == "url.pdf"
        assert model.content == b"pdf"
        assert model.checksum == sha256(b"pdf").hexdigest()

    def test_given_empty_pdf_content_when_to_model_then_returns_placeholder_model(self):
        edge = Edge(
            url="url.pdf",
            type=ResourceType.PDF,
            hierarchy=CurriculumHierarchyType.STUDY_PROGRAM,
            parent_url="parent",
            title="title",
            content=b"",
        )

        model = StudyProgramMapper().to_model(edge)

        assert model.content == b""

    def test_given_wrong_hierarchy_when_to_model_then_raises_assertion_error(self):
        edge = Edge(
            url="url",
            type=ResourceType.PDF,
            hierarchy=CurriculumHierarchyType.CURRICULUM,
        )

        with pytest.raises(AssertionError):
            StudyProgramMapper().to_model(edge)
