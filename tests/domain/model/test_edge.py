from domain.model.curriculum_hierarchy_type import CurriculumHierarchyType
from domain.model.edge import Edge
from domain.model.resource_type import ResourceType


class TestEdge:
    def test_given_full_edge_data_when_created_then_values_are_stored(self):
        edge = Edge(
            url="url",
            type=ResourceType.HTML,
            hierarchy=CurriculumHierarchyType.CURRICULUM,
            parent_url="parent",
            title="title",
            content="content",
        )

        assert edge.parent_url == "parent"
        assert edge.title == "title"
        assert edge.content == "content"

    def test_given_downloaded_resource_edge_when_hierarchy_omitted_then_hierarchy_is_none(
        self,
    ):
        edge = Edge(url="url", type=ResourceType.HTML, content="content")

        assert edge.hierarchy is None
