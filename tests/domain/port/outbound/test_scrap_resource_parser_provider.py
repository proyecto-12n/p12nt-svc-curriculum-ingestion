from domain.port.outbound.scrap_resource_parser_provider import (
    ScrapResourceParserProvider,
)


class ConcreteScrapResourceParserProvider:
    def get_parser(self, discriminator):
        return discriminator


class TestScrapResourceParserProvider:
    async def test_given_concrete_implementation_when_method_called_then_contract_is_satisfied(
        self,
    ):
        port: ScrapResourceParserProvider = ConcreteScrapResourceParserProvider()

        assert port.get_parser("type") == "type"
