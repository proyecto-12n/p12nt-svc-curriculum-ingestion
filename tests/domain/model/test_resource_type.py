from domain.model.resource_type import ResourceType


class TestResourceType:
    def test_given_resource_type_when_reading_value_then_returns_wire_value(self):
        assert ResourceType.HTML.value == "HTML"
        assert ResourceType.PDF.value == "PDF"
