from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from domain.model.resource_type import ResourceType
from domain.model.scrap_resource import ScrapResource
from infrastructure.adapter.outbound.http.parser.impl.grade_level_edge_parser import (
    GradeLevelScrapResourceParser,
)


class TestGradeLevelScrapResourceParser:
    def setup_method(self):
        self.parser = GradeLevelScrapResourceParser()
        self.resource = ScrapResource(
            url="url",
            type=ResourceType.HTML,
            content='<h1>Grade</h1><div class="three-grid-content"><div class="card--content"><span class="badge">Programa de estudio</span><a href="/ref">Programa</a></div></div>',
        )

    async def test_given_html_resource_when_get_edge_then_returns_current_hierarchy_edge(
        self,
    ):
        edge = await self.parser.get_edge(self.resource)

        assert edge.url == "url"
        assert edge.type == ResourceType.HTML
        assert edge.hierarchy == CurriculumHierarchyType.GRADE_LEVEL

    async def test_given_html_resource_when_get_children_then_returns_expected_child_hierarchy(
        self,
    ):
        children = [child async for child in self.parser.get_children(self.resource)]

        assert len(children) == 1
        assert children[0].url == "/ref"
        assert children[0].hierarchy == CurriculumHierarchyType.STUDY_PROGRAM_REF

    async def test_given_html_without_title_when_get_title_then_returns_none(self):
        resource = ScrapResource(
            url="url", type=ResourceType.HTML, content="<html></html>"
        )

        assert await self.parser.get_title(resource) is None
