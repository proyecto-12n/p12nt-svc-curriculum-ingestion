import pytest

from domain.model.resource_type import ResourceType
from domain.model.scrap_resource import ScrapResource
from infrastructure.util.beautiful_soup_builder import BeautifulSoupBuilder


class TestBeautifulSoupBuilder:
    def test_given_html_resource_when_build_then_returns_searchable_soup(self):
        resource = ScrapResource(
            url="url", type=ResourceType.HTML, content="<div id='x'>Hi</div>"
        )

        soup = BeautifulSoupBuilder.build(resource)

        assert soup.find(id="x").text == "Hi"

    def test_given_pdf_resource_when_build_then_raises_value_error(self):
        resource = ScrapResource(url="url", type=ResourceType.PDF, content="pdf")

        with pytest.raises(ValueError, match="Cannot build BeautifulSoup"):
            BeautifulSoupBuilder.build(resource)
