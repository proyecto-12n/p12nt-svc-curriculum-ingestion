from unittest.mock import MagicMock, patch

from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from domain.model.resource_type import ResourceType
from domain.model.scrap_resource import ScrapResource
from infrastructure.adapter.outbound.http.parser.impl.study_program_node_parser import (
    StudyProgramScrapResourceParser,
)


class TestStudyProgramScrapResourceParser:
    async def test_given_pdf_resource_when_get_edge_then_returns_study_program_edge(
        self,
    ):
        resource = ScrapResource(
            url="https://test/program.pdf", type=ResourceType.PDF, content=b"pdf"
        )

        edge = await StudyProgramScrapResourceParser().get_edge(resource)

        assert edge.hierarchy == CurriculumHierarchyType.STUDY_PROGRAM
        assert edge.title == "program"
        assert edge.content == b"pdf"

    async def test_given_pdf_resource_when_get_children_then_yields_no_children(self):
        resource = ScrapResource(
            url="https://test/program.pdf", type=ResourceType.PDF, content=b"pdf"
        )

        children = [
            child
            async for child in StudyProgramScrapResourceParser().get_children(resource)
        ]

        assert children == []

    async def test_given_pdf_metadata_title_when_get_title_then_uses_metadata_title(
        self,
    ):
        resource = ScrapResource(
            url="https://test/program.pdf", type=ResourceType.PDF, content=b"pdf"
        )
        document = MagicMock()
        document.metadata = {"title": "Metadata Title"}
        document.__enter__.return_value = document

        with patch("pymupdf.Document", return_value=document):
            title = await StudyProgramScrapResourceParser().get_title(resource)

        assert title == "Metadata Title"
