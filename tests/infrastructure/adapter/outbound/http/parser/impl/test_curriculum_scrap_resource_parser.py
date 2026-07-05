from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from domain.model.resource_type import ResourceType
from domain.model.scrap_resource import ScrapResource
from infrastructure.adapter.outbound.http.parser.impl.curriculum_node_parser import (
    CurriculumScrapResourceParser,
)


class TestCurriculumScrapResourceParser:
    async def test_given_html_resource_when_get_edge_then_returns_current_hierarchy_edge(
        self,
    ):
        resource = ScrapResource(
            url="url",
            type=ResourceType.HTML,
            content='<h1>Bases</h1><div class="menu"><a href="/mod"><h3>Mod</h3></a></div>',
        )
        parser = CurriculumScrapResourceParser()

        edge = await parser.get_edge(resource)

        assert edge.url == "url"
        assert edge.type == ResourceType.HTML
        assert edge.hierarchy == CurriculumHierarchyType.CURRICULUM

    async def test_given_html_resource_when_get_children_then_returns_expected_child_hierarchy(
        self,
    ):
        resource = ScrapResource(
            url="url",
            type=ResourceType.HTML,
            content='<h1>Bases</h1><div class="menu"><a href="/mod"><h3>Mod</h3></a></div>',
        )
        parser = CurriculumScrapResourceParser()

        children = [child async for child in parser.get_children(resource)]

        assert len(children) == 1
        assert children[0].url == "/mod"
        assert children[0].hierarchy == CurriculumHierarchyType.MODALITY

    async def test_given_html_without_title_when_get_title_then_returns_none(self):
        resource = ScrapResource(
            url="url", type=ResourceType.HTML, content="<html></html>"
        )

        assert await CurriculumScrapResourceParser().get_title(resource) is None
