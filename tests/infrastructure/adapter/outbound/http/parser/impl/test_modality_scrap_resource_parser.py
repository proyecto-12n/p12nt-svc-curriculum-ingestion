import pytest

from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from domain.model.resource_type import ResourceType
from domain.model.scrap_resource import ScrapResource
from infrastructure.adapter.outbound.http.parser.impl.modality_edge_parser import (
    ModalityScrapResourceParser,
)


class TestModalityScrapResourceParser:
    def setup_method(self):
        self.parser = ModalityScrapResourceParser()
        self.resource = ScrapResource(
            url="url",
            type=ResourceType.HTML,
            content='<h1>Mod</h1><div class="subject"><a href="/sub"><span class="subject-title">Sub</span></a></div>',
        )

    async def test_given_html_resource_when_get_edge_then_returns_current_hierarchy_edge(
        self,
    ):
        edge = await self.parser.get_edge(self.resource)

        assert edge.url == "url"
        assert edge.type == ResourceType.HTML
        assert edge.hierarchy == CurriculumHierarchyType.MODALITY

    async def test_given_html_resource_when_get_children_then_returns_expected_child_hierarchy(
        self,
    ):
        children = [child async for child in self.parser.get_children(self.resource)]

        assert len(children) == 1
        assert children[0].url == "/sub"
        assert children[0].hierarchy == CurriculumHierarchyType.SUBJECT

    async def test_given_html_without_title_when_get_title_then_raises(self):
        resource = ScrapResource(
            url="url", type=ResourceType.HTML, content="<html></html>"
        )

        with pytest.raises(AssertionError):
            await self.parser.get_title(resource)
