from domain.model.edge import Edge
from domain.model.resource_type import ResourceType
from infrastructure.adapter.outbound.http.parser.scrap_resource_parser import (
    ScrapResourceParser,
)


class ConcreteScrapResourceParser:
    async def get_children(self, resource):
        yield Edge(url="child", type=ResourceType.HTML)

    async def get_edge(self, resource):
        return Edge(url="edge", type=ResourceType.HTML)

    async def get_title(self, resource):
        return "title"


class TestScrapResourceParser:
    async def test_given_concrete_parser_when_methods_called_then_contract_is_satisfied(
        self,
    ):
        parser: ScrapResourceParser[str] = ConcreteScrapResourceParser()

        assert [child async for child in parser.get_children(object())][
            0
        ].url == "child"
        assert (await parser.get_edge(object())).url == "edge"
        assert await parser.get_title(object()) == "title"
