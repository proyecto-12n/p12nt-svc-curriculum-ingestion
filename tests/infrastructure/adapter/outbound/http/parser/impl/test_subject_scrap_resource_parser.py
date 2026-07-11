import pytest

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

    async def test_given_html_resource_when_get_children_then_returns_expected_child_hierarchy(
        self,
    ):
        children = [child async for child in self.parser.get_children(self.resource)]

        assert len(children) == 1
        assert children[0].url == "/grade"
        assert children[0].hierarchy == CurriculumHierarchyType.GRADE_LEVEL
        assert children[0].title == "1"

    async def test_given_html_without_title_when_get_title_then_raises(self):
        resource = ScrapResource(
            url="url", type=ResourceType.HTML, content="<html></html>"
        )

        with pytest.raises(AssertionError):
            await self.parser.get_title(resource)

    @pytest.mark.parametrize("suffix", ["3° medio", "4° MEDIO"])
    async def test_given_title_with_grade_suffix_when_get_title_then_removes_suffix(
        self, suffix: str
    ):
        resource = ScrapResource(
            url="url",
            type=ResourceType.HTML,
            content=f"<h1>Lengua y Literatura {suffix}</h1>",
        )

        assert await self.parser.get_title(resource) == "Lengua y Literatura"
