from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from domain.model.resource_type import ResourceType
from domain.model.scrap_resource import ScrapResource
from infrastructure.adapter.outbound.http.parser.impl.subject_edge_parser import (
    SubjectScrapResourceParser,
)


class TestSubjectScrapResourceParser:
    def setup_method(self):
        self.parser = SubjectScrapResourceParser()
        self.resource = ScrapResource(
            url="url",
            type=ResourceType.HTML,
            content='<h1>Sub</h1><div class="cursos-wrapper"><div class="grade-wrapper"><a href="/grade">1</a></div></div>',
        )

    async def test_given_html_resource_when_get_edge_then_returns_current_hierarchy_edge(
        self,
    ):
        edge = await self.parser.get_edge(self.resource)

        assert edge.url == "url"
        assert edge.type == ResourceType.HTML
        assert edge.hierarchy == CurriculumHierarchyType.SUBJECT

    async def test_given_html_resource_when_get_children_then_returns_expected_child_hierarchy(
        self,
    ):
        children = [child async for child in self.parser.get_children(self.resource)]

        assert len(children) == 1
        assert children[0].url == "/grade"
        assert children[0].hierarchy == CurriculumHierarchyType.GRADE_LEVEL

    async def test_given_html_without_title_when_get_title_then_returns_none(self):
        resource = ScrapResource(
            url="url", type=ResourceType.HTML, content="<html></html>"
        )

        assert await self.parser.get_title(resource) is None
