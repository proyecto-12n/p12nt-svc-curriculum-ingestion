import pytest

from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from domain.model.edge import Edge
from domain.model.resource_type import ResourceType
from infrastructure.mapper.impl.modality_mapper import ModalityMapper
from infrastructure.models import Modality


class TestModalityMapper:
    def setup_method(self):
        self.mapper = ModalityMapper()

    def test_given_sql_model_when_to_edge_then_returns_matching_edge(self):
        model = Modality(id=1, url="url", title="title", parent_id=99, content="html")

        edge = self.mapper.to_edge(model)

        assert edge.url == "url"
        assert edge.type == ResourceType.HTML
        assert edge.hierarchy == CurriculumHierarchyType.MODALITY
        assert edge.title == "title"
        assert edge.content == "html"

    def test_given_valid_edge_when_to_model_then_returns_sql_model(self):
        edge = Edge(
            url="url",
            type=ResourceType.HTML,
            hierarchy=CurriculumHierarchyType.MODALITY,
            parent_url="parent",
            title="title",
            content="html",
        )

        model = self.mapper.to_model(edge)

        assert model.url == "url"
        assert model.title == "title"
        assert model.content == "html"

    def test_given_wrong_hierarchy_when_to_model_then_raises_assertion_error(self):
        edge = Edge(
            url="url",
            type=ResourceType.HTML,
            hierarchy=CurriculumHierarchyType.STUDY_PROGRAM,
            parent_url="parent",
            title="title",
            content="html",
        )

        with pytest.raises(AssertionError):
            self.mapper.to_model(edge)
