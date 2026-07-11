import pytest

from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from domain.model.resource_type import ResourceType
from domain.model.scrap_resource import ScrapResource
from infrastructure.adapter.outbound.http.parser.impl.study_program_ref_edge_parser import (
    StudyProgramRefScrapResourceParser,
)


class TestStudyProgramRefScrapResourceParser:
    def setup_method(self):
        self.parser = StudyProgramRefScrapResourceParser()
        self.resource = ScrapResource(
            url="url",
            type=ResourceType.HTML,
            content='<h1>Ref</h1><a href="/file.pdf">PDF</a>',
        )

    async def test_given_html_resource_when_get_children_then_returns_expected_child_hierarchy(
        self,
    ):
        children = [child async for child in self.parser.get_children(self.resource)]

        assert len(children) == 1
        assert children[0].url == "/file.pdf"
        assert children[0].hierarchy == CurriculumHierarchyType.STUDY_PROGRAM
        assert children[0].title == "PDF"

    async def test_given_html_without_title_when_get_title_then_raises(self):
        resource = ScrapResource(
            url="url", type=ResourceType.HTML, content="<html></html>"
        )

        with pytest.raises(AssertionError):
            await self.parser.get_title(resource)
