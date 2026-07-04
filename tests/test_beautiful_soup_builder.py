# -*- coding: utf-8 -*-
import pytest

from domain.model.resource_type import ResourceType
from domain.model.scrap_resource import ScrapResource
from infrastructure.util.beautiful_soup_builder import BeautifulSoupBuilder


def test_beautiful_soup_builder_success():
    resource = ScrapResource(
        url="https://test.url",
        type=ResourceType.HTML,
        content="<html><body><div id='test'>Hello World</div></body></html>",
    )

    soup = BeautifulSoupBuilder.build(resource)
    assert soup.find(id="test").text == "Hello World"


def test_beautiful_soup_builder_invalid_type():
    resource = ScrapResource(
        url="https://test.url/doc.pdf", type=ResourceType.PDF, content="binary_content"
    )

    with pytest.raises(ValueError) as excinfo:
        BeautifulSoupBuilder.build(resource)
    assert "Cannot build BeautifulSoup from resource type" in str(excinfo.value)
