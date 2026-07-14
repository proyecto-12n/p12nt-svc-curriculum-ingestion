import pytest

from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from domain.model.resource_type import ResourceType
from domain.model.scrap_resource import ScrapResource
from infrastructure.adapter.outbound.http.parser.impl.curriculum_edge_parser import (
    CurriculumScrapResourceParser,
)


class TestCurriculumScrapResourceParser:
    def setup_method(self):
        self.parser = CurriculumScrapResourceParser()
        self.resource = ScrapResource(
            url="url",
            type=ResourceType.HTML,
            content='<h1>Bases</h1><div class="menu"><a href="/mod"><h3>Mod</h3></a></div>',
        )

    async def test_given_html_resource_when_get_children_then_returns_expected_child_hierarchy(
        self,
    ):
        children = [child async for child in self.parser.get_children(self.resource)]

        assert len(children) == 1
        assert children[0].url == "/mod"
        assert children[0].hierarchy == CurriculumHierarchyType.CURRICULUM_FRAMEWORK
        assert children[0].title == "Mod"

    async def test_given_html_without_title_when_get_title_then_raises(self):
        resource = ScrapResource(
            url="url", type=ResourceType.HTML, content="<html></html>"
        )

        with pytest.raises(AssertionError):
            await self.parser.get_title(resource)
