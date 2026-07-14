import pytest

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
            content="""
                <ol class="breadcrumb">
                  <li><a href="https://www.curriculumnacional.cl/">Inicio</a></li>
                  <li><a href="https://www.curriculumnacional.cl/curriculum">Currículum</a></li>
                  <li><a href="/CurriculumFramework">Modalidad</a></li>
                  <li><a href="/subject">Asignatura</a></li>
                  <li>Grade</li>
                </ol>
                <h1>Grade</h1>
                <div class="three-grid-content"><div class="card--content"><span class="badge">Programa de estudio</span><a href="/ref">Programa</a></div></div>
            """,
        )

    async def test_given_html_resource_when_get_children_then_returns_expected_child_hierarchy(
        self,
    ):
        children = [child async for child in self.parser.get_children(self.resource)]

        assert len(children) == 1
        assert children[0].url == "/ref"
        assert children[0].hierarchy == CurriculumHierarchyType.STUDY_PROGRAM_REF
        assert children[0].title == "Programa"

    async def test_given_html_without_title_when_get_title_then_raises(self):
        resource = ScrapResource(
            url="url", type=ResourceType.HTML, content="<html></html>"
        )

        with pytest.raises(AssertionError):
            await self.parser.get_title(resource)

    async def test_given_title_with_subject_prefix_when_get_title_then_removes_prefix(
        self,
    ):
        resource = ScrapResource(
            url="url",
            type=ResourceType.HTML,
            content="""
                <ol class="breadcrumb">
                  <li><a href="https://www.curriculumnacional.cl/">Inicio</a></li>
                  <li><a href="https://www.curriculumnacional.cl/curriculum">Currículum</a></li>
                  <li><a href="/CurriculumFramework">Modalidad</a></li>
                  <li><a href="/subject">Asignatura</a></li>
                  <li>Grade</li>
                </ol>
                <h1>Asignatura Grade</h1>
            """,
        )

        assert await self.parser.get_title(resource) == "Grade"

    async def test_given_title_with_subject_prefix_in_different_case_when_get_title_then_removes_prefix(
        self,
    ):
        resource = ScrapResource(
            url="url",
            type=ResourceType.HTML,
            content="""
                <ol class="breadcrumb">
                  <li><a href="https://www.curriculumnacional.cl/">Inicio</a></li>
                  <li><a href="https://www.curriculumnacional.cl/curriculum">Currículum</a></li>
                  <li><a href="/CurriculumFramework">Modalidad</a></li>
                  <li><a href="/subject">Asignatura</a></li>
                  <li>Grade</li>
                </ol>
                <h1>ASIGNATURA Grade</h1>
            """,
        )

        assert await self.parser.get_title(resource) == "Grade"

    async def test_given_special_grade_level_title_when_get_title_then_replaces_title(
        self,
    ):
        for title, expected_title in (
            ("SC (Sala Cuna)", "Sala Cuna (SC)"),
            ("NM (Nivel Medio)", "Nivel Medio (NM)"),
            ("NT (Nivel Transición)", "Nivel Transición (NT)"),
        ):
            resource = ScrapResource(
                url="url",
                type=ResourceType.HTML,
                content=f"""
                    <ol class="breadcrumb">
                      <li><a href="https://www.curriculumnacional.cl/">Inicio</a></li>
                      <li><a href="https://www.curriculumnacional.cl/curriculum">Currículum</a></li>
                      <li><a href="/CurriculumFramework">Modalidad</a></li>
                      <li><a href="/subject">Asignatura</a></li>
                      <li>{title}</li>
                    </ol>
                    <h1>{title}</h1>
                """,
            )

            assert await self.parser.get_title(resource) == expected_title
