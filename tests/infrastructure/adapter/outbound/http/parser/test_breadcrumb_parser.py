from bs4 import BeautifulSoup
import pytest

from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from infrastructure.adapter.outbound.http.parser.breadcrumb_parser import (
    BreadcrumbParser,
)


class TestBreadcrumbParser:
    def setup_method(self):
        self.parser = BreadcrumbParser()

    def test_given_breadcrumb_when_parse_then_maps_components_to_hierarchy(self):
        soup = BeautifulSoup(
            """
            <ol class="breadcrumb">
              <li><a href="https://www.curriculumnacional.cl/">Inicio</a></li>
              <li><a href="https://www.curriculumnacional.cl/curriculum">Currículum</a></li>
              <li><a href="/Modality">Modality</a></li>
            </ol>
            """,
            "html.parser",
        )

        breadcrumbs = self.parser.parse(soup)

        assert breadcrumbs[CurriculumHierarchyType.CURRICULUM].url == (
            "https://www.curriculumnacional.cl/curriculum"
        )
        assert breadcrumbs[CurriculumHierarchyType.MODALITY].url == "/Modality"
        assert CurriculumHierarchyType.SUBJECT not in breadcrumbs

    def test_given_required_breadcrumb_text_when_parse_then_ignores_required_urls(self):
        soup = BeautifulSoup(
            """
            <ol class="breadcrumb">
              <li><a href="/different-home">Inicio</a></li>
              <li><a href="/different-curriculum">Currículum</a></li>
            </ol>
            """,
            "html.parser",
        )

        breadcrumbs = self.parser.parse(soup)

        assert breadcrumbs[CurriculumHierarchyType.CURRICULUM].url == (
            "/different-curriculum"
        )

    def test_given_soup_without_required_breadcrumb_when_parse_then_raises(self):
        with pytest.raises(AssertionError, match="First breadcrumb must be Inicio"):
            self.parser.parse(BeautifulSoup("<main></main>", "html.parser"))

    def test_given_wrong_curriculum_breadcrumb_when_parse_then_raises(self):
        soup = BeautifulSoup(
            """
            <ol class="breadcrumb">
              <li>Inicio</li>
              <li>Wrong</li>
            </ol>
            """,
            "html.parser",
        )

        with pytest.raises(
            AssertionError, match="Second breadcrumb must be Currículum"
        ):
            self.parser.parse(soup)
