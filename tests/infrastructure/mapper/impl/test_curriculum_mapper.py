import pytest

from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from domain.model.edge import Edge
from domain.model.resource_type import ResourceType
from infrastructure.mapper.impl.curriculum_mapper import CurriculumMapper
from infrastructure.models import Curriculum


class TestCurriculumMapper:
    def test_given_sql_model_when_to_edge_then_returns_matching_edge(self):
        model = Curriculum(id=1, url="url", title="title", content="html")
        mapper = CurriculumMapper()

        edge = mapper.to_edge(model)

        assert edge.url == "url"
        assert edge.type == ResourceType.HTML
        assert edge.hierarchy == CurriculumHierarchyType.CURRICULUM
        assert edge.title == "title"
        assert edge.content == "html"

    def test_given_valid_edge_when_to_model_then_returns_sql_model(self):
        edge = Edge(
            url="url",
            type=ResourceType.HTML,
            hierarchy=CurriculumHierarchyType.CURRICULUM,
            title="title",
            content="html",
        )
        mapper = CurriculumMapper()

        model = mapper.to_model(edge)

        assert model.url == "url"
        assert model.title == "title"
        assert model.content == "html"

    def test_given_wrong_hierarchy_when_to_model_then_raises_assertion_error(self):
        edge = Edge(
            url="url",
            type=ResourceType.HTML,
            hierarchy=CurriculumHierarchyType.STUDY_PROGRAM,
            title="title",
            content="html",
        )
        mapper = CurriculumMapper()

        with pytest.raises(AssertionError):
            mapper.to_model(edge)
