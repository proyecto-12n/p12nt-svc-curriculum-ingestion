from domain.model.resource_type import ResourceType
from domain.model.scrap_resource import ScrapResource


class TestScrapResource:
    def test_given_html_content_when_created_then_resource_keeps_type_and_content(self):
        resource = ScrapResource(url="url", type=ResourceType.HTML, content="html")

        assert resource.url == "url"
        assert resource.type == ResourceType.HTML
        assert resource.content == "html"
