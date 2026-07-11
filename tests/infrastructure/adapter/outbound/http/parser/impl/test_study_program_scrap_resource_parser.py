from unittest.mock import MagicMock, patch

from domain.model.resource_type import ResourceType
from domain.model.scrap_resource import ScrapResource
from infrastructure.adapter.outbound.http.parser.impl.study_program_edge_parser import (
    StudyProgramScrapResourceParser,
)


class TestStudyProgramScrapResourceParser:
    def setup_method(self):
        self.parser = StudyProgramScrapResourceParser()
        self.resource = ScrapResource(
            url="https://test/program.pdf", type=ResourceType.PDF, content=b"pdf"
        )

    async def test_given_pdf_resource_when_get_children_then_yields_no_children(self):
        children = [child async for child in self.parser.get_children(self.resource)]

        assert children == []

    async def test_given_pdf_metadata_title_when_get_title_then_uses_metadata_title(
        self,
    ):
        document = MagicMock()
        document.metadata = {"title": "Metadata Title"}
        document.__enter__.return_value = document

        with patch("pymupdf.Document", return_value=document):
            title = await self.parser.get_title(self.resource)

        assert title == "Metadata Title"
